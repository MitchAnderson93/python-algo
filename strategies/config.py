class Config:
    def __init__(self):
        # Change as needed / change to dataset.sqlite3 and build_db true before commit
        self.db_file = 'db.sqlite3'
        self.total_funds = 100000  # Total funds available for trading
        self.show_charts = True
        self.source_manifest = 'https://www.marketindex.com.au/asx-listed-companies'
        self.build_db = False