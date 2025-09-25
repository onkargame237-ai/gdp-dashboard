import yfinance as yf
import pandas as pd
import streamlit as st

# Function to get stock high/low
def stock_high_low(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date)
    print(data)

    df = pd.DataFrame({
        "Date": data.index.date,
        "Stock": symbol,
        "High": data["High"],
        "Low": data["Low"],
        "High+Low": data["High"] + data["Low"]
    })
    return df.reset_index(drop=True)

# Streamlit UI
st.title("📊 Indian Stock High/Low")

# Input fields
symbol = st.text_input("Enter Stock Symbol (e.g. INFY.NS, RELIANCE.NS)", "INFY.NS")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Get Data"):
    try:
        df = stock_high_low(symbol, str(start_date), str(end_date))
        if not df.empty:
            st.write("### Stock Data")
            st.dataframe(df)

            # Optional: Plot high and low
            st.line_chart(df.set_index("Date")[["High", "Low"]])
        else:
            st.warning("No data found for this stock/date range.")
    except Exception as e:
        st.error(f"Error: {e}")
