from .trade import TradesService, isMarketOpenUS
from .rss import RssService
from .utils import CustomLogger

from datetime import datetime


class Factory:
    def __init__(self, rssService: RssService, tradesService: TradesService, logger: CustomLogger):
        self._rss = rssService
        self._trades = tradesService
        self.logger = logger

    def dataCollectionFactory(self):
        """Factory method for data collection"""
        # 1. Check if market is open using any US stock e.g. AAPL ('Apple Co.')
        isMarketOpen = isMarketOpenUS(symbol='AAPL')
        current_date = datetime.utcnow().isoformat()

        if isMarketOpen:
            # 2. Check if RSS feed contains new entries
            count = self._rss.service()

            if count > 0:
                # 3. If so, collect market data and write to database
                self._trades.service()
                self.logger.info(f'Factory Service Complete at {current_date}')
