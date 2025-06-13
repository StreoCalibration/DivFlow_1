from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .asset import Asset

@dataclass
class Portfolio:
    assets: Dict[str, Asset] = field(default_factory=dict)

    def add_asset(self, asset: Asset) -> None:
        self.assets[asset.ticker] = asset

    def remove_asset(self, ticker: str) -> None:
        self.assets.pop(ticker, None)

    def get_total_value(self) -> float:
        return sum(a.get_value() for a in self.assets.values())

    def get_allocation_ratios(self) -> Dict[str, float]:
        total = self.get_total_value()
        return {t: a.get_weight_percentage(total) for t, a in self.assets.items()}

    def update_prices(self, prices: Dict[str, float], dividends: Optional[Dict[str, float]] = None) -> None:
        for ticker, price in prices.items():
            if ticker in self.assets:
                self.assets[ticker].close_price = price
        if dividends:
            for ticker, dy in dividends.items():
                if ticker in self.assets:
                    self.assets[ticker].dividend_yield = dy

    def calculate_stats(self) -> Dict[str, float]:
        total_value = self.get_total_value()
        total_gain = sum(a.get_gain() for a in self.assets.values())
        total_dividend = sum(a.get_dividend_amount() for a in self.assets.values())
        return {
            "value": total_value,
            "gain": total_gain,
            "dividend": total_dividend,
        }


class PortfolioApp:
    def __init__(self, portfolio: Portfolio, price_fetcher: "PriceFetcher", storage: "PortfolioStorage"):
        self.portfolio = portfolio
        self.price_fetcher = price_fetcher
        self.storage = storage
        self.ui = None
        self.exchange_rate = 1.0

    def set_ui(self, ui: "MainWindow") -> None:
        self.ui = ui

    def refresh_data(self) -> None:
        tickers = list(self.portfolio.assets.keys())
        prices, dividends = self.price_fetcher.fetch_all(tickers)
        self.exchange_rate = self.price_fetcher.fetch_exchange_rate()
        self.portfolio.update_prices(prices, dividends)
        if self.ui:
            self.ui.update_ui()

    def save_state(self) -> None:
        self.storage.save(self.portfolio)
        self.storage.save_exchange_rate(self.exchange_rate)

    def load_state(self) -> None:
        loaded = self.storage.load()
        if loaded:
            self.portfolio = loaded
            # 기존 저장된 시세 정보를 Fetcher 캐시에 반영한다
            prices = {t: a.close_price for t, a in loaded.assets.items()}
            dividends = {t: a.dividend_yield for t, a in loaded.assets.items()}
            self.price_fetcher.load_cache(prices, dividends)
        rate = self.storage.load_exchange_rate()
        if rate is not None:
            self.exchange_rate = rate
        if self.ui:
            self.ui.update_ui()

    def calculate_rebalancing(self, amount: float) -> Dict[str, int]:
        """입금액(원화)을 사용하여 매수 권장 수량을 계산한다."""
        deposit = amount / self.exchange_rate
        total = self.portfolio.get_total_value() + deposit
        allocations = {}
        for asset in self.portfolio.assets.values():
            desired_value = total * asset.weight
            to_buy_value = max(desired_value - asset.get_value(), 0)
            if asset.close_price > 0:
                allocations[asset.ticker] = int(to_buy_value / asset.close_price)
            else:
                allocations[asset.ticker] = 0
        return allocations
