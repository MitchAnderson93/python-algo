
# ASX Notebook
## Installation

Python kit for ASX analysis (pandas, sqlite, numpy, bs4/selenium, TA, yfinance) in an OOP format/Jupyter notebook.

```python 
class Config:
    def __init__(self):
        # Change as needed
        self.build_db = True
        # ensure there is a blank db.sqlite3 file in root
```

Builds a local DB with 2400+ symbols and a manifest specific table for lookups (e.g. BHP / Materials / BHP.AX) during setup (if enabled in config).

Each symbol table contains 2 years historical data (approx. 150mb when complete). This includes columns for SMA, RSI and Bollinger bands.

**Manifest (key/values):**<BR>
Ticker | Sector | Table_Name | Last Scan Date<BR>
BHP | Materials | BHP.AX | 2023-06-07

**{TICKER}.AX table:**<BR>
Date | Open | High | Low | Close | Adj Close | Volume | MA25 | MA50 | MA75 | MA200 | RSI | BBUPPER | BBLOWER<BR>

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
    
#### Accessing classes
```python 
    # Global vars
    db_file = global_vars.db_file

    # DataStorage class
    storage = DataStorage(db_file)

    #Get table data
    data = storage.get_table_data(table_name)
```

#### To do's
Slowely adding linear regression and other tools for analysis (future commits)

#### Flake8 linting runs on pre-commit hook
- See .pre-commit-config.yaml
```bash
pre-commit install
```