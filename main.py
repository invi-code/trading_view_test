from fastapi import FastAPI
from tradingview_ta import TA_Handler, Interval
from typing import List, Dict, Any

app = FastAPI()

# Define the list of Nifty 50 stocks
nifty50_symbols = [
    "TATAMOTORS", "RELIANCE", "INFY", "HDFCBANK", "ICICIBANK",
    "SBIN", "TCS", "HINDUNILVR", "KOTAKBANK", "ITC", "LT"
]

@app.get("/stocks/ohlc_data", response_model=List[Dict[str, Any]])
async def fetch_ohlc_data():
    """Fetch OHLC data and percentage change for Nifty 50 stocks."""
    ohlc_data = []

    for symbol in nifty50_symbols:
        analysis = TA_Handler(
            symbol=symbol,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_DAY
        )

        try:
            # Fetch analysis summary
            summary = analysis.get_analysis()

            # Extract OHLC data
            open_price = summary.indicators.get("open")
            close_price = summary.indicators.get("close")

            # Calculate percentage change
            if open_price and close_price:
                percentage_change = round(((close_price - open_price) / open_price) * 100, 2)
            else:
                percentage_change = None  # Handle missing data

            ohlc = {
                "Symbol": symbol,
                "Open": open_price,
                "Close": close_price,
                "Percentage Change (%)": percentage_change
            }
            ohlc_data.append(ohlc)

        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    return ohlc_data

