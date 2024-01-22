from . import SupabaseClient
from .models import RssFeedData
from ..utils import CustomLogger


class FeedsModel(SupabaseClient):
    TABLE_NAME = 'feeds'

    def __init__(self, logger: CustomLogger) -> None:
        super().__init__(logger)

    # Create Row
    def writeRSS(self, row: RssFeedData):
        """Create a new row in the `feed` table with data provided by the `data` """

        data = {
            "rss_id": row.rss_id,
            "headline": row.headline,
            "description": row.description,
            "sentiment": row.sentiment_score,
            "category": row.category,
            "source": row.source,
            "datetime": row.datetime
        }

        try:
            # Perform the insert operation
            data, _count = self.supabase.table(
                FeedsModel.TABLE_NAME).insert(data).execute()

            return data
        except Exception as e:
            # Handle any exceptions
            self.logger.error(f"Error writing to database: {e}")

    def isUniqueRSSID(self, id: str) -> bool:
        """Check if an rss ID already exists in the database"""
        try:
            data, _count = self.supabase.table(FeedsModel.TABLE_NAME).select(
                '*').eq('rss_id', id).execute()
            if (data[-1]):
                return False
            return True
        except Exception as e:
            # Handle any exceptions
            self.logger.error(f"Error identifying unique RSS: {e}")
