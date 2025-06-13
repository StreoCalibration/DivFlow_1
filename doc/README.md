# DivFlow 문서 모음

본 폴더는 프로젝트 설계와 요구사항 등 모든 문서를 보관합니다.

## 하위 폴더
- `architecture/`: 아키텍처 문서 및 다이어그램
- `specs/`: 요구사항 명세서(SRS, URS)
- `ui/`: UI 목업과 예제 코드

## 모듈 설명
- `src/asset.py`: `Asset` 데이터 클래스
- `src/fetcher.py`: 가격과 배당 데이터를 가져오는 `PriceFetcher`
- `src/portfolio.py`: 포트폴리오 로직과 `PortfolioApp`
- `src/storage.py`: 파일 기반 저장소 `PortfolioStorage`
- `src/main_window.py`: GUI 구현 `MainWindow`
- `src/__main__.py`: 프로그램 진입점
