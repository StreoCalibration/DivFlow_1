# 개발 뷰 (Development View)

이 문서는 코드 구조 및 파일 매핑을 설명합니다.

```
/divflow/
├── requirements.txt       # 외부 패키지 의존성
├── README.md             # 프로젝트 개요 및 실행 방법
├── src/
│   ├── __init__.py       # 패키지 초기화
│   ├── __main__.py       # 애플리케이션 진입점
│   ├── asset.py          # Asset 데이터 클래스
│   ├── portfolio.py      # Portfolio, PortfolioApp 클래스
│   ├── fetcher.py        # PriceFetcher 클래스 (yfinance 사용)
│   ├── storage.py        # PortfolioStorage 클래스 (JSON 저장/불러오기)
│   └── main_window.py    # MainWindow 클래스 (tkinter GUI)
├── data/                 # 런타임 생성 (gitignore)
│   ├── portfolio.json    # 포트폴리오 데이터
│   └── exchange_rate.json # 환율 정보
└── doc/
    ├── README.md         # 문서 개요
    ├── architecture/     # 아키텍처 문서
    │   ├── logical_view.md
    │   ├── physical_view.md
    │   ├── process_view.md
    │   ├── development_view.md
    │   ├── scenario_view.md
    │   └── diagrams/     # 다이어그램 파일
    ├── specs/            # 요구사항 명세
    │   ├── SRS.md       # 소프트웨어 요구사항
    │   └── URS.md       # 사용자 요구사항
    ├── ui/              # UI 관련 문서
    │   └── UI_skeleton.py # UI 프로토타입
    └── log/             # 변경 이력
        ├── 2025-06-13.md
        ├── 2025-06-14.md
        └── 2025-06-15.md
```

## 모듈별 책임

### `asset.py`
- **Asset** 클래스: 개별 자산 정보를 담는 데이터 클래스
- 평가액, 손익, 배당금 계산 메서드 제공

### `portfolio.py`
- **Portfolio** 클래스: 자산 컬렉션 관리
  - 자산 추가/제거
  - 전체 평가액 및 비중 계산
  - 가격 정보 업데이트
- **PortfolioApp** 클래스: 애플리케이션 로직
  - 시세 갱신
  - 저장/불러오기
  - 리밸런싱 계산

### `fetcher.py`
- **PriceFetcher** 클래스: 외부 API 연동
  - yfinance를 통한 Yahoo Finance 데이터 조회
  - 종가, 배당률, 환율 정보 가져오기
  - 1시간 캐싱으로 API 호출 최소화

### `storage.py`
- **PortfolioStorage** 클래스: 영속성 관리
  - JSON 형식으로 포트폴리오 저장/불러오기
  - 환율 정보 별도 파일 관리
  - 디렉토리 자동 생성

### `main_window.py`
- **MainWindow** 클래스: GUI 구현
  - tkinter 기반 사용자 인터페이스
  - 테이블 뷰로 포트폴리오 표시
  - 자산 추가/수정/삭제 기능
  - 인라인 편집 기능

### `__main__.py`
- 애플리케이션 진입점
- 각 컴포넌트 초기화 및 연결
- GUI 실행

## 코딩 컨벤션
- Python PEP 8 스타일 가이드 준수
- 메서드명: snake_case
- 클래스명: PascalCase
- 상수: UPPER_SNAKE_CASE
- Private 멤버: 언더스코어 prefix (`_member`)
- Type hints 사용 (Python 3.8+ 호환)

## 확장 가능성
- 각 모듈이 단일 책임을 가지도록 설계
- 인터페이스를 통한 느슨한 결합
- 새로운 데이터 소스 추가 시 PriceFetcher만 수정
- 새로운 저장 형식 추가 시 PortfolioStorage만 수정