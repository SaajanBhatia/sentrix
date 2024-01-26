from ..utils import CustomLogger
from ..database import TradesModel, TradeData
from . import Ticker, load_tickers_from_csv

from typing import List
import yfinance as yf
from datetime import datetime


class TradesService:
    def __init__(self, logger: CustomLogger) -> None:
        self.db = TradesModel(logger)
        self.tickersList: List[Ticker] = load_tickers_from_csv(
            Ticker.TICKERS_FILEPATH)
        self.logger = logger

    def getMarketData(self, symbol: str):
        try:
            data = yf.download(symbol, period='1d', interval='1m').tail(1)

            # Access DateTime index value for the last row
            datetime_index_value = data.index[-1]

            # Ensure the DateTime index value is in UTC and remove timezone information for formatting
            datetime_index_value_utc = datetime_index_value.tz_convert(
                'UTC').tz_localize(None)

            # Format the timestamp for PostgreSQL's timestamp with time zone
            datetime_index_value_str = datetime_index_value_utc.strftime(
                '%Y-%m-%d %H:%M:%S+00:00')

            values = {
                "Open": data['Open'].iloc[0],
                "High": data['High'].iloc[0],
                "Low": data['Low'].iloc[0],
                "Close": data['Close'].iloc[0],
                "Datetime": datetime_index_value_str
            }
            return values
        except Exception as e:
            self.logger.error(f"Error getting market data values {e}")
            return None

    def service(self):
        for market in self.tickersList:
            # Try get the market data, if not do not write
            data = self.getMarketData(symbol=market.ticker)
            currentDatetime = datetime.utcnow().isoformat() + 'Z'

            if data:
                tradeData: TradeData = TradeData(
                    symbol=market.ticker,
                    type=market.type,
                    open=data['Open'],
                    close=data['Close'],
                    high=data["High"],
                    low=data['Low'],
                    datetime=data["Datetime"]
                )

                # Write the trade data to database
                self.db.write_trade(row=tradeData)

                self.logger.info(f'RSS Service Complete at {currentDatetime}')
