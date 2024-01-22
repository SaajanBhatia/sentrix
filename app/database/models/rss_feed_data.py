# Model for feed

class RssFeedData:
    def __init__(
            self,
            rss_id: str,
            headline: str,
            description: str,
            sentiment_score: float,
            category: str,
            source: str,
            datetime: str
    ) -> None:
        self.rss_id = rss_id
        self.headline = headline
        self.description = description
        self.sentiment_score = sentiment_score
        self.category = category
        self.source = source
        self.datetime = datetime
