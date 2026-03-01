import streamlit as st
import pandas as pd


# ---------- LOAD CSS ----------
def load_css():
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Best Month to Buy Gold", layout="wide")

# ---------- TITLE ----------
st.title("🟢 Best Month to Buy Gold")
st.write("Find the best month to buy gold based on historical average prices")

# ---------- LOAD DATA ----------
df = pd.read_csv("Gold Price.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year
df["Month_Name"] = df["Date"].dt.strftime("%B")

# ---------- YEAR FILTER ----------
selected_year = st.selectbox("Select Year", sorted(df["Year"].unique(), reverse=True))

filtered_df = df[df["Year"] == selected_year]

# ---------- CALCULATE BEST MONTH ----------
monthly_avg = filtered_df.groupby("Month_Name")["Price"].mean().reset_index()

best_row = monthly_avg.loc[monthly_avg["Price"].idxmin()]
best_month = best_row["Month_Name"]
best_price = best_row["Price"]

# ---------- DISPLAY RESULT ----------
st.markdown(
    f"""
    <div style="
        border: 2px solid #facc15;
        border-radius: 12px;
        padding: 25px;
        background: #0e0e12;
        text-align: center;
        margin-top: 30px;
    ">
        <h2 style="color:#facc15;">Best Month to Buy Gold ({selected_year})</h2>
        <h1 style="color:#ffffff;">{best_month}</h1>
        <p style="font-size:18px;">
            Average Price: <strong>₹ {best_price:,.0f}</strong> per 10 grams
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- OPTIONAL TABLE ----------
with st.expander("📊 View Monthly Average Prices"):
    st.dataframe(monthly_avg.sort_values("Price"))

st.sidebar.markdown("---")
st.sidebar.subheader("⬇️ Download Data")

st.sidebar.download_button(
    label="Download Gold Price Data (CSV)",
    data=df.to_csv(index=False),
    file_name="gold_price_data.csv",
    mime="text/csv",
)
