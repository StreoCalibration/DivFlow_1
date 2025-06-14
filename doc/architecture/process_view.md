# 프로세스 뷰 (Process View)

이 문서는 런타임 동작 흐름 및 시퀀스 다이어그램을 포함합니다.

![시퀀스 다이어그램](diagrams/sequence_refresh.png)

## Refresh 시퀀스

1. 사용자가 **Refresh** 버튼 클릭  
2. `MainWindow.on_refresh_clicked()` 호출  
3. `PortfolioApp.refresh_data()` 실행
4. `PriceFetcher.fetch_all(tickers)` 호출
   - 각 종목에 대해 `fetch_close_price()` 실행
   - 각 종목에 대해 `fetch_dividend()` 실행
5. `PriceFetcher.fetch_exchange_rate()` 호출로 환율 정보 가져오기
6. `Portfolio.update_prices(prices, dividends)`로 포트폴리오 업데이트
7. `MainWindow.update_ui()`로 화면 갱신

## 저장/불러오기 시퀀스

### 저장
1. 사용자가 **Save** 버튼 클릭 또는 애플리케이션 종료
2. `MainWindow.on_save_clicked()` 또는 `on_close()` 호출
3. `PortfolioApp.save_state()` 실행
4. `PortfolioStorage.save(portfolio)` - 포트폴리오 정보 저장
5. `PortfolioStorage.save_exchange_rate(rate)` - 환율 정보 저장

### 불러오기
1. 애플리케이션 시작 시 또는 **Load** 버튼 클릭
2. `PortfolioApp.load_state()` 호출
3. `PortfolioStorage.load()` - 포트폴리오 정보 불러오기
4. `PortfolioStorage.load_exchange_rate()` - 환율 정보 불러오기
5. `PriceFetcher.load_cache()` - 기존 가격 정보를 캐시에 로드
6. `MainWindow.update_ui()` - UI 갱신

## 리밸런싱 계산 프로세스

1. 사용자가 입금액 입력 후 **리밸런스** 버튼 클릭
2. `MainWindow.on_add_fund_clicked()` 호출
3. `PortfolioApp.calculate_rebalancing(amount)` 실행
   - 원화를 달러로 환산
   - `Portfolio.print_allocation()` - 현재 비중 출력
   - 목표 비중과의 차이가 큰 종목부터 매수 수량 계산
   - 잔여 금액이 없을 때까지 반복
4. 결과를 메시지 박스로 표시