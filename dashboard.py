import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# --- Page Config ---
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide",
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Work+Sans:wght@300;400;500;600;700&display=swap');

    :root {
        --brand: #0E7C86;
        --brand-2: #F26B4F;
        --brand-3: #F5C451;
        --ink: #24364B;
        --muted: #5B6B7A;
        --bg: #F7F4EF;
        --panel: #FFFFFF;
        --panel-2: #F0F6F8;
        --border: #E3E9EE;
    }

    html, body, [class*="css"] { font-family: 'Work Sans', sans-serif; }
    .stApp {
        background:
            radial-gradient(1200px 600px at 10% -10%, rgba(14,124,134,0.12), transparent 60%),
            radial-gradient(800px 400px at 90% 0%, rgba(242,107,79,0.12), transparent 55%),
            linear-gradient(180deg, #F7F4EF 0%, #F9FBFD 45%, #FFFFFF 100%);
    }
    .block-container { padding-top: 1.5rem; padding-bottom: 1.5rem; }

    .main-header {
        font-family: 'DM Serif Display', serif;
        font-size: 2.6rem;
        letter-spacing: 0.3px;
        color: var(--ink);
        margin-bottom: 0.25rem;
    }
    .sub-header { font-size: 1rem; color: var(--muted); margin-bottom: 1.4rem; }

    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(14,124,134,0.12), rgba(242,107,79,0.12));
        border: 1px solid var(--border);
        padding: 14px 18px;
        border-radius: 14px;
        box-shadow: 0 8px 18px rgba(36,54,75,0.08);
    }
    [data-testid="stMetric"] [data-testid="stMetricLabel"] {
        color: var(--muted) !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--ink) !important;
        font-size: 1.7rem !important;
        font-weight: 700;
    }
    [data-testid="stMetric"] [data-testid="stMetricDelta"] { color: var(--brand) !important; }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #102B35 0%, #0F1F2A 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    div[data-testid="stSidebar"] * { color: #F5F8FA !important; }
    div[data-testid="stSidebar"] .stSelectbox label { color: #C9D4DB !important; }
    div[data-testid="stSidebar"] .stSelectbox div { border-color: rgba(255,255,255,0.2); }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .block-container { animation: fadeInUp 0.6s ease; }

    div[data-testid="stDataFrame"] {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 0.35rem;
        box-shadow: 0 10px 24px rgba(36,54,75,0.06);
    }
    div[data-testid="stDataFrame"] [role="grid"] {
        border-radius: 12px;
    }
    div[data-testid="stDataFrame"] [role="columnheader"] {
        background: #F4F8FB;
        color: var(--ink);
        font-weight: 600;
    }
    div[data-testid="stDataFrame"] [role="row"] {
        font-size: 0.9rem;
    }

    @media (max-width: 900px) {
        .main-header { font-size: 2.05rem; }
        .sub-header { font-size: 0.95rem; }
    }
</style>
""", unsafe_allow_html=True)

# --- Theme Helpers ---
PRIMARY = "#0E7C86"
SECONDARY = "#F26B4F"
ACCENT = "#F5C451"
INK = "#24364B"
MUTED = "#5B6B7A"

COLOR_SEQ = [PRIMARY, SECONDARY, ACCENT, "#6C8AA6", "#2B2D42", "#8AB17D"]
CONTINUOUS_TEAL = [[0, "#D4F0F2"], [1, PRIMARY]]
CONTINUOUS_CORAL = [[0, "#FCE9E6"], [1, SECONDARY]]
CONTINUOUS_SAGE = [[0, "#E5F2EA"], [1, "#5E8C61"]]

pio.templates["superstore"] = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Work Sans", size=13, color=INK),
        title=dict(x=0.02, xanchor="left", font=dict(family="DM Serif Display", size=20)),
        paper_bgcolor="rgba(255,255,255,0.92)",
        plot_bgcolor="rgba(255,255,255,1)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=20, t=60, b=40),
        colorway=COLOR_SEQ,
    )
)
pio.templates.default = "superstore"

try:
    _ = st.column_config
    USE_COLUMN_CONFIG = True
except Exception:
    USE_COLUMN_CONFIG = False


def apply_chart_style(
    fig,
    height=400,
    showlegend=True,
    xaxis_title=None,
    yaxis_title=None,
    margin=None,
    xaxis_tickformat=None,
    yaxis_tickformat=None,
    xaxis_tickprefix=None,
    yaxis_tickprefix=None,
):
    fig.update_layout(
        height=height,
        showlegend=showlegend,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Work Sans"),
    )
    if margin:
        fig.update_layout(margin=margin)
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(36,54,75,0.08)",
        automargin=True,
        tickformat=xaxis_tickformat,
        tickprefix=xaxis_tickprefix,
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(36,54,75,0.08)",
        automargin=True,
        tickformat=yaxis_tickformat,
        tickprefix=yaxis_tickprefix,
    )
    return fig


def render_filtered_table(data):
    display_df = data.copy()
    display_df['Order Date'] = display_df['Order Date'].dt.date
    display_df['Ship Date'] = display_df['Ship Date'].dt.date

    if 'Postal Code' in display_df.columns:
        display_df['Postal Code'] = (
            display_df['Postal Code']
            .fillna("")
            .astype(str)
            .str.replace(r"\.0$", "", regex=True)
        )

    st.markdown("---")
    st.subheader("Filtered Data")
    st.caption("Scroll to view all columns. Use the search box in the table header to find rows quickly.")
    table_height = min(760, max(360, 40 + (len(display_df) * 26)))

    if USE_COLUMN_CONFIG:
        column_config = {
            "Order ID": st.column_config.TextColumn("Order ID", width="medium"),
            "Order Date": st.column_config.DateColumn("Order Date", format="YYYY-MM-DD", width="small"),
            "Ship Date": st.column_config.DateColumn("Ship Date", format="YYYY-MM-DD", width="small"),
            "Ship Mode": st.column_config.TextColumn("Ship Mode", width="small"),
            "Customer ID": st.column_config.TextColumn("Customer ID", width="medium"),
            "Customer Name": st.column_config.TextColumn("Customer Name", width="medium"),
            "Segment": st.column_config.TextColumn("Segment", width="small"),
            "Country": st.column_config.TextColumn("Country", width="small"),
            "City": st.column_config.TextColumn("City", width="medium"),
            "State": st.column_config.TextColumn("State", width="medium"),
            "Postal Code": st.column_config.TextColumn("Postal Code", width="small"),
            "Region": st.column_config.TextColumn("Region", width="small"),
            "Product ID": st.column_config.TextColumn("Product ID", width="medium"),
            "Category": st.column_config.TextColumn("Category", width="small"),
            "Sub-Category": st.column_config.TextColumn("Sub-Category", width="medium"),
            "Product Name": st.column_config.TextColumn("Product Name", width="large"),
            "Sales": st.column_config.NumberColumn("Sales", format="$,.2f"),
            "Quantity": st.column_config.NumberColumn("Quantity", format=","),
            "Discount": st.column_config.NumberColumn("Discount", format=".0%"),
            "Profit": st.column_config.NumberColumn("Profit", format="$,.2f"),
        }
        column_config = {k: v for k, v in column_config.items() if k in display_df.columns}
        st.dataframe(
            display_df,
            use_container_width=True,
            height=table_height,
            hide_index=True,
            column_config=column_config,
        )
    else:
        format_dict = {}
        for col, fmt in {
            'Sales': '${:,.2f}',
            'Profit': '${:,.2f}',
            'Discount': '{:.0%}',
            'Quantity': '{:,}',
        }.items():
            if col in display_df.columns:
                format_dict[col] = fmt
        st.dataframe(
            display_df.style.format(format_dict),
            use_container_width=True,
            height=table_height,
        )

    csv = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data",
        csv,
        file_name="superstore_filtered.csv",
        mime="text/csv",
    )

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('Sample - Superstore.csv', encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
    return df

df = load_data()

# --- Sidebar Filters ---
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.markdown("---")

    selected_year = st.selectbox(
        "📅 Select Year",
        options=["All"] + sorted(df['Year'].unique().tolist()),
    )

    selected_region = st.selectbox(
        "🌍 Select Region",
        options=["All"] + sorted(df['Region'].unique().tolist()),
    )

    selected_category = st.selectbox(
        "📦 Select Category",
        options=["All"] + sorted(df['Category'].unique().tolist()),
    )

    selected_segment = st.selectbox(
        "👥 Select Segment",
        options=["All"] + sorted(df['Segment'].unique().tolist()),
    )

    st.markdown("---")

    view_option = st.selectbox(
        "📊 Dashboard View",
        options=[
            "Overview",
            "Top Products",
            "Sales Trends",
            "Profit Analysis",
            "Regional Breakdown",
        ],
    )

# --- Apply Filters ---
filtered = df.copy()
if selected_year != "All":
    filtered = filtered[filtered['Year'] == selected_year]
if selected_region != "All":
    filtered = filtered[filtered['Region'] == selected_region]
if selected_category != "All":
    filtered = filtered[filtered['Category'] == selected_category]
if selected_segment != "All":
    filtered = filtered[filtered['Segment'] == selected_segment]

# --- Header ---
st.markdown('<div class="main-header">Superstore Sales Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive analytics for sales, profit & product performance</div>', unsafe_allow_html=True)
st.caption(
    f"Filters: Year={selected_year} | Region={selected_region} | "
    f"Category={selected_category} | Segment={selected_segment} | "
    f"Records: {len(filtered):,}"
)

if filtered.empty:
    st.warning("No data matches the current filters. Adjust the filters to view results.")
    st.stop()


# ======================= OVERVIEW =======================
if view_option == "Overview":
    total_sales = filtered['Sales'].sum()
    total_profit = filtered['Profit'].sum()
    total_orders = filtered['Order ID'].nunique()
    avg_discount = filtered['Discount'].mean() * 100
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Sales", f"${total_sales:,.0f}")
    c2.metric("Total Profit", f"${total_profit:,.0f}")
    c3.metric("Orders", f"{total_orders:,}")
    c4.metric("Profit Margin", f"{profit_margin:.1f}%")
    c5.metric("Avg Discount", f"{avg_discount:.1f}%")

    st.markdown("####")

    col1, col2 = st.columns(2)

    with col1:
        cat_sales = filtered.groupby('Category')[['Sales', 'Profit']].sum().reset_index()
        fig = px.bar(
            cat_sales, x='Category', y=['Sales', 'Profit'],
            barmode='group', title='Sales & Profit by Category',
            color_discrete_sequence=[PRIMARY, SECONDARY],
        )
        fig.update_layout(legend_title_text='')
        apply_chart_style(fig, height=420)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        seg_sales = filtered.groupby('Segment')['Sales'].sum().reset_index()
        fig = px.pie(
            seg_sales, values='Sales', names='Segment',
            title='Sales Distribution by Segment',
            color_discrete_sequence=COLOR_SEQ,
            hole=0.45,
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        apply_chart_style(fig, height=420, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        region_data = filtered.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
        fig = px.bar(
            region_data, x='Region', y=['Sales', 'Profit'],
            barmode='group', title='Sales & Profit by Region',
            color_discrete_sequence=[PRIMARY, SECONDARY],
        )
        apply_chart_style(fig, height=420)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        ship_data = filtered.groupby('Ship Mode')['Sales'].sum().reset_index()
        fig = px.pie(
            ship_data, values='Sales', names='Ship Mode',
            title='Sales by Ship Mode',
            color_discrete_sequence=COLOR_SEQ,
            hole=0.45,
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        apply_chart_style(fig, height=420, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


# ======================= TOP PRODUCTS =======================
elif view_option == "Top Products":
    n = st.slider("Number of products to display", 5, 20, 10)

    col1, col2 = st.columns(2)

    with col1:
        top_sales = (
            filtered.groupby('Product Name')['Sales'].sum()
            .sort_values(ascending=False).head(n).reset_index()
        )
        fig = px.bar(
            top_sales, x='Sales', y='Product Name',
            orientation='h', title=f'Top {n} Products by Sales',
            color='Sales', color_continuous_scale=CONTINUOUS_TEAL, text_auto='.2s',
        )
        fig.update_layout(yaxis={'autorange': 'reversed'})
        apply_chart_style(fig, height=520, showlegend=False, margin=dict(l=190, r=20, t=60, b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        top_profit = (
            filtered.groupby('Product Name')['Profit'].sum()
            .sort_values(ascending=False).head(n).reset_index()
        )
        fig = px.bar(
            top_profit, x='Profit', y='Product Name',
            orientation='h', title=f'Top {n} Products by Profit',
            color='Profit', color_continuous_scale=CONTINUOUS_SAGE, text_auto='.2s',
        )
        fig.update_layout(yaxis={'autorange': 'reversed'})
        apply_chart_style(fig, height=520, showlegend=False, margin=dict(l=190, r=20, t=60, b=40))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Sub-Category Performance")

    subcat = filtered.groupby('Sub-Category')[['Sales', 'Profit']].sum().reset_index()
    subcat = subcat.sort_values('Sales', ascending=False)
    fig = px.bar(
        subcat, x='Sub-Category', y=['Sales', 'Profit'],
        barmode='group', title='Sales & Profit by Sub-Category',
        color_discrete_sequence=[PRIMARY, SECONDARY],
    )
    fig.update_layout(xaxis_tickangle=-30)
    apply_chart_style(fig, height=460)
    st.plotly_chart(fig, use_container_width=True)


# ======================= SALES TRENDS =======================
elif view_option == "Sales Trends":
    monthly = filtered.set_index('Order Date').resample('M')[['Sales', 'Profit']].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly['Order Date'], y=monthly['Sales'],
        mode='lines+markers', name='Sales',
        line=dict(color=PRIMARY, width=2.5),
        marker=dict(size=5),
    ))
    fig.add_trace(go.Scatter(
        x=monthly['Order Date'], y=monthly['Profit'],
        mode='lines+markers', name='Profit',
        line=dict(color=SECONDARY, width=2.5),
        marker=dict(size=5),
    ))
    fig.update_layout(title='Monthly Sales & Profit Trend')
    fig.update_xaxes(tickformat="%b %Y")
    apply_chart_style(fig, height=450, xaxis_title='Date', yaxis_title='Amount ($)')
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        yearly = filtered.set_index('Order Date').resample('Y')[['Sales']].sum().reset_index()
        yearly['Year'] = yearly['Order Date'].dt.year
        fig = px.bar(
            yearly, x='Year', y='Sales', title='Yearly Sales',
            color='Sales', color_continuous_scale=CONTINUOUS_TEAL, text_auto=',.0f',
        )
        apply_chart_style(fig, height=400, showlegend=False, xaxis_title='Year', yaxis_title='Sales ($)')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        yearly_p = filtered.set_index('Order Date').resample('Y')[['Profit']].sum().reset_index()
        yearly_p['Year'] = yearly_p['Order Date'].dt.year
        fig = px.bar(
            yearly_p, x='Year', y='Profit', title='Yearly Profit',
            color='Profit', color_continuous_scale=CONTINUOUS_SAGE, text_auto=',.0f',
        )
        apply_chart_style(fig, height=400, showlegend=False, xaxis_title='Year', yaxis_title='Profit ($)')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Quarterly Breakdown")
    quarterly = filtered.set_index('Order Date').resample('Q')[['Sales', 'Profit']].sum().reset_index()
    quarterly['Quarter'] = quarterly['Order Date'].dt.to_period('Q').astype(str)
    fig = px.bar(
        quarterly, x='Quarter', y=['Sales', 'Profit'],
        barmode='group', title='Quarterly Sales & Profit',
        color_discrete_sequence=[PRIMARY, SECONDARY],
        text_auto='.2s',
    )
    fig.update_layout(xaxis_tickangle=-30)
    apply_chart_style(fig, height=420)
    st.plotly_chart(fig, use_container_width=True)


# ======================= PROFIT ANALYSIS =======================
elif view_option == "Profit Analysis":
    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(
            filtered, x='Sales', y='Profit', color='Category',
            title='Sales vs Profit',
            color_discrete_sequence=COLOR_SEQ,
            opacity=0.6, hover_data=['Product Name'],
        )
        apply_chart_style(fig, height=450)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            filtered, x='Discount', y='Profit', color='Category',
            title='Discount vs Profit',
            color_discrete_sequence=COLOR_SEQ,
            opacity=0.6,
        )
        apply_chart_style(fig, height=450)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    loss_products = (
        filtered.groupby('Product Name')['Profit'].sum()
        .sort_values().head(10).reset_index()
    )
    fig = px.bar(
        loss_products, x='Profit', y='Product Name',
        orientation='h', title='Top 10 Loss-Making Products',
        color='Profit', color_continuous_scale=CONTINUOUS_CORAL, text_auto='.2s',
    )
    fig.update_layout(yaxis={'autorange': 'reversed'})
    apply_chart_style(fig, height=460, showlegend=False, margin=dict(l=200, r=20, t=60, b=40))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Profit Margin by Sub-Category")
    subcat_pm = filtered.groupby('Sub-Category')[['Sales', 'Profit']].sum().reset_index()
    subcat_pm['Profit Margin %'] = (subcat_pm['Profit'] / subcat_pm['Sales'] * 100).round(1)
    subcat_pm = subcat_pm.sort_values('Profit Margin %', ascending=True)
    colors = ['#D1495B' if v < 0 else PRIMARY for v in subcat_pm['Profit Margin %']]
    fig = go.Figure(go.Bar(
        x=subcat_pm['Profit Margin %'], y=subcat_pm['Sub-Category'],
        orientation='h', marker_color=colors,
        text=subcat_pm['Profit Margin %'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
    ))
    fig.update_layout(title='Profit Margin % by Sub-Category')
    apply_chart_style(fig, height=460, xaxis_title='Profit Margin %', margin=dict(l=200, r=20, t=60, b=40))
    st.plotly_chart(fig, use_container_width=True)


# ======================= REGIONAL BREAKDOWN =======================
elif view_option == "Regional Breakdown":
    region_summary = filtered.groupby('Region').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Quantity=('Quantity', 'sum'),
    ).reset_index()

    fig = px.bar(
        region_summary, x='Region', y=['Sales', 'Profit'],
        barmode='group', title='Sales & Profit by Region',
        color_discrete_sequence=[PRIMARY, SECONDARY],
        text_auto=',.0f',
    )
    apply_chart_style(fig, height=420)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        state_sales = filtered.groupby('State')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(
            state_sales, x='Sales', y='State',
            orientation='h', title='Top 10 States by Sales',
            color='Sales', color_continuous_scale=CONTINUOUS_TEAL, text_auto='.2s',
        )
        fig.update_layout(yaxis={'autorange': 'reversed'})
        apply_chart_style(fig, height=460, showlegend=False, margin=dict(l=160, r=20, t=60, b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        city_sales = filtered.groupby('City')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(
            city_sales, x='Sales', y='City',
            orientation='h', title='Top 10 Cities by Sales',
            color='Sales', color_continuous_scale=CONTINUOUS_TEAL, text_auto='.2s',
        )
        fig.update_layout(yaxis={'autorange': 'reversed'})
        apply_chart_style(fig, height=460, showlegend=False, margin=dict(l=160, r=20, t=60, b=40))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Regional Details")
    if USE_COLUMN_CONFIG:
        st.dataframe(
            region_summary,
            use_container_width=True,
            height=280,
            hide_index=True,
            column_config={
                "Sales": st.column_config.NumberColumn("Sales", format="$,.0f"),
                "Profit": st.column_config.NumberColumn("Profit", format="$,.0f"),
                "Orders": st.column_config.NumberColumn("Orders", format=","),
                "Quantity": st.column_config.NumberColumn("Quantity", format=","),
            },
        )
    else:
        st.dataframe(
            region_summary.style.format({'Sales': '${:,.0f}', 'Profit': '${:,.0f}', 'Orders': '{:,}', 'Quantity': '{:,}'}),
            use_container_width=True,
            height=280,
        )

render_filtered_table(filtered)
