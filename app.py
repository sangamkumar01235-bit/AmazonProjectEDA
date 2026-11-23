import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Amazon Analytics Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Amazon-inspired palette
NAVY = "#131921"
DARK = "#232F3E"
ORANGE = "#FF9900"
PALE = "#FFF4E5"

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  html, body, [class*="css"] {{ font-family: Inter, sans-serif; }}
  .stApp {{ background: #F4F6F8; }}
  [data-testid="stSidebar"] {{ background: {NAVY}; }}
  [data-testid="stSidebar"] * {{ color: #FFFFFF !important; }}
  [data-testid="stSidebar"] [data-testid="stFileUploader"] {{ background: #232F3E; border-radius: 10px; padding: 8px; }}
  .amazon-header {{ background: linear-gradient(105deg, {NAVY}, {DARK}); padding: 22px 26px; border-radius: 14px; color: white; margin-bottom: 18px; box-shadow: 0 5px 18px rgba(19,25,33,.12); }}
  .amazon-wordmark {{ font-size: 25px; font-weight: 800; letter-spacing: -1.3px; color: white; line-height: 1; }}
  .amazon-wordmark span {{ color: {ORANGE}; }}
  .amazon-subtitle {{ color: #D5D9D9; font-size: 13px; margin-top: 5px; }}
  .kpi {{ background: white; padding: 17px 18px; border-radius: 12px; border: 1px solid #E6E9ED; box-shadow: 0 2px 8px rgba(0,0,0,.035); min-height: 112px; }}
  .kpi-label {{ color: #667085; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .5px; }}
  .kpi-value {{ color: {NAVY}; font-size: 27px; font-weight: 800; margin-top: 7px; }}
  .kpi-note {{ color: #98A2B3; font-size: 11px; margin-top: 2px; }}
  .section-title {{ color: {NAVY}; font-size: 18px; font-weight: 750; margin: 8px 0 12px 0; }}
  div[data-testid="stMetric"] {{ background: white; border: 1px solid #E6E9ED; padding: 14px; border-radius: 12px; }}
  .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
  .stTabs [data-baseweb="tab"] {{ background: white; border-radius: 8px 8px 0 0; padding: 10px 16px; }}
  .stDownloadButton button {{ background: {ORANGE}; color: {NAVY}; border: 0; font-weight: 700; }}
  .stDownloadButton button:hover {{ background: #F3A847; color: {NAVY}; }}
  .small-muted {{ color: #667085; font-size: 12px; }}
</style>
""", unsafe_allow_html=True)


def clean_number(series: pd.Series, percent=False) -> pd.Series:
    s = series.astype(str).str.strip()
    s = s.str.replace(r"[₹,%]", "", regex=True).str.replace(",", "", regex=False)
    s = s.str.replace(r"[^0-9.\-]", "", regex=True)
    return pd.to_numeric(s, errors="coerce")


def prepare_data(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    for col in ["discounted_price", "actual_price", "discount_percentage", "rating", "rating_count"]:
        if col in df.columns:
            df[col + "_num"] = clean_number(df[col])
    # Accept already-cleaned notebook columns too.
    for col in ["discounted_price_num", "actual_price_num", "discount_pct_num", "rating_num", "rating_count_num"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "discount_pct_num" not in df and "discount_percentage_num" in df:
        df["discount_pct_num"] = df["discount_percentage_num"]
    if "discount_pct_num" not in df and "discount_percentage" in df:
        df["discount_pct_num"] = clean_number(df["discount_percentage"])
    if "rating_num" not in df and "rating" in df:
        df["rating_num"] = clean_number(df["rating"])
    if "discounted_price_num" not in df and "discounted_price" in df:
        df["discounted_price_num"] = clean_number(df["discounted_price"])
    if "actual_price_num" not in df and "actual_price" in df:
        df["actual_price_num"] = clean_number(df["actual_price"])
    if "rating_count_num" not in df and "rating_count" in df:
        df["rating_count_num"] = clean_number(df["rating_count"])
    if "category" not in df:
        df["category"] = "Uncategorized"
    df["category"] = df["category"].fillna("Uncategorized").astype(str)
    if "product_name" not in df:
        df["product_name"] = [f"Product {i+1}" for i in range(len(df))]
    return df


def money(value):
    return "—" if pd.isna(value) else f"₹{value:,.0f}"


def chart_layout(fig, height=360):
    fig.update_layout(
        height=height, margin=dict(l=12, r=12, t=48, b=12),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Inter, sans-serif", color=NAVY),
        title_font=dict(size=15, color=NAVY),
        legend_title_text="",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#EEF0F2", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#EEF0F2", zeroline=False)
    return fig


# Sidebar branding and file input
with st.sidebar:
    st.markdown(f"""
    <div style='padding:8px 2px 18px 2px'>
      <div style='font-size:28px;font-weight:800;letter-spacing:-1.5px;color:white'>a<span style='color:{ORANGE}'>mazon</span></div>
      <div style='height:3px;width:68px;background:{ORANGE};border-radius:4px;margin-top:3px'></div>
      <div style='font-size:11px;color:#D5D9D9;margin-top:9px;letter-spacing:1px'>ANALYTICS WORKSPACE</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### Dataset")
    uploaded = st.file_uploader("Upload Amazon CSV file", type=["csv"], help="Upload the amazon.csv dataset used in your notebook.")
    st.caption("Your notebook references a CSV named amazon.csv. Upload that file here to populate the dashboard.")
    st.markdown("---")
    st.markdown("### Dashboard filters")

# Load uploaded file, or a local amazon.csv if available.
source = uploaded
if source is None and Path("amazon.csv").exists():
    source = Path("amazon.csv")

st.markdown(f"""
<div class="amazon-header">
  <div class="amazon-wordmark">a<span>mazon</span> <span style="color:#D5D9D9;font-size:14px;font-weight:500;letter-spacing:0">| PRODUCT INTELLIGENCE</span></div>
  <div style="font-size:25px;font-weight:800;margin-top:13px">Amazon Analytics Dashboard</div>
  <div class="amazon-subtitle">Explore product pricing, categories, ratings and discount performance</div>
</div>
""", unsafe_allow_html=True)

if source is None:
    st.info("Upload your **amazon.csv** file in the left sidebar to start exploring the dashboard.")
    st.markdown("#### What this dashboard includes")
    c1, c2, c3 = st.columns(3)
    c1.markdown("**📦 Product insights**\n\nProduct counts, category rankings and product-level details.")
    c2.markdown("**💰 Pricing & discounts**\n\nActual price, discounted price and discount distribution.")
    c3.markdown("**⭐ Ratings & reviews**\n\nRating distribution, popular products and correlations.")
    st.stop()

try:
    raw_df = pd.read_csv(source)
    df = prepare_data(raw_df)
except Exception as exc:
    st.error(f"Could not read this CSV file: {exc}")
    st.stop()

# Filters
with st.sidebar:
    categories = sorted(df["category"].dropna().astype(str).unique().tolist())
    selected_categories = st.multiselect("Product category", categories, default=categories)
    if "rating_num" in df.columns:
        valid_ratings = df["rating_num"].dropna()
        if not valid_ratings.empty:
            min_rating, max_rating = float(valid_ratings.min()), float(valid_ratings.max())
            rating_range = st.slider("Rating range", min_value=float(min_rating), max_value=float(max_rating if max_rating > min_rating else min_rating + 0.1), value=(float(min_rating), float(max_rating if max_rating > min_rating else min_rating + 0.1)))
        else:
            rating_range = None
    else:
        rating_range = None
    st.markdown("---")
    st.caption(f"Rows in source file: {len(df):,}")

filtered = df[df["category"].astype(str).isin(selected_categories)].copy()
if rating_range is not None and "rating_num" in filtered:
    filtered = filtered[filtered["rating_num"].between(rating_range[0], rating_range[1], inclusive="both") | filtered["rating_num"].isna()]

# KPIs
n_products = len(filtered)
avg_rating = filtered["rating_num"].mean() if "rating_num" in filtered else float("nan")
avg_discount = filtered["discount_pct_num"].mean() if "discount_pct_num" in filtered else float("nan")
category_count = filtered["category"].nunique()
avg_price = filtered["discounted_price_num"].mean() if "discounted_price_num" in filtered else float("nan")

kpis = st.columns(4)
metrics = [
    ("TOTAL PRODUCTS", f"{n_products:,}", "Products after filters"),
    ("AVERAGE RATING", "—" if pd.isna(avg_rating) else f"{avg_rating:.2f} / 5", "Mean customer rating"),
    ("AVERAGE DISCOUNT", "—" if pd.isna(avg_discount) else f"{avg_discount:.1f}%", "Mean discount percentage"),
    ("PRODUCT CATEGORIES", f"{category_count:,}", "Distinct categories"),
]
for col, (label, value, note) in zip(kpis, metrics):
    col.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
tab_overview, tab_products, tab_pricing, tab_ratings, tab_data = st.tabs(["📊 Overview", "📦 Products", "💰 Pricing & Discounts", "⭐ Ratings", "🗂️ Data Explorer"])

with tab_overview:
    left, right = st.columns([1.1, 1])
    with left:
        st.markdown('<div class="section-title">Top product categories</div>', unsafe_allow_html=True)
        cat_counts = filtered["category"].value_counts().head(10).reset_index()
        cat_counts.columns = ["Category", "Products"]
        if not cat_counts.empty:
            fig = px.bar(cat_counts.sort_values("Products"), x="Products", y="Category", orientation="h", color="Products", color_continuous_scale=["#FFD18A", ORANGE], title="Products by category (top 10)")
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(chart_layout(fig, 390), use_container_width=True)
        else:
            st.warning("No category data for the selected filters.")
    with right:
        st.markdown('<div class="section-title">Average price by category</div>', unsafe_allow_html=True)
        if "discounted_price_num" in filtered:
            price_cat = filtered.groupby("category", as_index=False)["discounted_price_num"].mean().nlargest(10, "discounted_price_num")
            fig = px.bar(price_cat, x="category", y="discounted_price_num", color_discrete_sequence=[ORANGE], title="Average discounted price")
            fig.update_xaxes(tickangle=-35, title="Category")
            fig.update_yaxes(title="Average price (₹)")
            st.plotly_chart(chart_layout(fig, 390), use_container_width=True)
        else:
            st.info("Discounted-price column not found in this file.")
    if "discount_pct_num" in filtered and "rating_num" in filtered:
        st.markdown('<div class="section-title">Discount vs. rating</div>', unsafe_allow_html=True)
        scatter = filtered.dropna(subset=["discount_pct_num", "rating_num"])
        fig = px.scatter(scatter, x="discount_pct_num", y="rating_num", color="category", hover_name="product_name", opacity=.65, title="Do discounts relate to product ratings?")
        fig.update_xaxes(title="Discount (%)")
        fig.update_yaxes(title="Rating (out of 5)")
        st.plotly_chart(chart_layout(fig, 390), use_container_width=True)

with tab_products:
    st.markdown('<div class="section-title">Top 5 highest-discount products</div>', unsafe_allow_html=True)
    if "discount_pct_num" in filtered:
        cols = [c for c in ["product_name", "category", "actual_price", "discounted_price", "discount_percentage", "discount_pct_num"] if c in filtered.columns]
        top_discount = filtered.nlargest(5, "discount_pct_num")[cols]
        st.dataframe(top_discount, use_container_width=True, hide_index=True)
    else:
        st.info("Discount percentage column not found.")
    st.markdown('<div class="section-title">Most-reviewed products with a 5-star rating</div>', unsafe_allow_html=True)
    if "rating_num" in filtered and "rating_count_num" in filtered:
        best = filtered[filtered["rating_num"] == 5.0].nlargest(5, "rating_count_num")
        show_cols = [c for c in ["product_name", "category", "rating_num", "rating_count", "discounted_price"] if c in best.columns]
        st.dataframe(best[show_cols], use_container_width=True, hide_index=True)
    else:
        st.info("Rating and rating-count columns are needed for this table.")

with tab_pricing:
    p1, p2 = st.columns(2)
    with p1:
        st.markdown('<div class="section-title">Actual vs discounted price</div>', unsafe_allow_html=True)
        if {"actual_price_num", "discounted_price_num"}.issubset(filtered.columns):
            price_data = filtered[["actual_price_num", "discounted_price_num"]].rename(columns={"actual_price_num": "Actual price", "discounted_price_num": "Discounted price"}).melt(var_name="Price type", value_name="Price (₹)").dropna()
            fig = px.histogram(price_data, x="Price (₹)", color="Price type", barmode="overlay", opacity=.72, color_discrete_sequence=[DARK, ORANGE], title="Price distribution")
            st.plotly_chart(chart_layout(fig, 360), use_container_width=True)
        else:
            st.info("Actual and discounted price columns are required.")
    with p2:
        st.markdown('<div class="section-title">Discount percentage spread</div>', unsafe_allow_html=True)
        if "discount_pct_num" in filtered:
            fig = px.box(filtered, y="discount_pct_num", points="outliers", color_discrete_sequence=[ORANGE], title="Discount distribution")
            fig.update_yaxes(title="Discount (%)")
            st.plotly_chart(chart_layout(fig, 360), use_container_width=True)
        else:
            st.info("Discount percentage column not found.")
    if "category" in filtered and {"actual_price_num", "discounted_price_num"}.issubset(filtered.columns):
        summary = filtered.groupby("category", as_index=False).agg(average_actual_price=("actual_price_num", "mean"), average_discounted_price=("discounted_price_num", "mean"), products=("product_name", "count")).sort_values("products", ascending=False).head(15)
        st.markdown('<div class="section-title">Price comparison by category</div>', unsafe_allow_html=True)
        st.dataframe(summary.style.format({"average_actual_price": "₹{:,.2f}", "average_discounted_price": "₹{:,.2f}"}), use_container_width=True, hide_index=True)

with tab_ratings:
    r1, r2 = st.columns(2)
    with r1:
        st.markdown('<div class="section-title">Product rating distribution</div>', unsafe_allow_html=True)
        if "rating_num" in filtered:
            fig = px.histogram(filtered.dropna(subset=["rating_num"]), x="rating_num", nbins=20, color_discrete_sequence=[ORANGE], title="Number of products by rating")
            fig.update_xaxes(title="Rating (out of 5)")
            fig.update_yaxes(title="Number of products")
            st.plotly_chart(chart_layout(fig, 360), use_container_width=True)
        else:
            st.info("Rating column not found.")
    with r2:
        st.markdown('<div class="section-title">Price vs rating</div>', unsafe_allow_html=True)
        if {"discounted_price_num", "rating_num"}.issubset(filtered.columns):
            fig = px.scatter(filtered, x="discounted_price_num", y="rating_num", color_discrete_sequence=[DARK], opacity=.6, hover_name="product_name", title="Discounted price and rating")
            fig.update_xaxes(title="Discounted price (₹)")
            fig.update_yaxes(title="Rating (out of 5)")
            st.plotly_chart(chart_layout(fig, 360), use_container_width=True)
        else:
            st.info("Discounted price and rating columns are required.")
    numeric_cols = filtered.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) >= 2:
        st.markdown('<div class="section-title">Correlation heatmap</div>', unsafe_allow_html=True)
        corr = filtered[numeric_cols].corr(numeric_only=True)
        fig = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1, title="Correlation between numeric features")
        st.plotly_chart(chart_layout(fig, 440), use_container_width=True)

with tab_data:
    st.markdown('<div class="section-title">Filtered dataset</div>', unsafe_allow_html=True)
    st.caption(f"Showing {len(filtered):,} rows and {len(filtered.columns):,} columns")
    st.dataframe(filtered, use_container_width=True, height=480)
    st.download_button("⬇ Download filtered data (CSV)", data=filtered.to_csv(index=False).encode("utf-8"), file_name="amazon_filtered_data.csv", mime="text/csv")

st.markdown("---")
st.markdown("<div class='small-muted'>Amazon-inspired student analytics project • Built with Streamlit and Plotly. This is an independent dashboard and is not affiliated with Amazon.</div>", unsafe_allow_html=True)
