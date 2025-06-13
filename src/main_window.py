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

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.editing_ticker = None
        self._build_widgets()
        self.update_ui()

    def _build_widgets(self) -> None:
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = (
            "티커",
            "비중",
            "주수",
            "평균 단가",
            "전일종가(외화)",
            "전일종가(원화)",
            "평가금액(외화)",
            "평가금액(원화)",
        )
        self.table = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            # 모든 헤더와 셀을 우측 정렬한다
            self.table.heading(col, text=col, anchor=tk.E)
            # 컬럼을 창 크기에 맞춰 늘어나도록 설정하고 우측 정렬
            self.table.column(col, stretch=True, anchor=tk.E)
        self.table.pack(fill=tk.BOTH, expand=True)
        self.table.bind("<Double-1>", self.on_edit_asset)
        # 창 크기가 변할 때 컬럼 너비를 자동 조절
        self.table.bind("<Configure>", self._on_table_configure)

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

        # 버튼 전용 프레임을 만들어 입금액 입력 영역과 티커 입력 영역 사이에 배치한다
        button_row = ttk.Frame(frame)
        button_row.pack(fill=tk.X, pady=5)

        self.btn_add = ttk.Button(button_row, text="추가", command=self.on_add_or_update)
        self.btn_add.pack(side=tk.LEFT, padx=5)

        self.btn_cancel = ttk.Button(button_row, text="취소", command=self.on_cancel_edit)
        self.btn_cancel.pack(side=tk.LEFT, padx=5)
        # 편집 모드가 아닐 때는 버튼을 숨긴다
        self.btn_cancel.pack_forget()

        ttk.Button(button_row, text="삭제", command=self.on_remove_asset).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_row, text="갱신", command=self.on_refresh_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_row, text="저장", command=self.on_save_clicked).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_row, text="불러오기", command=self.on_load_clicked).pack(side=tk.LEFT, padx=5)

        rebalance_frame = ttk.Frame(frame)
        rebalance_frame.pack(fill=tk.X)
        ttk.Label(rebalance_frame, text="입금액").grid(row=0, column=0)
        self.entry_deposit = ttk.Entry(rebalance_frame, width=10)
        self.entry_deposit.grid(row=0, column=1)
        ttk.Button(rebalance_frame, text="리밸런스", command=self.on_add_fund_clicked).grid(row=0, column=2, padx=5)

    def _clear_table(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)

    def _clear_entries(self) -> None:
        """모든 입력 필드를 초기화한다."""
        for entry in (
            self.entry_ticker,
            self.entry_weight,
            self.entry_shares,
            self.entry_cost,
        ):
            entry.delete(0, tk.END)

    def update_ui(self) -> None:
        self._clear_table()
        rate = self.app.exchange_rate
        for asset in self.app.portfolio.assets.values():
            price = asset.close_price
            value = asset.get_value()
            self.table.insert(
                "",
                tk.END,
                values=(
                    asset.ticker,
                    f"{asset.weight*100:.1f}%",
                    asset.shares,
                    f"{asset.avg_cost:,.2f}",
                    f"{price:,.2f}",
                    f"{price*rate:,.0f}",
                    f"{value:,.2f}",
                    f"{value*rate:,.0f}",
                ),
            )

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

    def on_add_or_update(self) -> None:
        try:
            ticker = self.entry_ticker.get().upper()
            weight = float(self.entry_weight.get()) / 100
            shares = float(self.entry_shares.get())
            cost = float(self.entry_cost.get())
        except ValueError:
            messagebox.showerror("오류", "입력 값이 잘못되었습니다")
            return

        if self.editing_ticker:
            asset = self.app.portfolio.assets.get(self.editing_ticker)
            if not asset:
                messagebox.showerror("오류", "수정할 자산을 찾을 수 없습니다")
                return
            asset.weight = weight
            asset.shares = shares
            asset.avg_cost = cost
            if ticker != self.editing_ticker:
                self.app.portfolio.remove_asset(self.editing_ticker)
                asset.ticker = ticker
                self.app.portfolio.add_asset(asset)
            self.editing_ticker = None
            self.entry_ticker.config(state="normal")
            self.btn_add.config(text="추가")
            self.btn_cancel.grid_remove()
        else:
            asset = Asset(ticker=ticker, weight=weight, shares=shares, avg_cost=cost)
            self.app.portfolio.add_asset(asset)

        self._clear_entries()
        self.update_ui()

    def on_cancel_edit(self) -> None:
        """편집 모드를 취소하고 입력 필드를 초기화한다."""
        self.editing_ticker = None
        self.entry_ticker.config(state="normal")
        self.btn_add.config(text="추가")
        self.btn_cancel.grid_remove()
        self._clear_entries()

    def on_edit_asset(self, event) -> None:
        item_id = self.table.identify_row(event.y)
        if not item_id:
            return
        ticker = self.table.item(item_id)["values"][0]
        asset = self.app.portfolio.assets.get(ticker)
        if asset is None:
            return

        self.editing_ticker = ticker
        self.entry_ticker.delete(0, tk.END)
        self.entry_ticker.insert(0, asset.ticker)
        self.entry_ticker.config(state="disabled")
        self.entry_weight.delete(0, tk.END)
        self.entry_weight.insert(0, f"{asset.weight*100:.2f}")
        self.entry_shares.delete(0, tk.END)
        self.entry_shares.insert(0, str(asset.shares))
        self.entry_cost.delete(0, tk.END)
        self.entry_cost.insert(0, str(asset.avg_cost))
        self.btn_add.config(text="수정")
        self.btn_cancel.grid()

    def on_remove_asset(self) -> None:
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("오류", "선택된 자산이 없습니다")
            return
        ticker = self.table.item(selected[0])["values"][0]
        self.app.portfolio.remove_asset(ticker)
        if self.editing_ticker == ticker:
            self.editing_ticker = None
            self.entry_ticker.config(state="normal")
            self.btn_add.config(text="추가")
            self.btn_cancel.grid_remove()
            self._clear_entries()
        self.update_ui()

    def on_load_clicked(self) -> None:
        self.app.load_state()
        messagebox.showinfo("불러오기 완료", "포트폴리오를 불러왔습니다")

    def on_close(self) -> None:
        self.app.save_state()
        self.destroy()

    def _on_table_configure(self, event) -> None:
        """창 크기에 맞춰 컬럼 너비를 조정한다."""
        if event.width <= 1:
            return
        total_cols = len(self.table["columns"])
        if total_cols == 0:
            return
        col_width = max(event.width // total_cols, 20)
        for col in self.table["columns"]:
            self.table.column(col, width=col_width)
