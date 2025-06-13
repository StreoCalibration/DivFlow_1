# User Requirements Specification (URS)

## 1. Introduction
This document captures the user-level requirements for the Dividend ETF Portfolio Management Application.

### 1.1 Purpose
To define the functionalities and constraints from the end-user perspective.

### 1.2 Scope
The application allows users to manage a portfolio of dividend-focused ETFs, including setting target allocations, recording purchases, refreshing real-time data, and calculating portfolio metrics.

## 2. Functional Requirements
1. **Portfolio Configuration**
   - FR1.1: User shall be able to add/remove ETF tickers.
   - FR1.2: User shall be able to set target allocation percentages for each ETF.
2. **Transaction Recording**
   - FR2.1: User shall be able to input purchase details: number of shares and average cost per share.
   - FR2.2: User shall be able to update holdings after additional purchases.
3. **Data Refresh**
   - FR3.1: User shall be able to trigger a refresh to fetch current market prices and dividend yields.
   - FR3.2: System shall display updated portfolio value, individual asset value, gain/loss, and dividend estimates.
4. **Rebalancing Assistant**
   - FR4.1: User shall be able to input an additional deposit amount.
   - FR4.2: System shall calculate and suggest share purchases to match target allocations based on refreshed prices.
5. **Persistence**
   - FR5.1: User settings and portfolio state shall be saved automatically.
   - FR5.2: User shall be able to load the last saved state on application start.

## 3. Non-Functional Requirements
1. **Usability**
   - NFR1.1: The UI shall be intuitive, with clear labels and prompts.
   - NFR1.2: Refresh operations shall complete within 5 seconds.
2. **Reliability**
   - NFR2.1: The application shall handle API failures gracefully with user-friendly error messages.
3. **Performance**
   - NFR3.1: The application shall refresh market data for up to 20 assets in under 5 seconds.
4. **Maintainability**
   - NFR4.1: Configuration and state files shall use human-readable formats (JSON or SQLite).
5. **Portability**
   - NFR5.1: The application shall run on Windows, macOS, and Linux environments.

## 4. Assumptions
- Users have internet connectivity to fetch market data.
- Users possess an API key if required by the data provider.

