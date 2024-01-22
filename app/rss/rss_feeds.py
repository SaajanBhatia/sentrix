import csv
from typing import List


class RSS:
    FEEDS_CSV_FILEPATH = 'app/rss/feeds.csv'

    def __init__(self, name: str, source: str, url: str, category: str) -> None:
        self.name = name
        self.source = source
        self.url = url
        self.category = category

    def getUrl(self) -> str:
        return self.url

    def getCategory(self) -> str:
        return self.category

    def getName(self) -> str:
        return self.name


# Function to load RSS feeds from a CSV file
def load_rss_from_csv(file_path: str) -> List[RSS]:
    feeds = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rss_feed = RSS(row['name'], row['source'],
                           row['url'], row['category'])
            feeds.append(rss_feed)
    return feeds
