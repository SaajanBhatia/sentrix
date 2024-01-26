from . import SupabaseClient
from .models import TradeData
from ..utils import CustomLogger


class TradesModel(SupabaseClient):
    TABLE_NAME = 'trades'

    def __init__(self, logger: CustomLogger) -> None:
        super().__init__(logger)

    def write_trade(self, row: TradeData):
        """Write Trade to 'trades' table"""
        data = {
            "datetime": row.datetime,
            "symbol": row.symbol,
            "type": row.type,
            "high": row.high,
            "low": row.low,
            "open": row.open,
            "close": row.close
        }

        try:
            data, _count = self.supabase.table(
                TradesModel.TABLE_NAME
            ).insert(data).execute()

            return data
        except Exception as e:
            self.logger.error(f"Error writing to trades table: {e}")
