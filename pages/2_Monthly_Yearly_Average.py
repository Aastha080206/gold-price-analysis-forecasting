import streamlit as st
import pandas as pd
import plotly.express as px


def load_css():
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


st.set_page_config(page_title="Average Gold Price Analysis", layout="wide")

st.title("📊  Monthly & Yearly Average Gold Price Analysis")

# Load data
df = pd.read_csv("Gold Price.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%B")

# ---------------- YEARLY AVERAGE ----------------
st.subheader("Year-wise Average Gold Price (₹ per 10g)")
yearly_avg = df.groupby("Year")["Price"].mean().reset_index()

fig1 = px.bar(
    yearly_avg,
    x="Year",
    y="Price",
    title="Average Gold Price by Year",
    labels={"Price": "Avg Price (₹/10g)"},
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------- MONTHLY AVERAGE ----------------
st.subheader("Month-wise Average Gold Price (Selected Year)")
selected_year = st.selectbox("Select Year", sorted(df["Year"].unique()))

monthly_avg = (
    df[df["Year"] == selected_year]
    .groupby(["Month", "Month_Name"])["Price"]
    .mean()
    .reset_index()
    .sort_values("Month")
)

fig2 = px.bar(
    monthly_avg,
    x="Month_Name",
    y="Price",
    title=f"Monthly Average Gold Price in {selected_year}",
    labels={"Price": "Avg Price (₹/10g)", "Month_Name": "Month"},
)
st.plotly_chart(fig2, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.subheader("⬇️ Download Data")

st.sidebar.download_button(
    label="Download Gold Price Data (CSV)",
    data=df.to_csv(index=False),
    file_name="gold_price_data.csv",
    mime="text/csv",
)
