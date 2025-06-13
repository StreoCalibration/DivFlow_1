# 📄 Feature: Refresh 기능

## 목표
버튼 클릭 시 ETF 현재가를 조회하고 수익률/평가금/배당을 자동 갱신한다.

## 입력
- 사용자가 'Refresh' 버튼 클릭

## 처리
- FinanceAPI 호출하여 현재가 및 환율 수집
- PortfolioModel에서 계산 수행

## 출력
- PortfolioTable UI 갱신
