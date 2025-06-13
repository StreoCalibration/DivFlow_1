"""DivFlow 애플리케이션 진입점."""

# Allow running this file directly (e.g. ``python src/__main__.py``)
if __package__ is None:  # pragma: no cover - convenience for manual execution
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    __package__ = "src"

from .asset import Asset
from .fetcher import PriceFetcher
from .portfolio import Portfolio, PortfolioApp
from .storage import PortfolioStorage
from .main_window import MainWindow


def main():
    portfolio = Portfolio()
    fetcher = PriceFetcher()
    storage = PortfolioStorage()
    app = PortfolioApp(portfolio, fetcher, storage)
    app.load_state()

    ui = MainWindow(app)
    ui.mainloop()


if __name__ == "__main__":
    main()
