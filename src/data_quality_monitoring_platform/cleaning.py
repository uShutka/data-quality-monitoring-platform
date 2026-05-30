import pandas as pd

from data_quality_monitoring_platform.checks.formats import invalid_email_mask, invalid_phone_mask


def clean_customer_dataset(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.drop_duplicates(subset=["customer_id"]).copy()
    cleaned["email"] = cleaned["email"].astype(str).str.lower().str.strip()
    cleaned["phone"] = cleaned["phone"].astype(str).str.replace(r"\D", "", regex=True)
    cleaned["phone"] = cleaned["phone"].where(cleaned["phone"].str.len().between(8, 15), None)
    cleaned["phone"] = "+" + cleaned["phone"].fillna("")
    cleaned["phone"] = cleaned["phone"].replace("+", None)
    cleaned["country"] = cleaned["country"].fillna("UNKNOWN").astype(str).str.upper()
    cleaned["age"] = pd.to_numeric(cleaned["age"], errors="coerce").fillna(cleaned["age"].median())
    cleaned["lifetime_value"] = pd.to_numeric(cleaned["lifetime_value"], errors="coerce")
    cleaned["lifetime_value"] = cleaned["lifetime_value"].clip(lower=0, upper=cleaned["lifetime_value"].quantile(0.95))
    cleaned = cleaned[~invalid_email_mask(cleaned)]
    cleaned = cleaned[~invalid_phone_mask(cleaned)]
    return cleaned.reset_index(drop=True)
