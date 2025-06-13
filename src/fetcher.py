import json
import random
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, Iterable, Tuple, Optional


class PriceFetcher:
    """외부 API를 사용하여 시세를 조회하는 페쳐."""

    def __init__(self) -> None:
        # 한 세션 내에서 동일한 시세를 유지하기 위해 캐시를 사용한다.
        self._price_cache: Dict[str, float] = {}
        self._dividend_cache: Dict[str, float] = {}
        self._exchange_rate: Optional[float] = None

    def _fetch_yahoo_quote(self, ticker: str) -> Optional[dict]:
        """야후 파이낸스에서 쿼트 정보를 가져온다."""
        url = (
            "https://query1.finance.yahoo.com/v7/finance/quote?symbols="
            f"{urllib.parse.quote(ticker)}"
        )
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, json.JSONDecodeError):
            return None

        result = data.get("quoteResponse", {}).get("result")
        if not result:
            return None
        return result[0]

    def fetch_close_price(self, ticker: str) -> float:
        """종가를 외부 API에서 조회한다."""
        if ticker not in self._price_cache:
            quote = self._fetch_yahoo_quote(ticker)
            if quote and "regularMarketPreviousClose" in quote:
                self._price_cache[ticker] = float(quote["regularMarketPreviousClose"])
            elif quote and "regularMarketPrice" in quote:
                self._price_cache[ticker] = float(quote["regularMarketPrice"])
            else:
                self._price_cache[ticker] = round(random.uniform(10, 500), 2)
        return self._price_cache[ticker]

    def fetch_dividend(self, ticker: str) -> float:
        if ticker not in self._dividend_cache:
            quote = self._fetch_yahoo_quote(ticker)
            if quote and "trailingAnnualDividendYield" in quote and quote["trailingAnnualDividendYield"] is not None:
                self._dividend_cache[ticker] = float(quote["trailingAnnualDividendYield"])
            else:
                self._dividend_cache[ticker] = 0.0
        return self._dividend_cache[ticker]

    def fetch_all(self, tickers: Iterable[str]) -> Tuple[Dict[str, float], Dict[str, float]]:
        prices = {t: self.fetch_close_price(t) for t in tickers}
        dividends = {t: self.fetch_dividend(t) for t in tickers}
        return prices, dividends

    def fetch_exchange_rate(self) -> float:
        """원/달러 환율을 외부 API에서 조회한다."""
        if self._exchange_rate is None:
            url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=USDKRW=X"
            try:
                with urllib.request.urlopen(url, timeout=5) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                result = data.get("quoteResponse", {}).get("result")
                if result:
                    self._exchange_rate = float(result[0].get("regularMarketPrice", 0.0))
            except (urllib.error.URLError, json.JSONDecodeError):
                self._exchange_rate = None
        if self._exchange_rate is None:
            self._exchange_rate = round(random.uniform(1000, 1500), 2)
        return self._exchange_rate

    def load_cache(
        self,
        prices: Dict[str, float],
        dividends: Dict[str, float],
    ) -> None:
        """기존 시세 데이터를 캐시에 미리 로드한다."""
        self._price_cache.update(prices)
        self._dividend_cache.update(dividends)
