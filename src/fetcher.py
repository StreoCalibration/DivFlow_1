import random
from typing import Dict, Iterable, Tuple

class PriceFetcher:
    """외부 API 대신 임시로 무작위 값을 반환하는 페쳐."""

    def fetch_price(self, ticker: str) -> float:
        return round(random.uniform(10, 500), 2)

    def fetch_dividend(self, ticker: str) -> float:
        return round(random.uniform(0.01, 0.05), 4)

    def fetch_all(self, tickers: Iterable[str]) -> Tuple[Dict[str, float], Dict[str, float]]:
        prices = {t: self.fetch_price(t) for t in tickers}
        dividends = {t: self.fetch_dividend(t) for t in tickers}
        return prices, dividends
