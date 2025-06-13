# 프로세스 뷰 (Process View)

이 문서는 런타임 동작 흐름 및 시퀀스 다이어그램을 포함합니다.

![시퀀스 다이어그램](diagrams/sequence_refresh.png)

## Refresh 시퀀스

1. 사용자가 **Refresh** 버튼 클릭  
2. MainWindow.onRefreshClicked() 호출  
3. PortfolioApp.refreshData()  
4. PriceFetcher.fetchAll()  
5. Portfolio.updatePrices() 및 calculateStats()  
6. MainWindow.updateUI()  
