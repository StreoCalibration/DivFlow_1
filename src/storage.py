import json
from pathlib import Path
from typing import Optional, Union

from .asset import Asset
from .portfolio import Portfolio


class PortfolioStorage:
    def __init__(
        self,
        path: Union[str, Path] = Path("data") / "portfolio.json",
        exchange_rate_path: Union[str, Path] = Path("data") / "exchange_rate.json",
    ) -> None:
        self.path = Path(path)
        self.exchange_rate_path = Path(exchange_rate_path)
        # Ensure the directory for the storage files exist
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.exchange_rate_path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, portfolio: Portfolio) -> None:
        data = [asset.__dict__ for asset in portfolio.assets.values()]
        with self.path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)

    def save_exchange_rate(self, rate: float) -> None:
        with self.exchange_rate_path.open("w", encoding="utf-8") as fp:
            json.dump({"exchange_rate": rate}, fp, ensure_ascii=False, indent=2)

    def load(self) -> Optional[Portfolio]:
        if not self.path.exists():
            return None
        with self.path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
        portfolio = Portfolio()
        for item in data:
            if "current_price" in item and "close_price" not in item:
                item["close_price"] = item.pop("current_price")
            asset = Asset(**item)
            portfolio.add_asset(asset)
        return portfolio

    def load_exchange_rate(self) -> Optional[float]:
        if not self.exchange_rate_path.exists():
            return None
        with self.exchange_rate_path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
        if isinstance(data, dict):
            value = data.get("exchange_rate")
        else:
            value = data
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
