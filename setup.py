import pandas as pd
from datetime import datetime

#Custom tools
from data_processing import DataStorage, WebScrape

class Instance:
    def __init__(self, config):
        self.config = config

        # Access the variables
        self.db_file = config.db_file
        self.build_db = config.build_db
        self.source_manifest = config.source_manifest

        storage = DataStorage(self.db_file)

        if self.build_db:
            # Scrape data
            scrape = WebScrape(source_manifest)
            df = scrape.scrape_data()
            manifest = storage.create_manifest(df, build_db=True)
            storage.store_manifest_data(manifest, build_db=True)
        else:
            #Get manifest if rebuild (build_db) is false
            manifest = storage.load_manifest_data()

        if self.build_db:
            # Fetch historical prices and analyze data for each ticker
            for _, row in manifest.iterrows():
                ticker = row['Ticker'] + '.AX'
                table_name = row['Table_Name']
                sector = row['Sector']
                
                #Get each price (2y) and write to DB tables
                data = DataSource(ticker).get_historical_prices()
                
                # Create an instance of TrendAnalyzer
                analyzer = TrendAnalyzer(ticker, data)
                
                # Calculate the technical indicators
                analyzer.calculate_technical_indicators()
                
                # Store the modified historical prices in a separate table
                storage.store_historical_prices(table_name, analyzer.data)
                
                pass
        
        #init data storage
        self.datastore = DataStorage(self.db_file)