import tkinter as tk
from tkinter import ttk

class PortfolioAppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dividend ETF Portfolio Manager")
        self.geometry("1200x700")

        # Menu Bar
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save")
        file_menu.add_command(label="Load")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

        # Toolbar
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        for text in ["Add", "Remove", "Refresh", "Rebalance", "Save/Load"]:
            btn = tk.Button(toolbar, text=text)
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Main frames
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Asset table
        table_frame = tk.Frame(main_frame)
        table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        columns = ("Ticker", "Target%", "Shares", "AvgCost", "Price", "Value", "Gain%", "Yield%")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill=tk.BOTH, expand=True)

        # Input panel
        input_frame = tk.Frame(main_frame, width=300)
        input_frame.pack(side=tk.RIGHT, fill=tk.Y)
        fields = [("ETF Ticker", ""), ("Avg. Cost", ""), ("Deposit", "")]
        for label, _ in fields:
            row = tk.Frame(input_frame)
            tk.Label(row, text=label, width=15, anchor='w').pack(side=tk.LEFT)
            tk.Entry(row).pack(side=tk.RIGHT, fill=tk.X, expand=True)
            row.pack(fill=tk.X, pady=5)
        btn_frame = tk.Frame(input_frame)
        for btext in ["Add", "Update", "Rebalance"]:
            tk.Button(btn_frame, text=btext).pack(side=tk.LEFT, padx=5, pady=10)
        btn_frame.pack()

        # Status bar
        status = tk.Label(self, text="Last Refresh: -- | Total Value: --", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status.pack(side=tk.BOTTOM, fill=tk.X)

if __name__ == "__main__":
    app = PortfolioAppUI()
    app.mainloop()
