# 개발 뷰 (Development View)

이 문서는 코드 구조 및 파일 매핑을 설명합니다.

```
/your_repo/
├── src/
│   ├── portfolio.py       # PortfolioApp, Portfolio
│   ├── asset.py           # Asset
│   ├── fetcher.py         # PriceFetcher
│   ├── storage.py         # PortfolioStorage (포트폴리오와 환율 저장)
│   └── main_window.py     # MainWindow
```

- 각 모듈과 클래스가 1:1로 매핑되어 있어 유지보수 및 확장이 용이합니다.
- `README.md` 또는 `docs/README.md`에 각 모듈 설명을 추가 권장.
