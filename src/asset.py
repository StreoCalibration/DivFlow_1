from dataclasses import dataclass

@dataclass
class Asset:
    ticker: str
    weight: float
    shares: float
    avg_cost: float
    close_price: float = 0.0
    dividend_yield: float = 0.0

    def get_value(self) -> float:
        return self.shares * self.close_price

    def get_gain(self) -> float:
        return (self.close_price - self.avg_cost) * self.shares

    def get_dividend_amount(self) -> float:
        return self.close_price * self.shares * self.dividend_yield

    def get_weight_percentage(self, total: float) -> float:
        if total == 0:
            return 0.0
        return self.get_value() / total * 100
