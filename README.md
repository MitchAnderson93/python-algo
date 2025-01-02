## Toolkit for applied finance use

### Steps to setup:
- Requires Python3/pip to run (install both)
- ```python3 -m venv env``` to initialise a local env
- ```source env/bin/activate``` to activate local dev environment (for installing pip packages)
- ```pip install -r requirements.txt``` to install dependencies 
- ```jupyter notebook``` to run notebooks if exist

### Using the CLI tool:
- ```python cli.py``` to run CLI
- ```python cli.py --debug```to enable detailed logging

### Other commands for managing the repository:
- ```pip freeze > requirements.txt``` to add/manage new dependencies 

### Running tests:
- ```pytest tests/functions/cagr/test.py``` to validate an individual function

### Included in this repository:
``` 
├── env/                    # Not committed.
├── data/
│   ├── raw/                # Raw datasets (CSV/JSON)
│   ├── processed/          # Cleaned datasets as JSON documents sorted by date generated
├── sys/                    # System utilities directory
│   ├── common.py           # Shared imports and utilities
│   ├── setup.py            # Run from CLI during project setup
│   ├── update.py           # Update the local SQLite database using data/raw datasets
├── lib/                    # Application logic
│   ├── __init__.py         # Package file
│   ├── metrics.py          # Uses imports from `sys/common.py`
├── tests/                  # Unit tests for scripts
├── requirements.txt        # Dependencies
├── README.md               # Project overview and usage instructions
├── cli.py                  # Start here
```