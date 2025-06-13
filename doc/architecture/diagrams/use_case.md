flowchart TB
  %% 액터
  User((User))

  %% 유스케이스
  A1((Add Asset))
  A2((Refresh Portfolio))
  A3((Rebalance with Deposit))
  A4((Save/Load State))

  %% 관계
  User --> A1
  User --> A2
  User --> A3
  User --> A4
