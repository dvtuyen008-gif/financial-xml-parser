import pandas as pd
from loguru import logger


class FinancialReconciler:
    """Compare calculated transaction totals against an expected amount."""

    def reconcile(
        self,
        df: pd.DataFrame,
        expected_total: float,
        amount_column: str = "Amount",
        tolerance: float = 0.01,
    ) -> dict:
        calculated_total = float(df[amount_column].sum()) if not df.empty else 0.0
        difference = calculated_total - expected_total
        matched = abs(difference) <= tolerance

        result = {
            "calculated_total": calculated_total,
            "expected_total": expected_total,
            "difference": difference,
            "matched": matched,
        }

        if matched:
            logger.info(
                "Reconciliation matched. calculated_total={:.2f} expected_total={:.2f}",
                calculated_total,
                expected_total,
            )
        else:
            logger.warning(
                "Reconciliation mismatch. calculated_total={:.2f} expected_total={:.2f} difference={:.2f}",
                calculated_total,
                expected_total,
                difference,
            )

        return result
