import streamlit as st
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX



def load_css():
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()


# ---------------- Page Config ----------------
st.set_page_config(page_title="Gold Price Forecasting", layout="centered")
st.title("🔮 Gold Price Forecasting ")
st.write("Predict future gold prices based on historical trends")

# ---------------- Load Data ----------------
df = pd.read_csv("Gold Price.csv")

df["Date"] = pd.to_datetime(df["Date"])
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

df = df.sort_values("Date")
df = df.set_index("Date")

# ---------------- Monthly Resample ----------------
monthly_price = df["Price"].resample("ME").mean()

# Forward fill missing values
monthly_price = monthly_price.ffill()

# ---------------- Train Model ----------------
model = SARIMAX(
    monthly_price,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 12),
    enforce_stationarity=False,
    enforce_invertibility=False,
)

results = model.fit(disp=False)

# ---------------- UI Input ----------------
st.subheader("📅 Select a future date")
future_date = st.date_input(
    "Choose a future date", min_value=monthly_price.index.max().date()
)

# ---------------- Predict Button ----------------
if st.button("🔮 Predict Gold Price"):
    future_date = pd.to_datetime(future_date)

    months_ahead = (future_date.year - monthly_price.index[-1].year) * 12 + (
        future_date.month - monthly_price.index[-1].month
    )

    if months_ahead <= 0:
        st.warning("Please select a future date.")
    else:
        forecast = results.forecast(steps=months_ahead)
        predicted_price = forecast.iloc[-1]

        st.success(
            f"💰 **Predicted Gold Price on {future_date.strftime('%B %Y')}**\n\n"
            f"### ₹ {predicted_price:,.0f} per 10 grams"
        )

        with st.expander("📘 How this prediction works"):
            st.write(
                """
            • Uses **monthly gold price trends**  
            • SARIMAX captures **trend + seasonality**  
            • Prediction changes as date changes  
            • Prices shown are **₹ per 10 grams**
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
