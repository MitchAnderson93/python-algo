```
 ___        _    _                 _____            _     
| _ \ _  _ | |_ | |_   ___  _ _   |_   _| ___  ___ | | ___
|  _/| || ||  _|| ' \ / _ \| ' \    | |  / _ \/ _ \| |(_-<
|_|   \_, | \__||_||_|\___/|_||_|   |_|  \___/\___/|_|/__/
      |__/                                                
```

A python template and set of tools I developed for running regular  functions, tasks and reports. 

CLI menu:

```
1. Tasks - e.g /tasks/do_this.py
2. Functions - One off functions (calculate CAGR)
3. Reports - e.g. reports/visualize-x.py 
4. Update local data source (sqlite) - Reruns system/setup.py 
5. Exit
```

### Steps to setup:
- ```python3 -m venv env``` to initialise a local env
- ```source env/bin/activate``` to activate local dev environment (for installing pip packages)
- ```pip install -r requirements.txt``` to install dependencies 
- ```jupyter notebook``` to run notebooks if exist

### Using the CLI tool:
- ```python cli.py``` to run CLI
- ```--logs```to enable detailed logging as optional argument

### Running tests:
- ```pytest tests/{{file}}/test.py``` to validate an individual function

### Other commands for managing the repository:
- ```pip freeze > requirements.txt``` to add/manage new dependencies 

### Intended to be edited/customised/files added:
``` 
├── data/                   # ./data/ needs to exist with raw and processed subfolders. Files are customisable.   
│   ├── raw/                # Intended for raw datasets (CSV/JSON) and is referred to in system code as a path.
│   ├── processed/          # Output directory for processed files (CSV/JSON) and is referred to in system code as a path.
├── custom_setup/           # A place to customise the setup of the database, runs after general setup if ./custom_setup/ exists.
│   ├── custom_setup.py     # An example included to show how to customise the sqlite db during setup/update. Only runs if exists in parent folder.
│   ├── jobs/metrics/       # An example of a job that is run during the included custom_setup.py example, this adds additional data to the database during setup/update cycle.
├── reports/                # A place to store reports for easy generation from the menu (.py)
├── tasks/                  # A set of regular tasks that run against the dataset, and exports to data/processed/{date}
├── functions/              # Functions runs from the CLI and includes an example (CAGR)
├── tests/                  # Unit tests for reused functions
```

### Not intended to be edited:
``` 
├── env/                    # Not committed but created during setup steps. Do not commit (is covered by default in .gitignore)
├── system/                 # System utilities directory
│   ├── common.py           # Shared imports and utilities
│   ├── setup.py            # Runs during setup (any python/context)
│   ├── utils/              # Basic utility functions e.g log_message()
│      ├── common.py        # Common packages used throughout
├── cli.py                  # Start here to run.
├── requirements.txt        # Dependencies 
```