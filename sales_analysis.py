from pathlib import Path
from data_cleaning import clean_sales_data

BASE_DIR = Path(__file__).resolve().parent.parent


# 1. Calculate Total Revenue
def total_revenue(df):
    return df["revenue"].sum()


# 2. Calculate Total Sales Records
def total_orders(df):
    if "order_id" in df.columns:
        return df["order_id"].nunique()

    return len(df)


# 3. Calculate Total Units Sold
def total_units_sold(df):
    return df["quantity"].sum()


# 4. Find Best-Selling Product
def best_selling_product(df):

    product_sales = df.groupby("product")["quantity"].sum()

    if product_sales.empty:
        return None

    return product_sales.idxmax()


# 5. Calculate Product-Wise Sales
def product_wise_sales(df):

    return (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )


# 6. Calculate Daily Sales
def daily_sales(df):

    return (
        df.groupby(df["date"].dt.date)["revenue"]
        .sum()
        .sort_index()
    )


# 7. Calculate Category-Wise Sales
def category_wise_sales(df):

    if "category" not in df.columns:
        return None

    return (
        df.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )


# 8. Calculate Product-Wise Quantity
def product_wise_quantity(df):

    return (
        df.groupby("product")["quantity"]
        .sum()
        .sort_values(ascending=False)
    )


# Main Program
if __name__ == "__main__":

    # Load and clean sales dataset
    file_path = BASE_DIR / "sales.csv"

    df = clean_sales_data(file_path)

    print("\n======================================")
    print("     AUTOMATED DAILY SALES REPORT")
    print("======================================")

    # Total Revenue
    print(
        "\nTotal Revenue (INR):",
        round(total_revenue(df), 2)
    )

    # Total Sales Records
    print(
        "Total Sales Records:",
        total_orders(df)
    )

    # Total Units Sold
    print(
        "Total Units Sold:",
        total_units_sold(df)
    )

    # Best-Selling Product
    print(
        "Best-Selling Product:",
        best_selling_product(df) or "N/A"
    )

    # Product-Wise Sales
    print("\n===== PRODUCT-WISE SALES =====")
    print(product_wise_sales(df))

    # Product-Wise Quantity
    print("\n===== PRODUCT-WISE QUANTITY =====")
    print(product_wise_quantity(df))

    # Daily Sales
    print("\n===== DAILY SALES =====")
    print(daily_sales(df))

    # Category-Wise Sales
    categories = category_wise_sales(df)

    if categories is not None:

        print("\n===== CATEGORY-WISE SALES =====")
        print(categories)

    else:

        print(
            "\nCategory-Wise Sales: "
            "Category column not available."
        )

    print("\n======================================")
    print("       REPORT GENERATED SUCCESSFULLY")
    print("======================================")