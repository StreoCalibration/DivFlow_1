# 논리 뷰 (Logical View)

이 문서는 시스템의 클래스 및 객체 구조를 정의합니다.

![클래스 다이어그램](diagrams/class_diagram.png)

## 주요 클래스 및 관계

- **PortfolioApp**  
  - portfolio: Portfolio  
  - price_fetcher: PriceFetcher  
  - storage: PortfolioStorage  
  - ui: MainWindow  
  - exchange_rate: float
  - 메서드: 
    - refresh_data(): 시세 정보를 갱신
    - save_state(): 포트폴리오와 환율 정보를 저장
    - load_state(): 저장된 포트폴리오와 환율 정보를 불러옴
    - calculate_rebalancing(amount): 입금액(원화)으로 리밸런싱 계산
    - set_ui(ui): UI 인스턴스 설정

- **Portfolio**  
  - assets: Dict[str, Asset]  
  - 메서드: 
    - add_asset(asset): 자산 추가
    - remove_asset(ticker): 자산 제거
    - get_total_value(): 전체 평가액 계산
    - get_allocation_ratios(): 현재 비중 계산
    - update_prices(prices, dividends): 가격 정보 업데이트
    - calculate_stats(): 통계 정보 계산
    - print_allocation(): 현재/목표 비중을 콘솔에 출력

- **Asset**
  - ticker: str (종목 코드)
  - weight: float (목표 비중, 0~1)
  - shares: float (보유 수량)
  - avg_cost: float (평균 매입 단가)
  - close_price: float (전일 종가)
  - dividend_yield: float (배당 수익률)
  - 메서드: 
    - get_value(): 평가액 계산
    - get_gain(): 손익 계산
    - get_dividend_amount(): 예상 배당금 계산
    - get_weight_percentage(total): 전체 대비 비중 계산

- **PriceFetcher**
  - _price_cache: Dict[str, float] (가격 캐시)
  - _price_timestamp: Dict[str, float] (캐시 타임스탬프)
  - _dividend_cache: Dict[str, float] (배당 캐시)
  - _exchange_rate: Optional[float] (환율 캐시)
  - _rate_timestamp: float (환율 캐시 타임스탬프)
  - 메서드: 
    - fetch_close_price(ticker): 종가 조회
    - fetch_dividend(ticker): 배당 수익률 조회
    - fetch_all(tickers): 여러 종목 정보 일괄 조회
    - fetch_exchange_rate(): USD/KRW 환율 조회
    - load_cache(prices, dividends): 캐시 초기화
    - _fetch_yahoo_info(ticker): yfinance API 호출 (내부 메서드)

- **PortfolioStorage**  
  - path: Path (포트폴리오 저장 경로)
  - exchange_rate_path: Path (환율 저장 경로)
  - 메서드: 
    - save(portfolio): 포트폴리오 저장
    - load(): 포트폴리오 불러오기
    - save_exchange_rate(rate): 환율 저장
    - load_exchange_rate(): 환율 불러오기

- **MainWindow**  
  - app: PortfolioApp (애플리케이션 인스턴스)
  - table: ttk.Treeview (포트폴리오 테이블)
  - editing_ticker: Optional[str] (편집 중인 종목)
  - UI 컴포넌트: entry_ticker, entry_weight, entry_shares, entry_cost, entry_deposit
  - 이벤트 핸들러:
    - on_refresh_clicked(): 시세 갱신
    - on_save_clicked(): 포트폴리오 저장
    - on_load_clicked(): 포트폴리오 불러오기
    - on_add_fund_clicked(): 리밸런싱 계산
    - on_add_asset(): 자산 추가
    - on_update_asset(): 자산 수정
    - on_remove_asset(): 자산 삭제
    - on_edit_asset(event): 자산 편집 모드 진입
    - on_cancel_edit(): 편집 취소
    - on_close(): 종료 시 자동 저장
    - update_ui(): UI 갱신
    - _build_widgets(): UI 구성
    - _clear_table(): 테이블 초기화
    - _clear_entries(): 입력 필드 초기화
    - _on_table_configure(event): 테이블 크기 조정