class Config:
    def __init__(self):
        # Change as needed / change to dataset.sqlite3 and build_db true before commit
        self.db_file = 'db.sqlite3'
        self.entry_threshold = -0.01  # 5% price decline
        self.exit_threshold = 0.01  # 5% price increase
        self.total_funds = 100000  # Total funds available for trading
        self.max_trade_size = self.total_funds * 0.1  # Maximum trade size (10% of total funds)
        self.max_allocation = self.max_trade_size * 0.1  # Maximum allocation per trade (10% of max trade size)
        self.show_charts = True
        self.source_manifest = 'https://www.marketindex.com.au/asx-listed-companies'
        self.build_db = False
