import json
from pathlib import Path
from typing import Optional

from .asset import Asset
from .portfolio import Portfolio


class PortfolioStorage:
    def __init__(self, path: str | Path = Path("data") / "portfolio.json") -> None:
        self.path = Path(path)
        # Ensure the directory for the storage file exists
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def save(self, portfolio: Portfolio) -> None:
        data = [asset.__dict__ for asset in portfolio.assets.values()]
        with self.path.open("w", encoding="utf-8") as fp:
            json.dump(data, fp, ensure_ascii=False, indent=2)

    def load(self) -> Optional[Portfolio]:
        if not self.path.exists():
            return None
        with self.path.open("r", encoding="utf-8") as fp:
            data = json.load(fp)
        portfolio = Portfolio()
        for item in data:
            asset = Asset(**item)
            portfolio.add_asset(asset)
        return portfolio
