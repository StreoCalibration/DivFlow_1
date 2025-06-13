import time
from typing import Dict, Iterable, Tuple, Optional

import yfinance as yf


class PriceFetcher:
    """외부 API를 사용하여 시세를 조회하는 페쳐."""

    def __init__(self) -> None:
        # 한 세션 내에서 동일한 시세를 유지하기 위해 캐시를 사용한다.
        self._price_cache: Dict[str, float] = {}
        self._price_timestamp: Dict[str, float] = {}
        self._dividend_cache: Dict[str, float] = {}
        self._exchange_rate: Optional[float] = None
        self._rate_timestamp: float = 0.0

    def _fetch_yahoo_info(self, ticker: str) -> Optional[dict]:
        """yfinance 패키지를 사용해 티커 정보를 가져온다."""
        try:
            return yf.Ticker(ticker).info
        except Exception as e:
            print(f"yfinance 조회 실패({ticker}): {e}")
            return None

    def fetch_close_price(self, ticker: str) -> float:
        """종가를 외부 API에서 조회한다."""
        now = time.time()
        if (
            ticker not in self._price_cache
            or now - self._price_timestamp.get(ticker, 0) > 3600
        ):
            info = self._fetch_yahoo_info(ticker)
            price = None
            if info and "regularMarketPreviousClose" in info:
                price = info["regularMarketPreviousClose"]
            if price is None and info and "regularMarketPrice" in info:
                price = info["regularMarketPrice"]
            if price is not None:
                self._price_cache[ticker] = float(price)
            else:
                print(f"시세 조회 실패({ticker})")
                self._price_cache[ticker] = 0.0
            self._price_timestamp[ticker] = now
        return self._price_cache[ticker]

    def fetch_dividend(self, ticker: str) -> float:
        if ticker not in self._dividend_cache:
            info = self._fetch_yahoo_info(ticker)
            if info and info.get("trailingAnnualDividendYield") is not None:
                self._dividend_cache[ticker] = float(info["trailingAnnualDividendYield"])
            else:
                print(f"배당 수익률 조회 실패({ticker})")
                self._dividend_cache[ticker] = 0.0
        return self._dividend_cache[ticker]

    def fetch_all(self, tickers: Iterable[str]) -> Tuple[Dict[str, float], Dict[str, float]]:
        prices = {t: self.fetch_close_price(t) for t in tickers}
        dividends = {t: self.fetch_dividend(t) for t in tickers}
        return prices, dividends

    def fetch_exchange_rate(self) -> float:
        """원/달러 환율을 외부 API에서 조회한다."""
        now = time.time()
        if self._exchange_rate is None or now - self._rate_timestamp > 3600:
            try:
                hist = yf.Ticker("USDKRW=X").history(period="1d")
                if not hist.empty:
                    self._exchange_rate = float(hist["Close"].iloc[-1])
            except Exception as e:
                print(f"환율 조회 실패: {e}")
                self._exchange_rate = 0.0
            self._rate_timestamp = now
        if self._exchange_rate is None:
            print("환율 조회 실패")
            self._exchange_rate = 0.0
        return self._exchange_rate

    def load_cache(
        self,
        prices: Dict[str, float],
        dividends: Dict[str, float],
    ) -> None:
        """기존 시세 데이터를 캐시에 미리 로드한다."""
        self._price_cache.update(prices)
        self._dividend_cache.update(dividends)
