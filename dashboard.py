import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Business Insight Dashboard", page_icon="📊", layout="wide")

if "theme" not in st.session_state:
    st.session_state.theme = "light"

st.markdown(
    '<div style="background: linear-gradient(135deg, #7c3aed 0%, #ec4899 100%);text-align: center;padding: 3rem 2rem;border-radius: 24px;margin-bottom: 2rem;box-shadow: 0 20px 50px rgba(124, 58, 237, 0.25);">'
    '<h1 style="margin: 0; color: white; font-size: 2.8rem; font-weight: 800; letter-spacing: -1px;">📊 Insights Dashboard</h1>'
    '<p style="margin: 0.8rem 0 0 0; color: rgba(255,255,255,0.95); font-size: 1.1rem; font-weight: 400;">Visualize patterns. Make better decisions.</p>'
    "</div>",
    unsafe_allow_html=True,
)

THEMES = {
    "light": {
        "primary": "#7c3aed",
        "secondary": "#ec4899",
        "bg_main": "#ffffff",
        "bg_secondary": "#f9fafb",
        "text_primary": "#111827",
        "text_secondary": "#6b7280",
        "border": "#e5e7eb",
        "card_shadow": "0 4px 20px rgba(0,0,0,0.08)",
        "expander_bg": "#f8fafc",
    },
    "dark": {
        "primary": "#a78bfa",
        "secondary": "#f472b6",
        "bg_main": "#1f2937",
        "bg_secondary": "#111827",
        "text_primary": "#f9fafb",
        "text_secondary": "#d1d5db",
        "border": "#374151",
        "card_shadow": "0 4px 20px rgba(0,0,0,0.3)",
        "expander_bg": "#111827",
    },
}

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
:root{{--primary:{primary};--secondary:{secondary};--bg-main:{bg_main};--bg-secondary:{bg_secondary};--text-primary:{text_primary};--text-secondary:{text_secondary};--border:{border};--card-shadow:{card_shadow};--expander-bg:{expander_bg};}}
*{{font-family:'Poppins',-apple-system,sans-serif;}}
body,main{{background:var(--bg-secondary)!important;}}
.block-container{{padding:2rem 3rem!important;}}
[data-testid="stMetric"]{{background:linear-gradient(135deg,#7c3aed 0%,#ec4899 100%)!important;padding:16px 18px!important;border-radius:16px!important;color:white!important;box-shadow:var(--card-shadow)!important;border:none!important;}}
[data-testid="stMetric"] label{{color:rgba(255,255,255,0.95)!important;font-size:0.7rem!important;font-weight:600!important;line-height:1.1!important;white-space:normal!important;}}
[data-testid="stMetric"] [data-testid="stMetricValue"]{{color:white!important;font-size:1.4rem!important;font-weight:800!important;line-height:1.15!important;white-space:normal!important;}}
div[data-testid="stSidebar"]{{background:var(--bg-main)!important;border-right:1px solid var(--border)!important;}}
div[data-testid="stSidebar"] *,div[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *{{color:var(--text-primary)!important;opacity:1!important;}}
h1,h2,h3,h4,h5,h6,div[data-testid="stMarkdownContainer"],div[data-testid="stMarkdownContainer"] h1,div[data-testid="stMarkdownContainer"] h2,div[data-testid="stMarkdownContainer"] h3,div[data-testid="stMarkdownContainer"] h4,div[data-testid="stMarkdownContainer"] h5,div[data-testid="stMarkdownContainer"] h6,div[data-testid="stMarkdownContainer"] p,div[data-testid="stMarkdownContainer"] li,div[data-testid="stMarkdownContainer"] span{{color:var(--text-primary)!important;opacity:1!important;}}
h3{{font-size:1.3rem!important;margin-top:1.5rem!important;}}
[data-testid="stSelectbox"],[data-testid="stMultiSelect"],[data-testid="stRadio"],[data-testid="stSlider"],[data-testid="stTextArea"]{{padding:12px 14px!important;border-radius:12px!important;border:2px solid var(--border)!important;background:var(--bg-main)!important;color:var(--text-primary)!important;}}
.stButton>button{{background:linear-gradient(135deg,#7c3aed 0%,#ec4899 100%)!important;color:white!important;border:none!important;border-radius:10px!important;padding:12px 28px!important;font-weight:600!important;box-shadow:0 4px 15px rgba(124,58,237,0.25)!important;}}
.stExpander,div[data-testid="stSidebar"] .stExpander{{border:2px solid var(--border)!important;border-radius:12px!important;background:var(--expander-bg)!important;}}
div[data-testid="stSidebar"] .stExpander summary,div[data-testid="stSidebar"] .stExpander summary *,div[data-testid="stSidebar"] .stExpander svg{{color:var(--text-primary)!important;opacity:1!important;}}
.stDataFrame{{border:1px solid var(--border)!important;border-radius:12px!important;background:var(--bg-main)!important;}}
.stDataFrame [role="gridcell"],.stDataFrame [role="columnheader"]{{font-size:0.78rem!important;line-height:1.2!important;}}
.stDataFrame [role="gridcell"]{{white-space:normal!important;word-break:break-word!important;}}
</style>
"""

theme = THEMES.get(st.session_state.theme, THEMES["light"])
st.markdown(BASE_CSS.format(**theme), unsafe_allow_html=True)

USE_COLUMN_CONFIG = hasattr(st, "column_config")

def show_fig(fig, y_reversed=False, **layout):
    fig.update_layout(template="plotly_white", **layout)
    if y_reversed:
        fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

TEXT_COLS = {"Order ID": "medium", "Ship Mode": "small", "Customer ID": "medium", "Customer Name": "medium", "Segment": "small", "Country": "small", "City": "medium", "State": "medium", "Postal Code": "small", "Region": "small", "Product ID": "medium", "Category": "small", "Sub-Category": "medium", "Product Name": "large"}
DATE_COLS = {"Order Date": "YYYY-MM-DD", "Ship Date": "YYYY-MM-DD"}
NUM_COLS = {"Sales": "$,.2f", "Quantity": ",", "Discount": ".0%", "Profit": "$,.2f"}

def render_filtered_table(data):
    display_df = data.copy()
    for col in ["Order Date", "Ship Date"]:
        if col in display_df.columns:
            display_df[col] = pd.to_datetime(display_df[col], errors="coerce").dt.date
    if "Postal Code" in display_df.columns:
        display_df["Postal Code"] = display_df["Postal Code"].fillna("").astype(str).str.replace(r"\.0$", "", regex=True)
    st.markdown("---")
    st.subheader("Filtered Data")
    st.caption("Scroll to view all columns. Use the search box in the table header to find rows quickly.")
    table_height = min(760, max(360, 40 + len(display_df) * 26))
    if USE_COLUMN_CONFIG:
        cols = display_df.columns
        column_config = {k: st.column_config.TextColumn(k, width=v) for k, v in TEXT_COLS.items() if k in cols}
        column_config.update({k: st.column_config.DateColumn(k, format=v, width="small") for k, v in DATE_COLS.items() if k in cols})
        column_config.update({k: st.column_config.NumberColumn(k, format=v) for k, v in NUM_COLS.items() if k in cols})
        st.dataframe(display_df, use_container_width=True, height=table_height, hide_index=True, column_config=column_config)
    else:
        format_dict = {k: v for k, v in NUM_COLS.items() if k in display_df.columns}
        st.dataframe(display_df.style.format(format_dict), use_container_width=True, height=table_height)
    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered data", csv, file_name="filtered_data.csv", mime="text/csv")

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is None:
        df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")
    else:
        try:
            df = pd.read_csv(uploaded_file, encoding="latin1")
        except Exception:
            st.error("Could not read the uploaded file. Please make sure it's a valid CSV with the same structure as the sample.")
            return pd.DataFrame()
    for col in ["Order Date", "Ship Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    if "Order Date" in df.columns:
        df["Year"] = df["Order Date"].dt.year
        df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    return df

df = load_data(st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"]))

if df.empty:
    st.error("No data available. Please upload a valid CSV or check the sample file.")
    st.stop()

required = ["Sales", "Profit", "Order ID"]
generic_mode = any(c not in df.columns for c in required)

with st.sidebar:
    st.markdown("## 📘 Quick Guide")
    with st.expander("How to use this dashboard", expanded=True):
        st.markdown("1. **Upload your own file** or use the built-in sample dataset.\n2. Choose filters below; you can select multiple values for each attribute.\n3. Pick a view and explore interactive charts. Hover and click for details.\n4. Beginners: start with the **Overview** tab before diving deeper.\n5. If your file doesn’t fit the expected schema, the app will switch to a generic explorer mode with basic summaries and histograms.")
    st.markdown("---")
    st.markdown("#### 🎨 Theme")
    col1, col2 = st.columns(2)
    if col1.button("☀️ Light", use_container_width=True):
        st.session_state.theme = "light"
        st.rerun()
    if col2.button("🌙 Dark", use_container_width=True):
        st.session_state.theme = "dark"
        st.rerun()
    st.markdown("---")
    if generic_mode:
        st.markdown("## 🔧 Generic filters")
        filter_col = st.selectbox("Pick a column to filter (optional)", options=[""] + df.columns.tolist())
        selected_values = st.multiselect(f"Values for {filter_col}", options=sorted(df[filter_col].dropna().unique().tolist())) if filter_col else []
        generic_filter = (filter_col, selected_values)
        view_option = st.radio("📊 Choose a view", options=["Overview"])
    else:
        st.markdown("## 🎛️ Filters")

    def options_for(col, warn_key):
        if col not in df.columns:
            st.warning(f"Dataset does not contain a '{col}' column; {warn_key} filtering will be skipped.")
            return []
        return sorted(df[col].dropna().unique().tolist())

    filter_defs = [
        ("Year", "📅 Year (pick one or more, blank = all)", "year", lambda opts: opts if len(opts) <= 3 else []),
        ("Region", "🌍 Region (pick one or more)", "region", None),
        ("Category", "📦 Category (pick one or more)", "category", None),
        ("Segment", "👥 Segment (pick one or more)", "segment", None),
    ]
    selections = {}
    for col, label, warn_key, default_fn in filter_defs:
        opts = options_for(col, warn_key)
        selections[col] = st.multiselect(label, options=opts, default=(default_fn(opts) if default_fn else []))
    selected_year, selected_region = selections["Year"], selections["Region"]
    selected_category, selected_segment = selections["Category"], selections["Segment"]
    st.markdown("---")

    view_option = st.radio(
        "📊 Choose a view",
        options=["Overview", "Top Products", "Sales Trends", "Profit Analysis", "Regional Breakdown"],
    )

    with st.expander("💬 Feedback", expanded=False):
        with st.form("feedback_form", clear_on_submit=True):
            rating = st.slider("Rate this dashboard", 1, 5, 3)
            comments = st.text_area("Comments (optional)")
            submitted = st.form_submit_button("Submit")
            if submitted:
                try:
                    import datetime
                    fb = pd.DataFrame([{"timestamp": datetime.datetime.now(), "rating": rating, "comments": comments}])
                    fb.to_csv("feedback.csv", mode="a", header=not pd.io.common.file_exists("feedback.csv"), index=False)
                    st.success("Thanks for your feedback!")
                except Exception:
                    st.error("Could not save feedback.")

        admin_pin = st.secrets.get("ADMIN_PIN", "")
        show_admin = st.toggle("Admin View", value=False)
        if show_admin:
            if not admin_pin:
                st.info("Admin view is disabled. Add ADMIN_PIN in Streamlit secrets.")
            else:
                pin_input = st.text_input("Admin PIN (private)", type="password", key="admin_pin_input")
                if pin_input:
                    if pin_input == admin_pin:
                        feedback_path = Path("feedback.csv")
                        if feedback_path.exists():
                            try:
                                fb_df = pd.read_csv(feedback_path)
                                if "timestamp" in fb_df.columns:
                                    fb_df["timestamp"] = pd.to_datetime(fb_df["timestamp"], errors="coerce")
                                    fb_df = fb_df.sort_values("timestamp", ascending=False)
                                st.markdown("##### Recent Feedback")
                                st.dataframe(fb_df.head(50), use_container_width=True, height=220)
                            except Exception:
                                st.info("Feedback saved. Unable to load the table.")
                        else:
                            st.caption("No feedback yet.")
                    else:
                        st.error("Invalid PIN.")
                else:
                    st.caption("Enter the admin PIN to view feedback.")

filtered = df.copy()
if generic_mode:
    col, vals = generic_filter
    if col and vals:
        filtered = filtered[filtered[col].isin(vals)]
else:
    for col_name, selected in [("Year", selected_year), ("Region", selected_region), ("Category", selected_category), ("Segment", selected_segment)]:
        if selected and col_name in filtered.columns:
            filtered = filtered[filtered[col_name].isin(selected)]

if filtered.empty:
    st.warning("No records match the selected filters. Please adjust the year/region/category/segment selections or upload a different dataset.")

if generic_mode:
    st.markdown("### Simple Dataset Summary")
    num_cols = filtered.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = filtered.select_dtypes(exclude=["number"]).columns.tolist()

    def first_col(columns, keywords):
        return next((c for c in columns if any(k in c.lower() for k in keywords)), None)

    def format_number(val):
        if pd.isna(val):
            return "—"
        return f"{val:,.0f}" if abs(val) >= 1000 else f"{val:,.2f}"

    brand_col = first_col(cat_cols, ["brand", "company", "manufacturer", "make"])
    if not brand_col and cat_cols:
        brand_col = next((c for c in cat_cols if filtered[c].nunique() <= 20), cat_cols[0])

    top_brands = []
    if brand_col:
        try:
            top_brands = filtered[brand_col].dropna().astype(str).value_counts().index.tolist()[:3]
        except Exception:
            pass

    ram_col = first_col(num_cols, ["ram", "memory"])
    best_ram = "—"
    if ram_col:
        max_ram = filtered[ram_col].max(skipna=True)
        if not pd.isna(max_ram):
            col_lower = ram_col.lower()
            if "gb" in col_lower:
                best_ram = f"{format_number(max_ram)} GB"
            elif "mb" in col_lower:
                best_ram = f"{format_number(max_ram)} MB"
            elif max_ram <= 256:
                best_ram = f"{format_number(max_ram)} GB"
            else:
                best_ram = format_number(max_ram)

    price_col = first_col(num_cols, ["price", "cost", "amount", "revenue", "sales"])
    avg_price = "—"
    if price_col:
        avg_val = filtered[price_col].mean(skipna=True)
        if not pd.isna(avg_val):
            avg_price = f"${avg_val:,.0f}" if any(k in price_col.lower() for k in ["price", "cost"]) else format_number(avg_val)

    labels = ["Most Selling Brand", "2nd Most Selling", "3rd Most Selling"]
    metric_items = [(labels[i], top_brands[i]) for i in range(min(3, len(top_brands)))]
    if best_ram not in ["", "—", None]:
        metric_items.append(("Best RAM", best_ram))
    if avg_price not in ["", "—", None]:
        metric_items.append(("Average Price", avg_price))

    for col, (label, value) in zip(st.columns(4), metric_items[:4]):
        col.metric(label, value)

    st.markdown("---")
    with st.expander("View sample rows", expanded=False):
        st.dataframe(filtered.head(8), use_container_width=True)
    st.markdown("---")

    palette = ["#FF6B6B", "#4D96FF", "#6BCB77", "#FFD93D", "#9D4EDD", "#FF8FAB", "#06D6A0", "#F72585"]
    if num_cols:
        st.subheader("Numeric distributions")
        sorted_num = sorted(num_cols, key=lambda c: filtered[c].count(), reverse=True)[:3]
        for i, col in enumerate(sorted_num):
            fig = px.histogram(filtered, x=col, nbins=30, title=f"Distribution of {col}", color_discrete_sequence=[palette[i % len(palette)]])
            show_fig(fig)
    else:
        st.info("No numeric columns found to show distributions.")

    if cat_cols:
        st.subheader("Top categories (by frequency)")
        cand = [c for c in cat_cols if filtered[c].nunique() <= 20][:3]
        for col in cand:
            df_top = filtered[col].fillna("(missing)").value_counts().reset_index()
            df_top.columns = [col, "count"]
            fig_bar = px.bar(df_top.head(10), x="count", y=col, orientation="h", title=f"Top values in {col}", color_discrete_sequence=palette)
            show_fig(fig_bar, y_reversed=True)
            fig_pie = px.pie(df_top.head(6), values="count", names=col, title=f"{col} composition (top 6)", color_discrete_sequence=palette)
            show_fig(fig_pie)
    else:
        st.info("No categorical columns found to show category breakdowns.")
    st.stop()

# ======================= OVERVIEW =======================
if view_option == "Overview":
    st.markdown("### Overview")
    if "Sales" not in filtered.columns:
        st.error("Cannot display overview: 'Sales' column missing.")
    else:
        total_sales = filtered["Sales"].sum()
        total_profit = filtered["Profit"].sum() if "Profit" in filtered.columns else 0
        total_orders = filtered["Order ID"].nunique() if "Order ID" in filtered.columns else len(filtered)
        avg_discount = filtered["Discount"].mean() * 100 if "Discount" in filtered.columns else None
        profit_margin = (total_profit / total_sales * 100) if total_sales else 0
    metrics = [
        ("Total Sales", f"${total_sales:,.0f}"),
        ("Total Profit", f"${total_profit:,.0f}"),
        ("Orders", f"{total_orders:,}"),
        ("Profit Margin", f"{profit_margin:.1f}%"),
        ("Avg Discount", "N/A" if avg_discount is None else f"{avg_discount:.1f}%"),
    ]
    for col, (label, value) in zip(st.columns(5), metrics):
        col.metric(label, value)
    st.markdown("####")
    col1, col2 = st.columns(2)
    with col1:
        if "Category" in filtered.columns:
            cat_sales = filtered.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
            fig = px.bar(cat_sales, x="Category", y=["Sales", "Profit"], barmode="group", title="Sales & Profit by Category", color_discrete_sequence=["#667eea", "#764ba2"])
            show_fig(fig, height=400, legend_title_text="")
        else:
            st.info("Category column not available; skipping category breakdown.")
    with col2:
        if "Segment" in filtered.columns:
            seg_sales = filtered.groupby("Segment")["Sales"].sum().reset_index()
            fig = px.pie(seg_sales, values="Sales", names="Segment", title="Sales Distribution by Segment", color_discrete_sequence=["#667eea", "#764ba2", "#f093fb"], hole=0.4)
            show_fig(fig, height=400)
        else:
            st.info("Segment column not available; skipping segment distribution.")
    col3, col4 = st.columns(2)
    with col3:
        if "Region" in filtered.columns:
            region_data = filtered.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
            fig = px.bar(region_data, x="Region", y=["Sales", "Profit"], barmode="group", title="Sales & Profit by Region", color_discrete_sequence=["#667eea", "#764ba2"])
            show_fig(fig, height=400)
        else:
            st.info("Region column not available; skipping regional breakdown.")
    with col4:
        if "Ship Mode" in filtered.columns:
            ship_data = filtered.groupby("Ship Mode")["Sales"].sum().reset_index()
            fig = px.pie(ship_data, values="Sales", names="Ship Mode", title="Sales by Ship Mode", color_discrete_sequence=["#667eea", "#764ba2", "#f093fb", "#a8edea"], hole=0.4)
            show_fig(fig, height=400)
        else:
            st.info("Ship Mode column not available; skipping shipping analysis.")


# ======================= TOP PRODUCTS =======================
elif view_option == "Top Products":
    st.markdown("### Top Products")
    if "Sales" not in filtered.columns:
        st.error("Cannot show top products: 'Sales' column missing.")
    else:
        n = st.slider("Number of products to display", 5, 20, 10)
    col1, col2 = st.columns(2)
    with col1:
        top_sales = filtered.groupby("Product Name")["Sales"].sum().nlargest(n).reset_index()
        fig = px.bar(top_sales, x="Sales", y="Product Name", orientation="h", title=f"Top {n} Products by Sales", color="Sales", color_continuous_scale="Purples")
        show_fig(fig, height=500, y_reversed=True, showlegend=False)
    with col2:
        top_profit = filtered.groupby("Product Name")["Profit"].sum().nlargest(n).reset_index()
        fig = px.bar(top_profit, x="Profit", y="Product Name", orientation="h", title=f"Top {n} Products by Profit", color="Profit", color_continuous_scale="Greens")
        show_fig(fig, height=500, y_reversed=True, showlegend=False)
    st.markdown("---")
    st.subheader("Sub-Category Performance")
    subcat = filtered.groupby("Sub-Category")[["Sales", "Profit"]].sum().reset_index().sort_values("Sales", ascending=False)
    fig = px.bar(subcat, x="Sub-Category", y=["Sales", "Profit"], barmode="group", title="Sales & Profit by Sub-Category", color_discrete_sequence=["#667eea", "#764ba2"])
    show_fig(fig, height=450, xaxis_tickangle=-45)


# ======================= SALES TRENDS =======================
elif view_option == "Sales Trends":
    st.markdown("### Sales Trends")
    if "Order Date" not in filtered.columns or "Sales" not in filtered.columns:
        st.error("Cannot show sales trends: 'Order Date' or 'Sales' column missing.")
    else:
        monthly = filtered.set_index("Order Date").resample("M")[["Sales", "Profit"]].sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly["Order Date"], y=monthly["Sales"],
        mode="lines+markers", name="Sales",
        line=dict(color="#667eea", width=2.5),
        marker=dict(size=5),
    ))
    fig.add_trace(go.Scatter(
        x=monthly["Order Date"], y=monthly["Profit"],
        mode="lines+markers", name="Profit",
        line=dict(color="#764ba2", width=2.5),
        marker=dict(size=5),
    ))
    show_fig(fig, height=450, title="Monthly Sales & Profit Trend", xaxis_title="Date", yaxis_title="Amount ($)")
    col1, col2 = st.columns(2)
    with col1:
        yearly = filtered.set_index("Order Date").resample("Y")[["Sales"]].sum().reset_index()
        yearly["Year"] = yearly["Order Date"].dt.year
        fig = px.bar(yearly, x="Year", y="Sales", title="Yearly Sales", color="Sales", color_continuous_scale="Purples", text_auto=",.0f")
        show_fig(fig, height=400, showlegend=False)
    with col2:
        yearly_p = filtered.set_index("Order Date").resample("Y")[["Profit"]].sum().reset_index()
        yearly_p["Year"] = yearly_p["Order Date"].dt.year
        fig = px.bar(yearly_p, x="Year", y="Profit", title="Yearly Profit", color="Profit", color_continuous_scale="Greens", text_auto=",.0f")
        show_fig(fig, height=400, showlegend=False)
    st.markdown("---")
    st.subheader("Quarterly Breakdown")
    quarterly = filtered.set_index("Order Date").resample("Q")[["Sales", "Profit"]].sum().reset_index()
    quarterly["Quarter"] = quarterly["Order Date"].dt.to_period("Q").astype(str)
    fig = px.bar(quarterly, x="Quarter", y=["Sales", "Profit"], barmode="group", title="Quarterly Sales & Profit", color_discrete_sequence=["#667eea", "#764ba2"])
    show_fig(fig, height=400, xaxis_tickangle=-45)


# ======================= PROFIT ANALYSIS =======================
elif view_option == "Profit Analysis":
    st.markdown("### Profit Analysis")
    if "Profit" not in filtered.columns:
        st.error("Cannot show profit analysis: 'Profit' column missing.")
    else:
        col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(filtered, x="Sales", y="Profit", color="Category", title="Sales vs Profit", color_discrete_sequence=["#667eea", "#764ba2", "#f093fb"], opacity=0.6, hover_data=["Product Name"])
        show_fig(fig, height=450)
    with col2:
        fig = px.scatter(filtered, x="Discount", y="Profit", color="Category", title="Discount vs Profit", color_discrete_sequence=["#667eea", "#764ba2", "#f093fb"], opacity=0.6)
        show_fig(fig, height=450)
    st.markdown("---")
    loss_products = filtered.groupby("Product Name")["Profit"].sum().sort_values().head(10).reset_index()
    fig = px.bar(loss_products, x="Profit", y="Product Name", orientation="h", title="Top 10 Loss-Making Products", color="Profit", color_continuous_scale="Reds_r")
    show_fig(fig, height=450, y_reversed=True, showlegend=False)
    st.markdown("---")
    st.subheader("Profit Margin by Sub-Category")
    subcat_pm = filtered.groupby("Sub-Category")[["Sales", "Profit"]].sum().reset_index()
    subcat_pm["Profit Margin %"] = (subcat_pm["Profit"] / subcat_pm["Sales"] * 100).round(1)
    subcat_pm = subcat_pm.sort_values("Profit Margin %", ascending=True)
    colors = ["#e74c3c" if v < 0 else "#667eea" for v in subcat_pm["Profit Margin %"]]
    fig = go.Figure(go.Bar(x=subcat_pm["Profit Margin %"], y=subcat_pm["Sub-Category"], orientation="h", marker_color=colors, text=subcat_pm["Profit Margin %"].apply(lambda x: f"{x:.1f}%"), textposition="outside"))
    show_fig(fig, height=450, title="Profit Margin % by Sub-Category", xaxis_title="Profit Margin %")


# ======================= REGIONAL BREAKDOWN =======================
elif view_option == "Regional Breakdown":
    st.markdown("### Geography view\nCompare performance across regions, states, and cities. The data table at the bottom gives an exact summary.")
    if "Region" not in filtered.columns or "Sales" not in filtered.columns:
        st.error("Cannot show regional breakdown: required columns missing.")
    else:
        region_summary = filtered.groupby("Region").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"), Quantity=("Quantity", "sum")).reset_index()
    fig = px.bar(region_summary, x="Region", y=["Sales", "Profit"], barmode="group", title="Sales & Profit by Region", color_discrete_sequence=["#667eea", "#764ba2"], text_auto=",.0f")
    show_fig(fig, height=400)
    col1, col2 = st.columns(2)
    for col, title, container in [("State", "Top 10 States by Sales", col1), ("City", "Top 10 Cities by Sales", col2)]:
        with container:
            top = filtered.groupby(col)["Sales"].sum().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(top, x="Sales", y=col, orientation="h", title=title, color="Sales", color_continuous_scale="Purples")
            show_fig(fig, height=450, y_reversed=True, showlegend=False)
    st.markdown("---")
    st.subheader("Regional Details")
    st.dataframe(
        region_summary.style.format({"Sales": "${:,.0f}", "Profit": "${:,.0f}", "Orders": "{:,}", "Quantity": "{:,}"}),
        use_container_width=True,
    )

render_filtered_table(filtered)
