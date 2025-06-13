flowchart TB
  subgraph Desktop_App ["Desktop App"]
    UI["UI (tkinter/Qt)"]
    Logic["PortfolioApp Logic"]
  end

  subgraph Local_Storage ["Local Storage"]
    DB["JSON / SQLite"]
  end

  subgraph External_API ["External API"]
    API["Price Data Service"]
  end

  Desktop_App --> Local_Storage
  Desktop_App --> External_API
