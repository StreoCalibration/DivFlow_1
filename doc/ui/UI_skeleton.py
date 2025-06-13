import tkinter as tk
from tkinter import ttk

class PortfolioAppUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("배당형 ETF 포트폴리오 관리")
        self.geometry("1200x700")

        # 메뉴 바
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="저장")
        file_menu.add_command(label="불러오기")
        file_menu.add_separator()
        file_menu.add_command(label="종료", command=self.quit)
        menubar.add_cascade(label="파일", menu=file_menu)
        self.config(menu=menubar)

        # 툴바
        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)
        for text in ["추가", "제거", "갱신", "리밸런싱", "저장/불러오기"]:
            btn = tk.Button(toolbar, text=text)
            btn.pack(side=tk.LEFT, padx=2, pady=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # 메인 프레임
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 자산 테이블
        table_frame = tk.Frame(main_frame)
        table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        columns = (
            "티커",
            "목표비중(%)",
            "현재비중(%)",
            "보유수량",
            "매입단가",
            "전일종가(외화)",
            "전일종가(원화)",
            "평가금액(외화)",
            "평가금액(원화)",
        )
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill=tk.BOTH, expand=True)

        # 입력 패널
        input_frame = tk.Frame(main_frame, width=300)
        input_frame.pack(side=tk.RIGHT, fill=tk.Y)
        fields = [("ETF 티커", ""), ("매입 단가", ""), ("입금액(원화)", "")]
        for label, _ in fields:
            row = tk.Frame(input_frame)
            tk.Label(row, text=label, width=12, anchor='w').pack(side=tk.LEFT)
            tk.Entry(row).pack(side=tk.RIGHT, fill=tk.X, expand=True)
            row.pack(fill=tk.X, pady=5)
        btn_frame = tk.Frame(input_frame)
        for btext in ["추가", "취소", "업데이트", "리밸런싱"]:
            tk.Button(btn_frame, text=btext).pack(side=tk.LEFT, padx=5, pady=10)
        btn_frame.pack()

        # 상태 표시줄
        status = tk.Label(self, text="마지막 갱신: -- | 연간 배당수익률 평균: --", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status.pack(side=tk.BOTTOM, fill=tk.X)

if __name__ == "__main__":
    app = PortfolioAppUI()
    app.mainloop()
