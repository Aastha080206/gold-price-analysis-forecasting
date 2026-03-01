import streamlit as st
import pandas as pd
import plotly.express as px


def load_css():
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()
# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Seasonality Analysis", layout="wide")
st.title("🌦️ Gold Price Seasonality Analysis")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("Gold Price.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%B")


# -----------------------------
# Season Mapping
# -----------------------------
def get_season(month):
    if month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:
        return "Winter"


df["Season"] = df["Month"].apply(get_season)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

year_selected = st.sidebar.selectbox(
    "Select Year", sorted(df["Year"].unique(), reverse=True)
)

season_selected = st.sidebar.selectbox("Select Season", ["Summer", "Monsoon", "Winter"])

chart_type = st.sidebar.radio("Select Chart Type", ["Line Chart", "Bar Chart"])

# -----------------------------
# Filter Data
# -----------------------------
filtered_df = df[(df["Year"] == year_selected) & (df["Season"] == season_selected)]

monthly_avg = (
    filtered_df.groupby(["Month", "Month_Name"], as_index=False)["Price"]
    .mean()
    .sort_values("Month")
)

# -----------------------------
# Plot
# -----------------------------
st.subheader(f"{season_selected} Gold Price Trend — {year_selected}")

if chart_type == "Line Chart":
    fig = px.line(
        monthly_avg,
        x="Month_Name",
        y="Price",
        markers=True,
        hover_data={"Price": ":,.0f"},
        title="Seasonal Gold Price Trend",
    )
else:
    fig = px.bar(
        monthly_avg,
        x="Month_Name",
        y="Price",
        hover_data={"Price": ":,.0f"},
        title="Seasonal Gold Price Comparison",
    )

fig.update_layout(
    xaxis_title="Month", yaxis_title="Gold Price (₹ per 10g)", hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Explanation Box (for viva)
# -----------------------------
st.info(
    f"""
📌 **Insight**  
This chart shows how gold prices behave during **{season_selected} season in {year_selected}**.
Hover over the chart to see exact monthly prices.
"""
)
st.sidebar.markdown("---")
st.sidebar.subheader("⬇️ Download Data")

st.sidebar.download_button(
    label="Download Gold Price Data (CSV)",
    data=df.to_csv(index=False),
    file_name="gold_price_data.csv",
    mime="text/csv",
)
