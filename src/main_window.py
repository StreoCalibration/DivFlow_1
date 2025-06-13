import tkinter as tk
from tkinter import ttk, messagebox

from .asset import Asset
from .portfolio import Portfolio, PortfolioApp


class MainWindow(tk.Tk):
    def __init__(self, app: PortfolioApp):
        super().__init__()
        self.app = app
        self.app.set_ui(self)
        self.title("DivFlow")
        self.geometry("700x400")

        self._build_widgets()
        self.update_ui()

    def _build_widgets(self) -> None:
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("Ticker", "Weight", "Shares", "Avg Cost", "Price", "Value")
        self.table = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.table.heading(col, text=col)
        self.table.pack(fill=tk.BOTH, expand=True)

        form = ttk.Frame(frame)
        form.pack(fill=tk.X, pady=5)

        ttk.Label(form, text="Ticker").grid(row=0, column=0)
        ttk.Label(form, text="Weight").grid(row=0, column=1)
        ttk.Label(form, text="Shares").grid(row=0, column=2)
        ttk.Label(form, text="Avg Cost").grid(row=0, column=3)

        self.entry_ticker = ttk.Entry(form, width=10)
        self.entry_weight = ttk.Entry(form, width=7)
        self.entry_shares = ttk.Entry(form, width=7)
        self.entry_cost = ttk.Entry(form, width=7)
        self.entry_ticker.grid(row=1, column=0)
        self.entry_weight.grid(row=1, column=1)
        self.entry_shares.grid(row=1, column=2)
        self.entry_cost.grid(row=1, column=3)

        ttk.Button(form, text="Add", command=self.on_add_asset).grid(row=1, column=4, padx=5)
        ttk.Button(form, text="Refresh", command=self.on_refresh_clicked).grid(row=1, column=5)
        ttk.Button(form, text="Save", command=self.on_save_clicked).grid(row=1, column=6)

        rebalance_frame = ttk.Frame(frame)
        rebalance_frame.pack(fill=tk.X)
        ttk.Label(rebalance_frame, text="Deposit").grid(row=0, column=0)
        self.entry_deposit = ttk.Entry(rebalance_frame, width=10)
        self.entry_deposit.grid(row=0, column=1)
        ttk.Button(rebalance_frame, text="Rebalance", command=self.on_add_fund_clicked).grid(row=0, column=2, padx=5)

    def _clear_table(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)

    def update_ui(self) -> None:
        self._clear_table()
        for asset in self.app.portfolio.assets.values():
            self.table.insert("", tk.END, values=(
                asset.ticker,
                f"{asset.weight*100:.1f}%",
                asset.shares,
                f"{asset.avg_cost:.2f}",
                f"{asset.current_price:.2f}",
                f"{asset.get_value():.2f}",
            ))

    def on_refresh_clicked(self) -> None:
        self.app.refresh_data()

    def on_save_clicked(self) -> None:
        self.app.save_state()
        messagebox.showinfo("Saved", "Portfolio saved")

    def on_add_fund_clicked(self) -> None:
        try:
            amount = float(self.entry_deposit.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return
        allocs = self.app.calculate_rebalancing(amount)
        msg = "\n".join(f"{t}: {n} shares" for t, n in allocs.items())
        messagebox.showinfo("Rebalance", msg)

    def on_add_asset(self) -> None:
        try:
            ticker = self.entry_ticker.get().upper()
            weight = float(self.entry_weight.get()) / 100
            shares = float(self.entry_shares.get())
            cost = float(self.entry_cost.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input")
            return
        asset = Asset(ticker=ticker, weight=weight, shares=shares, avg_cost=cost)
        self.app.portfolio.add_asset(asset)
        self.update_ui()
