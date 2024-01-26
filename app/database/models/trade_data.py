# Model for trades

class TradeData:
    def __init__(
            self,
            symbol: str,
            type: str,
            open: float,
            high: float,
            low: float,
            close: float,
            datetime: str
    ) -> None:
        self.symbol = symbol
        self.type = type
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.datetime = datetime
