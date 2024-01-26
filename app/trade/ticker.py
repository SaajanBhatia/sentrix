import csv
from typing import List


class Ticker:
    TICKERS_FILEPATH = 'app/trade/markets.csv'

    def __init__(self, name, ticker, type):
        self.name = name
        self.ticker = ticker
        self.type = type


# Function to extract from csv file
def load_tickers_from_csv(file_path: str) -> List[Ticker]:
    tickers: List[Ticker] = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tickers.append(Ticker(
                name=row['name'],
                ticker=row['ticker'],
                type=row['type']
            ))
    return tickers
