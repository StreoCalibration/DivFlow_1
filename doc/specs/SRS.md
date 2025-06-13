# Software Requirements Specification (SRS)

## 1. System Overview
The Dividend ETF Portfolio Management Application is a desktop GUI tool for tracking and managing a dividend-focused ETF portfolio.

## 2. External Interface Requirements

### 2.1 User Interfaces
- GUI with table view for portfolio, input panels for settings, buttons for actions.
- Menu or toolbar for save, load, and refresh functions.

### 2.2 Hardware Interfaces
- Standard PC or laptop environment.
- No specialized hardware required.

### 2.3 Software Interfaces
- Market data API (e.g., Yahoo Finance, Alpha Vantage).
- Local storage via JSON files or SQLite database.

### 2.4 Communications Interfaces
- HTTPS for API calls.

## 3. System Features

### 3.1 Portfolio Management
- Description: Manage ETF list and target allocations.
- Input: Ticker symbols, allocation percentages.
- Output: Updated portfolio configuration.

### 3.2 Transaction Recording
- Description: Record and update share holdings.
- Input: Number of shares, cost per share.
- Output: Updated holdings in local storage.

### 3.3 Data Refresh and Display
- Description: Fetch and display real-time price and dividend data.
- Input: Refresh command.
- Output: Table with current price, portfolio value, gain/loss, dividend yield.

### 3.4 Rebalancing Suggestion
- Description: Calculate purchase suggestions based on deposit.
- Input: Deposit amount.
- Output: Number of shares to buy per asset.

### 3.5 Persistence and Recovery
- Description: Automatic save and load of state.
- Input: Application start/exit events.
- Output: Restored portfolio state.

## 4. Performance Requirements
- The system shall handle up to 50 ETFs without degradation.
- Refresh operation shall complete within 5 seconds for 20 ETFs.

## 5. Design Constraints
- Implemented in Python 3.8+.
- GUI framework: Tkinter or PyQt5.
- Data storage: JSON or SQLite.

## 6. Quality Attributes
- Robust error handling for API and I/O.
- Clear and responsive UI.
- Modular code structure for ease of testing.

