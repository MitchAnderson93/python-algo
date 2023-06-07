
## Installation

Python kit for ASX analysis (pandas, sqlite, numpy, bs4/selenium, TA, yfinance) in an OOP format/Jupyter notebook.

```python 
class GlobalVariables:
    def __init__(self):
        # Global variables
        self.build_db = True
```

Builds a local DB with 2400 tickers (if enabled) and a manifest specific table for lookups (e.g. BHP / Materials / BHP.AX).

**Manifest table:**<BR>
Ticker | Sector | Table_Name | Last Scan Date<BR>
BHP | Materials | BHP.AX | 2023-06-07

**{ticker}.AX table:**<BR>
Date | Open | High | Low | Close | Adj Close | Volume<BR>
2021-06-07 00:00:00	 | X | X | X | X | X | x 

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