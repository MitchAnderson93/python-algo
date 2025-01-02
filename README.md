```
 ___        _    _                  _    _              _____            _     
| _ \ _  _ | |_ | |_   ___  _ _    /_\  | | __ _  ___  |_   _| ___  ___ | | ___
|  _/| || ||  _|| ' \ / _ \| ' \  / _ \ | |/ _` |/ _ \   | |  / _ \/ _ \| |(_-<
|_|   \_, | \__||_||_|\___/|_||_|/_/ \_\|_|\__, |\___/   |_|  \___/\___/|_|/__/
      |__/                                 |___/                               
```

A toolkit I made for re-usable financial functions.

### Steps to setup:
- ```python3 -m venv env``` to initialise a local env
- ```source env/bin/activate``` to activate local dev environment (for installing pip packages)
- ```pip install -r requirements.txt``` to install dependencies 
- ```jupyter notebook``` to run notebooks if exist

### Using the CLI tool:
- ```python cli.py``` to run CLI
- ```--logs```to enable detailed logging as optional argument

### Other commands for managing the repository:
- ```pip freeze > requirements.txt``` to add/manage new dependencies 

### Running tests:
- ```pytest tests/functions/cagr/main.py``` to validate an individual function

### Included in this repository:
``` 
├── env/                    # Not committed.
├── data/
│   ├── raw/                # Raw datasets (CSV/JSON) e.g. lvr.csv/listed.csv
│   ├── processed/          # Cleaned datasets as JSON documents sorted by date generated
├── system/                 # System utilities directory
│   ├── common.py           # Shared imports and utilities
│   ├── setup.py            # Run from CLI during project setup
│   ├── lib/                # Reusable functions
│      ├── functions/
│      ├── metrics.py       
│   ├──utils/               # Basic utility functions e.g log_message()
│      ├── common.py
├── tasks/                  # A set of regular tasks that run against the dataset, and exports to data/processed/{date}
├── tests/                  # Unit tests for reused functions
├── cli.py                  # Start here
├── requirements.txt        # Dependencies
```