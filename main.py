from pathlib import Path

import pandas as pd
from loguru import logger

from src.parser import XMLFinancialParser
from src.reconciler import FinancialReconciler

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "data" / "raw"
OUTPUT_DIR = ROOT / "data" / "output"
SAMPLE_XML = RAW_DIR / "sample_bank_statement.xml"
OUTPUT_XLSX = OUTPUT_DIR / "financial_report.xlsx"

SAMPLE_XML_CONTENT = """<?xml version="1.0" encoding="UTF-8"?>
<BankStatement>
  <AccountHolder>Acme Corp</AccountHolder>
  <StatementDate>2026-09-30</StatementDate>
  <ExpectedTotal>4250.75</ExpectedTotal>
  <Transactions>
    <Transaction>
      <TxId>TX-1001</TxId>
      <Date>2026-09-01</Date>
      <SenderAccount>VN-0011223344</SenderAccount>
      <ReceiverAccount>VN-9988776655</ReceiverAccount>
      <Amount>1500.00</Amount>
      <Currency>USD</Currency>
      <Status>SETTLED</Status>
    </Transaction>
    <Transaction>
      <TxId>TX-1002</TxId>
      <Date>2026-09-12</Date>
      <SenderAccount>VN-0011223344</SenderAccount>
      <ReceiverAccount>VN-5566778899</ReceiverAccount>
      <Amount>2000.50</Amount>
      <Currency>USD</Currency>
      <Status>SETTLED</Status>
    </Transaction>
    <Transaction>
      <TxId>TX-1003</TxId>
      <Date>2026-09-25</Date>
      <SenderAccount>VN-1122334455</SenderAccount>
      <ReceiverAccount>VN-0011223344</ReceiverAccount>
      <Amount>750.25</Amount>
      <Currency>USD</Currency>
      <Status>PENDING</Status>
    </Transaction>
  </Transactions>
</BankStatement>
"""


def ensure_sample_xml() -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if not SAMPLE_XML.exists():
        SAMPLE_XML.write_text(SAMPLE_XML_CONTENT, encoding="utf-8")
        logger.info(f"Created sample XML at {SAMPLE_XML}")
    else:
        logger.info(f"Using existing XML at {SAMPLE_XML}")
    return SAMPLE_XML


def export_report(df: pd.DataFrame, reconciliation: dict) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = pd.DataFrame(
        [
            {
                "CalculatedTotal": reconciliation["calculated_total"],
                "ExpectedTotal": reconciliation["expected_total"],
                "Difference": reconciliation["difference"],
                "Matched": reconciliation["matched"],
            }
        ]
    )
    with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Transactions", index=False)
        summary.to_excel(writer, sheet_name="Reconciliation", index=False)
    logger.info(f"Exported financial report to {OUTPUT_XLSX}")
    return OUTPUT_XLSX


def main() -> None:
    xml_path = ensure_sample_xml()
    parser = XMLFinancialParser()
    df = parser.parse(xml_path)
    expected_total = parser.expected_total(xml_path)
    reconciliation = FinancialReconciler().reconcile(df, expected_total)
    export_report(df, reconciliation)
    print(df.to_string(index=False))
    print(
        f"\nReconciliation matched: {reconciliation['matched']} | "
        f"calculated={reconciliation['calculated_total']:.2f} | "
        f"expected={reconciliation['expected_total']:.2f}"
    )


if __name__ == "__main__":
    main()
