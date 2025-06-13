import tkinter as tk
from tkinter import ttk, messagebox

from .asset import Asset
from .portfolio import Portfolio, PortfolioApp


class EditDialog(tk.Toplevel):
    def __init__(self, parent: tk.Widget, asset: Asset):
        super().__init__(parent)
        self.asset = asset
        self.result = None
        self.title(f"{asset.ticker} 수정")

        ttk.Label(self, text="비중(%)").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(self, text="주수").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self, text="평균 단가").grid(row=2, column=0, padx=5, pady=5)

        self.entry_weight = ttk.Entry(self, width=10)
        self.entry_weight.insert(0, f"{asset.weight*100:.2f}")
        self.entry_weight.grid(row=0, column=1, padx=5, pady=5)

        self.entry_shares = ttk.Entry(self, width=10)
        self.entry_shares.insert(0, str(asset.shares))
        self.entry_shares.grid(row=1, column=1, padx=5, pady=5)

        self.entry_cost = ttk.Entry(self, width=10)
        self.entry_cost.insert(0, str(asset.avg_cost))
        self.entry_cost.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(btn_frame, text="확인", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="취소", command=self.destroy).pack(side=tk.LEFT)

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def on_ok(self) -> None:
        try:
            weight = float(self.entry_weight.get()) / 100
            shares = float(self.entry_shares.get())
            cost = float(self.entry_cost.get())
        except ValueError:
            messagebox.showerror("오류", "값이 잘못되었습니다")
            return
        self.result = weight, shares, cost
        self.destroy()


class MainWindow(tk.Tk):
    def __init__(self, app: PortfolioApp):
        super().__init__()
        self.app = app
        self.app.set_ui(self)
        self.title("DivFlow")
        self.geometry("700x400")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._build_widgets()
        self.update_ui()

    def _build_widgets(self) -> None:
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("티커", "비중", "주수", "평균 단가", "현재가", "평가금액")
        self.table = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.table.heading(col, text=col)
        self.table.pack(fill=tk.BOTH, expand=True)
        self.table.bind("<Double-1>", self.on_edit_asset)

        form = ttk.Frame(frame)
        form.pack(fill=tk.X, pady=5)

        ttk.Label(form, text="티커").grid(row=0, column=0)
        ttk.Label(form, text="비중(%)").grid(row=0, column=1)
        ttk.Label(form, text="주수").grid(row=0, column=2)
        ttk.Label(form, text="평균 단가").grid(row=0, column=3)

        self.entry_ticker = ttk.Entry(form, width=10)
        self.entry_weight = ttk.Entry(form, width=7)
        self.entry_shares = ttk.Entry(form, width=7)
        self.entry_cost = ttk.Entry(form, width=7)
        self.entry_ticker.grid(row=1, column=0)
        self.entry_weight.grid(row=1, column=1)
        self.entry_shares.grid(row=1, column=2)
        self.entry_cost.grid(row=1, column=3)

        ttk.Button(form, text="추가", command=self.on_add_asset).grid(row=1, column=4, padx=5)
        ttk.Button(form, text="삭제", command=self.on_remove_asset).grid(row=1, column=5, padx=5)
        ttk.Button(form, text="갱신", command=self.on_refresh_clicked).grid(row=1, column=6)
        ttk.Button(form, text="저장", command=self.on_save_clicked).grid(row=1, column=7)
        ttk.Button(form, text="불러오기", command=self.on_load_clicked).grid(row=1, column=8)

        rebalance_frame = ttk.Frame(frame)
        rebalance_frame.pack(fill=tk.X)
        ttk.Label(rebalance_frame, text="입금액").grid(row=0, column=0)
        self.entry_deposit = ttk.Entry(rebalance_frame, width=10)
        self.entry_deposit.grid(row=0, column=1)
        ttk.Button(rebalance_frame, text="리밸런스", command=self.on_add_fund_clicked).grid(row=0, column=2, padx=5)

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
        messagebox.showinfo("저장 완료", "포트폴리오가 저장되었습니다")

    def on_add_fund_clicked(self) -> None:
        try:
            amount = float(self.entry_deposit.get())
        except ValueError:
            messagebox.showerror("오류", "금액이 잘못되었습니다")
            return
        allocs = self.app.calculate_rebalancing(amount)
        msg = "\n".join(f"{t}: {n}주" for t, n in allocs.items())
        messagebox.showinfo("리밸런스 결과", msg)

    def on_add_asset(self) -> None:
        try:
            ticker = self.entry_ticker.get().upper()
            weight = float(self.entry_weight.get()) / 100
            shares = float(self.entry_shares.get())
            cost = float(self.entry_cost.get())
        except ValueError:
            messagebox.showerror("오류", "입력 값이 잘못되었습니다")
            return
        asset = Asset(ticker=ticker, weight=weight, shares=shares, avg_cost=cost)
        self.app.portfolio.add_asset(asset)
        self.update_ui()

    def on_edit_asset(self, event) -> None:
        item_id = self.table.identify_row(event.y)
        if not item_id:
            return
        ticker = self.table.item(item_id)["values"][0]
        asset = self.app.portfolio.assets.get(ticker)
        if asset is None:
            return

        dialog = EditDialog(self, asset)
        self.wait_window(dialog)
        if dialog.result:
            weight, shares, cost = dialog.result
            asset.weight = weight
            asset.shares = shares
            asset.avg_cost = cost
            self.update_ui()

    def on_remove_asset(self) -> None:
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("오류", "선택된 자산이 없습니다")
            return
        ticker = self.table.item(selected[0])["values"][0]
        self.app.portfolio.remove_asset(ticker)
        self.update_ui()

    def on_load_clicked(self) -> None:
        self.app.load_state()
        messagebox.showinfo("불러오기 완료", "포트폴리오를 불러왔습니다")

    def on_close(self) -> None:
        self.app.save_state()
        self.destroy()
