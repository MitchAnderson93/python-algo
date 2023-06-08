import pandas as pd
from datetime import datetime

#Custom tools
from strategies.config import Config

class Instance:
    def __init__(self):
        #Custom tools
        from . import TrendAnalyzer
        from . import DataStorage, DataSource, WebScrape

        # Access the variables
        config = Config()
        self.db_file = config.db_file
        self.build_db = config.build_db
        self.source_manifest = config.source_manifest
        self.datastore = DataStorage(self.db_file)
        
        if self.build_db:
            # Scrape data
            scrape = WebScrape(self.source_manifest)
            df = scrape.scrape_data()
            manifest = self.datastore.create_manifest(df, build_db=True)
            self.datastore.store_manifest_data(manifest, build_db=True)
        else:
            #Get manifest if rebuild (build_db) is false
            manifest = self.datastore.load_manifest_data()

        if self.build_db:
            # Fetch historical prices and analyze data for each ticker
            for _, row in manifest.iterrows():
                ticker = row['Ticker'] + '.AX'
                table_name = row['Table_Name']
                sector = row['Sector']
                
                #Get each price (2y) and write to DB tables
                data = DataSource(ticker).get_historical_prices()
                
                # Create an instance of TrendAnalyzer to auto populate db with SMA/RSI/BB for demo
                analyzer = TrendAnalyzer(ticker, data)
                analyzer.calculate_technical_indicators()
                
                # Store the modified historical prices in a separate table
                self.datastore.store_historical_prices(table_name, analyzer.data)
                
                pass