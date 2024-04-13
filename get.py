import pandas as pd
import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
    
def get_data(tickers, start_dt, end_dt):
    load_dotenv()

    alpaca_key = os.getenv("ALPACA_API_KEY")
    alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

    alpaca = tradeapi.REST(
        alpaca_key,
        alpaca_secret_key,
        api_version="v2")

    start_date = pd.Timestamp(str(start_dt), tz="America/New_York").isoformat()
    end_date = pd.Timestamp(str(end_dt), tz="America/New_York").isoformat()

    timeframe = "1Day"

    df_portfolio = alpaca.get_bars(
    tickers,
    timeframe,
    start=start_date,
    end=end_date
    ).df

    return df_portfolio
