
# Swing trading toolkit

Python notebook for end of day securities analysis (using pandas, sqlite3, numpy, bs4/selenium, TA, yfinance, backtrader, matplotlib etc) in an Object Oriented format. 

Features:
- Builds local dataset (2 years historical data) to date
- Get dataset for specific symbol (includes SMA, RSI, BB bands)
- Generate a fundamentals chart (days) that accepts orders to reflect buy/sell signals
- Can modify/create new strategies and pass them to backtrader to show profit/loss
- Search for a symbol, name or sector (return 1 or more results) - TO DO

**Installation**

You can use this to spin up your own notebook project and automatically build a dataset of 2400+ symbols and a manifest specific table for lookups (e.g. BHP / Materials / BHP.AX) during setup (if enabled in config).

Each symbol table contains 2 years historical data (approx. 150mb when complete). 

Modify the global config as needed, including the URL to get all securities (ASX) and under /modules/data_processing > class WebScrape to change how the manifest is built.

```python 
class Config:
    def __init__(self):
        # Change as needed
        self.build_db = True
        # ensure there is a blank dataset.sqlite3 file in root
```

**Manifest (key/values):**<BR>
Ticker | Sector | Table_Name | Last Scan Date<BR>
BHP | Materials | BHP.AX | 2023-06-07

**{TICKER}.AX table:**<BR>
Date | Open | High | Low | Close | Adj Close | Volume | MA25 | MA50 | MA75 | MA200 | RSI | BBUPPER | BBLOWER<BR>

Requires pip/venv to setup and install requirements.txt. 

**On Windows:** 
```bash
    python3 -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    jupyter notebook   
```

**On macOS and Linux:**
```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    jupyter notebook    
```
    
**Make your own**
see workbook.ipynb for example

**To do's**
- Clean up