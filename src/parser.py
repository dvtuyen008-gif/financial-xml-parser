from pathlib import Path
from typing import Union

import pandas as pd
from lxml import etree
from loguru import logger


class XMLFinancialParser:
    """Parse bank statement XML files into a pandas DataFrame."""

    COLUMNS = [
        "TxId",
        "Date",
        "SenderAccount",
        "ReceiverAccount",
        "Amount",
        "Currency",
        "Status",
    ]

    def parse(self, xml_path: Union[str, Path]) -> pd.DataFrame:
        xml_path = Path(xml_path)
        if not xml_path.exists():
            raise FileNotFoundError(f"XML file not found: {xml_path}")

        logger.info(f"Parsing bank statement XML: {xml_path}")
        tree = etree.parse(str(xml_path))
        root = tree.getroot()

        rows = []
        for tx in root.xpath(".//Transaction"):
            rows.append(
                {
                    "TxId": self._text(tx, "TxId"),
                    "Date": self._text(tx, "Date"),
                    "SenderAccount": self._text(tx, "SenderAccount"),
                    "ReceiverAccount": self._text(tx, "ReceiverAccount"),
                    "Amount": self._amount(self._text(tx, "Amount")),
                    "Currency": self._text(tx, "Currency"),
                    "Status": self._text(tx, "Status"),
                }
            )

        df = pd.DataFrame(rows, columns=self.COLUMNS)
        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        logger.info(f"Parsed {len(df)} transaction(s)")
        return df

    def expected_total(self, xml_path: Union[str, Path]) -> float:
        xml_path = Path(xml_path)
        tree = etree.parse(str(xml_path))
        nodes = tree.getroot().xpath(".//ExpectedTotal")
        if not nodes or not (nodes[0].text or "").strip():
            raise ValueError("ExpectedTotal is missing from the XML file")
        return float(nodes[0].text.strip())

    @staticmethod
    def _text(element: etree._Element, tag: str) -> str:
        child = element.find(tag)
        if child is None or child.text is None:
            return ""
        return child.text.strip()

    @staticmethod
    def _amount(value: str) -> float:
        if not value:
            return 0.0
        return float(value.replace(",", ""))
