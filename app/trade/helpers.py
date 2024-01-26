import yfinance as yf
from datetime import datetime, time
import pytz


def isMarketOpenUS(symbol: str) -> bool:
    """Given a market symbol return if the market is open or not"""
    # Define US Eastern Time Zone
    eastern = pytz.timezone('US/Eastern')

    # Get the current time in UTC
    utc_now = pytz.utc.localize(datetime.utcnow())

    # Convert current time to US Eastern Time Zone
    eastern_now = utc_now.astimezone(eastern)

    # Define the market open and close times
    market_open_time = time(hour=9, minute=30, second=0)
    market_close_time = time(hour=16, minute=0, second=0)

    # Check if the current time is a weekday and within market hours
    if eastern_now.weekday() < 5 and market_open_time <= eastern_now.time() <= market_close_time:
        # Download the most recent data for the symbol to check the last trade time
        data = yf.download(tickers=symbol, period='1d', interval='1m').tail(1)
        if not data.empty:
            last_trade_time = data.index[-1].astimezone(eastern)
            # Assuming if the last trade was within the last 2 minutes, the market is open
            # This is a simplification and might not always be accurate
            if (eastern_now - last_trade_time).total_seconds() < 120:
                return True
    return False
