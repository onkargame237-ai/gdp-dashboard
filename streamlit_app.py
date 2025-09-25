import yfinance as yf
import pandas as pd
import streamlit as st

# Function to get stock high/low
def stock_high_low(symbol, start_date, end_date):
    # Adjust end date: yfinance treats end as exclusive
    end_date_adj = pd.to_datetime(end_date) + pd.Timedelta(days=1)
    
    stock = yf.Ticker(symbol)
    data = stock.history(start=start_date, end=end_date_adj)
    
    if data.empty:
        return pd.DataFrame()  # empty DataFrame if no data

    df = pd.DataFrame({
        "Date": data.index.date,
        "Stock": symbol,
        "High": data["High"],
        "Low": data["Low"],
        "High+Low": data["High"] + data["Low"]
    })
    
    # Add TOTAL row
    total_row = pd.DataFrame({
        "Date": ["TOTAL"],
        "Stock": [symbol],
        "High": [df["High"].sum()],
        "Low": [df["Low"].sum()],
        "High+Low": [df["High+Low"].sum()]
    })
    df = pd.concat([df, total_row], ignore_index=True)
    
    return df.reset_index(drop=True)

# Streamlit UI
st.title("📊 Indian Stock High/Low Viewer")

# Input fields
symbol = st.text_input("Enter Stock Symbol (e.g. INFY.NS, RELIANCE.NS)", "INFY.NS")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# Auto-adjust end date if it's today or in future
if end_date >= pd.Timestamp.today().date():
    end_date = pd.Timestamp.today().date() - pd.Timedelta(days=1)

if st.button("Get Data"):
    try:
        df = stock_high_low(symbol, str(start_date), str(end_date))
        if not df.empty:
            st.write("### Stock Data")
            st.dataframe(df)

            # Plot high and low (exclude TOTAL row)
            st.line_chart(df[df["Date"] != "TOTAL"].set_index("Date")[["High", "Low"]])
        else:
            st.warning("No data found for this stock/date range. Check symbol or try an earlier date.")
    except Exception as e:
        st.error(f"Error: {e}")
