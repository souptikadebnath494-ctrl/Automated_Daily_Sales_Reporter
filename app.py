
import streamlit as st
import pandas as pd
import plotly.express as px
import io

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="Smart Automated Daily Sales Reporter",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------------
# PROFESSIONAL DASHBOARD DESIGN
# -----------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #F4F7FB;
}

h1 {
    color: #17365D;
}

h2, h3 {
    color: #24476B;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #DCE6F1;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# PDF REPORT GENERATOR FUNCTION
# -----------------------------------------

def generate_pdf_report(
    total_revenue,
    total_quantity,
    total_orders,
    total_products,
    product_data
):

    buffer = io.BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "SMART AUTOMATED DAILY SALES REPORTER",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Professional Sales Analytics Report",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 15))

    summary_data = [
        ["Sales Summary", "Value"],
        ["Total Revenue", f"Rs. {total_revenue:,.2f}"],
        ["Total Quantity", str(total_quantity)],
        ["Total Orders", str(total_orders)],
        ["Total Products", str(total_products)]
    ]

    summary_table = Table(
        summary_data,
        colWidths=[250, 200]
    )

    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("PADDING", (0, 0), (-1, -1), 8),
        ])
    )

    elements.append(summary_table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Product Wise Revenue",
            styles["Heading2"]
        )
    )

    product_table_data = [
        ["Product", "Revenue"]
    ]

    for _, row in product_data.iterrows():

        product_table_data.append([
            str(row["Product"]),
            f"Rs. {row['Revenue']:,.2f}"
        ])

    product_table = Table(
        product_table_data,
        colWidths=[250, 200],
        repeatRows=1
    )

    product_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ])
    )

    elements.append(product_table)

    pdf.build(elements)

    buffer.seek(0)

    return buffer.getvalue()

# -----------------------------------------
# DASHBOARD TITLE
# -----------------------------------------

st.title("📊 SMART AUTOMATED DAILY SALES REPORTER")

st.subheader(
    "Interactive Sales Analytics and Business Intelligence Dashboard"
)

st.write(
    "Upload your sales dataset to analyze revenue, orders, "
    "products and business performance."
)

# -----------------------------------------
# SIDEBAR
# -----------------------------------------

st.sidebar.header("📂 Upload Sales Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)

# -----------------------------------------
# MAIN DASHBOARD
# -----------------------------------------

if uploaded_file is not None:

    try:

        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Clean column names
        df.columns = df.columns.str.strip()

        # -----------------------------------------
        # COLUMN DETECTION
        # -----------------------------------------

        column_map = {
            col.lower().replace("_", " ").strip(): col
            for col in df.columns
        }

        def find_column(possible_names):

            for name in possible_names:

                key = name.lower().replace("_", " ").strip()

                if key in column_map:
                    return column_map[key]

            return None

        product_col = find_column([
            "Product",
            "Product Name",
            "Item",
            "Item Name"
        ])

        quantity_col = find_column([
            "Quantity",
            "Qty",
            "Units Sold"
        ])

        price_col = find_column([
            "Price",
            "Unit Price",
            "Selling Price"
        ])

        date_col = find_column([
            "Date",
            "Order Date",
            "Sales Date"
        ])

        order_col = find_column([
            "Order ID",
            "Order Number",
            "Transaction ID"
        ])

        revenue_col = find_column([
            "Revenue",
            "Total Revenue",
            "Sales",
            "Sales Amount",
            "Total Amount"
        ])

        # -----------------------------------------
        # DATA CLEANING
        # -----------------------------------------

        df = df.drop_duplicates()

        if quantity_col:

            df[quantity_col] = pd.to_numeric(
                df[quantity_col],
                errors="coerce"
            )

        if price_col:

            df[price_col] = pd.to_numeric(
                df[price_col],
                errors="coerce"
            )

        if revenue_col:

            df[revenue_col] = pd.to_numeric(
                df[revenue_col],
                errors="coerce"
            )

        if date_col:

            df[date_col] = pd.to_datetime(
                df[date_col],
                errors="coerce"
            )

        df = df.dropna(
            how="all"
        )

        # -----------------------------------------
        # REVENUE CALCULATION
        # -----------------------------------------

        if revenue_col:

            df["Calculated Revenue"] = df[revenue_col]

        elif price_col and quantity_col:

            df["Calculated Revenue"] = (
                df[price_col] * df[quantity_col]
            )

        else:

            st.error(
                "Revenue cannot be calculated. "
                "Please upload data containing Price and Quantity "
                "or a Revenue column."
            )

            st.stop()

        df["Calculated Revenue"] = pd.to_numeric(
            df["Calculated Revenue"],
            errors="coerce"
        ).fillna(0)

        # -----------------------------------------
        # KPI CALCULATIONS
        # -----------------------------------------

        total_revenue = df["Calculated Revenue"].sum()

        if quantity_col:

            total_quantity = df[quantity_col].fillna(0).sum()

        else:

            total_quantity = 0

        if order_col:

            total_orders = df[order_col].nunique()

        else:

            total_orders = len(df)

        if product_col:

            total_products = df[product_col].nunique()

        else:

            total_products = 0

        # -----------------------------------------
        # KPI DISPLAY
        # -----------------------------------------

        st.markdown("---")

        st.header("📈 Business Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "💰 Total Revenue",
            f"₹{total_revenue:,.2f}"
        )

        col2.metric(
            "🛒 Total Orders",
            f"{total_orders:,}"
        )

        col3.metric(
            "📦 Total Quantity",
            f"{total_quantity:,.0f}"
        )

        col4.metric(
            "🏷️ Total Products",
            f"{total_products:,}"
        )

        # -----------------------------------------
        # PRODUCT WISE REVENUE
        # -----------------------------------------

        st.markdown("---")

        st.header("🏆 Product Performance")

        if product_col:

            product_data = (
                df.groupby(product_col)["Calculated Revenue"]
                .sum()
                .reset_index()
            )

            product_data.columns = [
                "Product",
                "Revenue"
            ]

            product_data = product_data.sort_values(
                by="Revenue",
                ascending=False
            )

            fig_product = px.bar(
                product_data,
                x="Product",
                y="Revenue",
                title="Product Wise Revenue",
                color="Revenue",
                text_auto=".2s"
            )

            st.plotly_chart(
                fig_product,
                use_container_width=True
            )

            best_product = product_data.iloc[0]["Product"]

            st.success(
                f"⭐ Best Selling Product by Revenue: {best_product}"
            )

        else:

            product_data = pd.DataFrame(
                columns=["Product", "Revenue"]
            )

            st.warning(
                "Product column was not found in the uploaded CSV."
            )

        # -----------------------------------------
        # DAILY SALES GRAPH
        # -----------------------------------------

        st.markdown("---")

        st.header("📅 Daily Sales Analysis")

        if date_col:

            daily_sales = (
                df.dropna(subset=[date_col])
                .groupby(date_col)["Calculated Revenue"]
                .sum()
                .reset_index()
            )

            daily_sales.columns = [
                "Date",
                "Revenue"
            ]

            daily_sales = daily_sales.sort_values(
                by="Date"
            )

            fig_daily = px.line(
                daily_sales,
                x="Date",
                y="Revenue",
                title="Daily Revenue Trend",
                markers=True
            )

            st.plotly_chart(
                fig_daily,
                use_container_width=True
            )

        else:

            st.info(
                "Date column not found. Daily sales graph is unavailable."
            )

        # -----------------------------------------
        # QUANTITY GRAPH
        # -----------------------------------------

        if product_col and quantity_col:

            st.header("📦 Product Wise Quantity Sold")

            quantity_data = (
                df.groupby(product_col)[quantity_col]
                .sum()
                .reset_index()
            )

            fig_quantity = px.bar(
                quantity_data,
                x=product_col,
                y=quantity_col,
                title="Quantity Sold by Product",
                color=quantity_col
            )

            st.plotly_chart(
                fig_quantity,
                use_container_width=True
            )

        # -----------------------------------------
        # DATA TABLE
        # -----------------------------------------

        st.markdown("---")

        st.header("📋 Complete Sales Dataset")

        st.dataframe(
            df,
            use_container_width=True
        )

        # -----------------------------------------
        # CSV DOWNLOAD
        # -----------------------------------------

        st.markdown("---")

        st.subheader("📥 Download CSV Report")

        csv_data = df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📄 Download CSV Report",
            data=csv_data,
            file_name="Sales_Report.csv",
            mime="text/csv"
        )

        # -----------------------------------------
        # PDF DOWNLOAD
        # -----------------------------------------

        st.subheader("📄 Download Professional PDF Report")

        pdf_data = generate_pdf_report(
            total_revenue,
            total_quantity,
            total_orders,
            total_products,
            product_data
        )

        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_data,
            file_name="Sales_Report.pdf",
            mime="application/pdf"
        )

        st.success(
            "✅ Sales Dashboard and Reports Generated Successfully!"
        )

    except Exception as e:

        st.error(
            f"An error occurred: {e}"
        )

else:

    st.info(
        "👈 Please upload your sales CSV file from the sidebar "
        "to start the dashboard."
    )

    st.markdown("""
    ### Dashboard Features

    - 📊 Interactive Sales Analytics
    - 💰 Revenue Calculation
    - 🛒 Order Analysis
    - 🏆 Best Selling Product
    - 📅 Daily Sales Graph
    - 📦 Product Quantity Analysis
    - 📄 CSV Report Download
    - 📑 Professional PDF Report Generator
    """)