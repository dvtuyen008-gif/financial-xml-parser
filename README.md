# Automated Financial Report & XML Interbank Parser

## Overview

A Python-based automated solution designed to parse complex interbank XML financial statements, perform automated balance reconciliation with warning logs, and export structured multi-sheet Excel reports (Transactions and Reconciliation).

`XMLFinancialParser` extracts transaction fields (`TxId`, `Date`, `SenderAccount`, `ReceiverAccount`, `Amount`, `Currency`, `Status`) into a pandas DataFrame. `FinancialReconciler` then compares the calculated total against the expected total and records a match or a warning via loguru. The pipeline finishes by writing a professional Excel workbook ready for audit and operations review.

## Business Value

- **Automated audit trail** — every parse and reconciliation run is logged, so reviewers can trace totals, mismatches, and export paths without reconstructing the process by hand.
- **Zero human-error reconciliation** — totals are calculated from source XML and compared to `ExpectedTotal` in code, removing manual spreadsheet arithmetic.
- **High performance for financial data automation** — `lxml` and pandas handle XML ingestion and tabular processing efficiently, supporting repeatable batch-style statement processing.

## Key Features

- **Fast XML parsing with lxml and pandas** — bank statement XML is loaded with `lxml` and normalized into a typed DataFrame.
- **Automated reconciliation checks with loguru error detection** — calculated vs expected amounts are compared within a small tolerance; matches are logged at info level and mismatches as warnings.
- **Professional multi-sheet Excel output using openpyxl** — `data/output/financial_report.xlsx` includes a **Transactions** sheet and a **Reconciliation** sheet (`CalculatedTotal`, `ExpectedTotal`, `Difference`, `Matched`).

## Project Structure

```text
financial-xml-parser/
├── main.py                 # Entry point: sample XML, parse, reconcile, export
├── requirements.txt        # lxml, pandas, openpyxl, loguru
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── parser.py           # XMLFinancialParser
│   └── reconciler.py       # FinancialReconciler
└── data/
    ├── raw/                # Input XML (sample created on first run)
    └── output/             # Excel report (financial_report.xlsx)
```

## Getting Started

### Prerequisites

- Python 3.10 or later

### Installation

From the project root:

```bash
pip install -r requirements.txt
```

### Usage

```bash
python main.py
```

On first run, if `data/raw/sample_bank_statement.xml` does not exist, the script creates a sample interbank statement. It then:

1. Parses transactions into a DataFrame.
2. Reconciles the sum of `Amount` against `ExpectedTotal`.
3. Exports `data/output/financial_report.xlsx`.

Replace or add XML files under `data/raw/` using the same schema (`BankStatement` / `Transaction` elements and an `ExpectedTotal` node) to process real statements. Point `main.py` at a different path if you need to parse a file other than the sample.
