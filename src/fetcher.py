import random
from typing import Dict, Iterable, Tuple, Optional


class PriceFetcher:
    """외부 API 대신 임시로 무작위 종가를 반환하는 페쳐."""

    def __init__(self) -> None:
        # 한 세션 내에서 동일한 시세를 유지하기 위해 캐시를 사용한다.
        self._price_cache: Dict[str, float] = {}
        self._dividend_cache: Dict[str, float] = {}
        self._exchange_rate: Optional[float] = None

    def fetch_close_price(self, ticker: str) -> float:
        """어제 종가를 임의의 값으로 반환한다."""
        if ticker not in self._price_cache:
            self._price_cache[ticker] = round(random.uniform(10, 500), 2)
        return self._price_cache[ticker]

    def fetch_dividend(self, ticker: str) -> float:
        if ticker not in self._dividend_cache:
            self._dividend_cache[ticker] = round(random.uniform(0.01, 0.05), 4)
        return self._dividend_cache[ticker]

    def fetch_all(self, tickers: Iterable[str]) -> Tuple[Dict[str, float], Dict[str, float]]:
        prices = {t: self.fetch_close_price(t) for t in tickers}
        dividends = {t: self.fetch_dividend(t) for t in tickers}
        return prices, dividends

    def fetch_exchange_rate(self) -> float:
        """원/달러 환율을 임의의 값으로 반환한다."""
        if self._exchange_rate is None:
            self._exchange_rate = round(random.uniform(1000, 1500), 2)
        return self._exchange_rate
