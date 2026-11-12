import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def clean_sales_data(file_path):

    # Read sales dataset
    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Check required columns
    required = ["date", "product", "quantity", "unit_price"]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Remove duplicate records
    df = df.drop_duplicates().copy()

    # Remove missing values
    df = df.dropna(subset=required).copy()

    # Clean product names
    df["product"] = df["product"].astype(str).str.strip()
    df = df[df["product"] != ""].copy()

    # Convert numeric values
    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"], errors="coerce"
    )

    # Remove invalid numeric values
    df = df.dropna(subset=["quantity", "unit_price"])

    df = df[
        (df["quantity"] > 0) &
        (df["quantity"] % 1 == 0) &
        (df["unit_price"] >= 0)
    ].copy()

    df["quantity"] = df["quantity"].astype(int)

    # Convert date
    df["date"] = pd.to_datetime(
        df["date"], errors="coerce"
    )

    df = df.dropna(subset=["date"]).copy()

    # Calculate revenue
    df["revenue"] = df["quantity"] * df["unit_price"]

    return df


if __name__ == "__main__":

    df = clean_sales_data(BASE_DIR.parent / "sales.csv")
    df.to_csv(BASE_DIR / "cleaned_sales.csv", index=False)

    print("Data Cleaning Completed Successfully!")
    print(df)