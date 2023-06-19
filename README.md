
# Python notebook for ASX analysis

I made this ASX/Python notebook (using pandas, sqlite3, numpy, bs4/selenium, TA, yfinance, matplotlib, quantconnect etc) in an Object Oriented format. It has sub folder for running quantconnect cloud strategies (non-asx) (./quantconnect-lib/current_portfolio) which is a work in progress (I need to clean this up as I expand beyond just ASX)

Features:
- Builds local dataset (2 years historical data) to date
- Get dataset for specific symbol (includes SMA, RSI, BB bands)
- Generate a fundamentals chart (days) that accepts orders to reflect buy/sell signals
- Reusable logging for trades/profit and loss across modules
- A mean reversion strategy (work in progress) (./strategies/strategies.py)
- A function to return linear regression coherants using numpy 

Other ideas:
- Build an integration with Sharesight for ASX trades (Sharesight REST API)
- Search for a symbol, name or sector (return 1 or more results) - TO DO
- A basic AI models to try and predict a future buy? (based on historic data)

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