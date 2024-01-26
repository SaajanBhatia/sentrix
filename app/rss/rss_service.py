from ..database import FeedsModel, RssFeedData
from . import RSS, load_rss_from_csv
from ..utils import CustomLogger

from typing import List
import feedparser
from datetime import datetime


class RssService:
    def __init__(self, logger: CustomLogger):
        self.db = FeedsModel(logger)
        self.rssList: List[RSS] = load_rss_from_csv(RSS.FEEDS_CSV_FILEPATH)
        self.logger = logger

    def get_attribute(self, entry, attr, default=""):
        """ Safely get an attribute from an RSS entry """
        return getattr(entry, attr, default)

    @staticmethod
    def formatDateObj(published_parsed):
        # Convert struct_time to datetime object
        dt = datetime(*published_parsed[:6])

        dt_string = dt.isoformat() + "Z"  # Appending 'Z' to indicate UTC time zone
        return dt_string

    def getEntryDate(self, entry):
        try:
            dt = RssService.formatDateObj(entry.published_parsed)
        except KeyError:  # If unable to process the date use todays date
            self.logger.info(
                'Could not get datetime from entry, using current UTC')
            dt = datetime.utcnow().isoformat() + 'Z'

        return dt

    def _writeToDB(self, rssData: RssFeedData):
        """Write to DB if the RSS ID doesn't exist"""
        try:
            unique = self.db.isUniqueRSSID(id=rssData.rss_id)
            if unique:
                # Write to db
                self.db.writeRSS(rssData)
                self.logger.info('Entry written to database')
                return True
        except Exception as e:
            self.logger.error(f"Error writing to DB: {e}")

        return False

    def service(self):
        writtenCount = 0
        for rss in self.rssList:
            try:
                feed = feedparser.parse(rss.getUrl())
                for entry in feed.entries:

                    # Create RSS Object with safe attribute access
                    rssFeedData: RssFeedData = RssFeedData(
                        rss_id=entry.id,
                        headline=entry.title,
                        description=self.get_attribute(entry, 'summary'),
                        sentiment_score=0.0,
                        category=self.get_attribute(entry, 'metadata_type'),
                        datetime=self.getEntryDate(entry),
                        source=entry.link
                    )

                    recorded = self._writeToDB(rssFeedData)
                    if recorded:
                        writtenCount += 1

            except Exception as e:
                self.logger.error(f"Error processing RSS feed: {e}")

        current_date = datetime.utcnow().isoformat()
        self.logger.info(f'RSS Service Complete at {current_date}')

        return writtenCount
