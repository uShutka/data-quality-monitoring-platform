import pandas as pd

REQUIRED_COLUMNS = {"customer_id", "email", "amount"}

def quality_report(df: pd.DataFrame) -> dict:
    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    duplicate_rows = int(df.duplicated().sum())
    null_cells = int(df.isna().sum().sum())
    invalid_email_rows = int((~df.get("email", pd.Series(dtype=str)).astype(str).str.contains("@", na=False)).sum()) if "email" in df else 0
    outliers = int((df.get("amount", pd.Series(dtype=float)) > 10000).sum()) if "amount" in df else 0
    penalties = len(missing_columns) * 20 + duplicate_rows * 5 + null_cells * 2 + invalid_email_rows * 5 + outliers * 5
    return {"quality_score": max(0, 100 - penalties), "missing_columns": missing_columns, "duplicate_rows": duplicate_rows, "null_cells": null_cells, "invalid_email_rows": invalid_email_rows, "outliers": outliers}

def load_sample(path="data/customers.csv"):
    return pd.read_csv(path)

if __name__ == "__main__":
    print(quality_report(load_sample()))
