
## Installation

Python kit for ASX analysis (pandas, sqlite, numpy, bs4/selenium/jupyter/TA/yfinance) in an OOP format.

Builds a local DB with 2400 tickers (if enabled) and a manifest specific table for lookups (e.g. BHP / Materials / BHP.AX).

Slowely adding linear regression and other tools for analysis. 

Requires pip/venv to setup and install requirements.txt. 


On Windows: 
```zsh
    python3 -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    jupyter notebook   
```

On macOS and Linux: 
```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    jupyter notebook    
```
    