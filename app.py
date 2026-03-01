import streamlit as st
import pandas as pd
import plotly.express as px


def load_css():
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

st.set_page_config(page_title="Indian Gold Price Dashboard", layout="wide")

st.title("📈 Indian Gold Price Trend ")
st.write("Long-term Gold Price Trend Analysis")

# Load data
df = pd.read_csv("Gold Price.csv")

# Date processing
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%B")

# Sidebar
st.sidebar.header("Filters")
view_type = st.sidebar.radio("Select View Type", ["Yearly Trend", "Monthly Trend"])

# ---------------- YEARLY TREND ----------------
if view_type == "Yearly Trend":
    yearly_avg = df.groupby("Year")["Price"].mean().reset_index()

    fig = px.line(
        yearly_avg,
        x="Year",
        y="Price",
        markers=True,
        title="Year-wise Average Gold Price (₹ per 10g)",
        labels={"Price": "Gold Price (₹/10g)"},
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- MONTHLY TREND ----------------
else:
    selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))

    monthly_avg = (
        df[df["Year"] == selected_year]
        .groupby(["Month", "Month_Name"])["Price"]
        .mean()
        .reset_index()
        .sort_values("Month")
    )

    fig = px.line(
        monthly_avg,
        x="Month_Name",
        y="Price",
        markers=True,
        title=f"Monthly Average Gold Price in {selected_year} (₹ per 10g)",
        labels={"Price": "Gold Price (₹/10g)", "Month_Name": "Month"},
    )
    st.plotly_chart(fig, use_container_width=True)
    
# ---------------- DOWNLOAD DATA ----------------
st.sidebar.markdown("---")
st.sidebar.subheader("⬇️ Download Data")

st.sidebar.download_button(
    label="Download Gold Price Data (CSV)",
    data=df.to_csv(index=False),
    file_name="gold_price_data.csv",
    mime="text/csv",
)
