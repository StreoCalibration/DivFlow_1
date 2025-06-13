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
