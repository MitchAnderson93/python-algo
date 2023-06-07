import os
import sqlite3
import pandas as pd
import yfinance as yf

from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dateutil.relativedelta import relativedelta

# Custom tools
from analyzer import TrendAnalyzer


class DataStorage:
    def __init__(self, db_file):
        self.db_file = db_file

    def store_manifest_data(self, manifest, build_db=False):
        if build_db and os.path.exists(self.db_file):
            os.remove(self.db_file)

        if build_db:
            open(self.db_file, 'w').close()

        conn = sqlite3.connect(self.db_file)
        manifest.to_sql('Manifest', conn, if_exists='replace', index=False)
        conn.close()

    def create_manifest(self, df, build_db=False):
        # Create a manifest table
        manifest = df[['Ticker', 'Sector']].copy()
        manifest['Table_Name'] = manifest['Ticker'] + '.AX'
        last_scan_date = datetime.today().strftime('%Y-%m-%d')
        manifest['Last Scan Date'] = last_scan_date
        return manifest

    def load_manifest_data(self):
        conn = sqlite3.connect(self.db_file)
        manifest = pd.read_sql_query('SELECT * FROM Manifest', conn)
        conn.close()
        return manifest

    def store_historical_prices(self, table_name, data):
        conn = sqlite3.connect(self.db_file)
        data_with_index = data.reset_index()  # Reset index to include the "Date" column
        data_with_index.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()

    def get_table_data(self, table_name):
        conn = sqlite3.connect(self.db_file)
        data = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)
        conn.close()
        return data

    def store_analyzed_data(self, table_name, data):
        conn = sqlite3.connect(self.db_file)
        data.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()

class DataSource:
    def __init__(self, ticker):
        self.ticker = ticker
        self.end_date = datetime.today().strftime('%Y-%m-%d')
        self.end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        # Calculate the start date 2 years before the current date
        self.start_date = (self.end_date - relativedelta(years=2)).strftime('%Y-%m-%d')

    def fetch_historical_prices(self):
        self.data = yf.download(self.ticker, self.start_date, self.end_date)
        return self.data

    def get_historical_prices(self):
        self.data = self.fetch_historical_prices()
        return self.data

    def extract_date_from_text(self, text):
        date_str = text.split('Data last updated: ')[1].split(' (')[0]
        return datetime.strptime(date_str, '%I:%M%p %d/%m/%y').strftime('%Y-%m-%d')


class DataAnalysis:
    def __init__(self, db_file):
        self.db_file = db_file
        self.data = None

    def analyze_data(self, ticker, data):
        # Perform linear regression analysis
        print('Performing tasks..')
        # ...
        pass
        
    def perform_linear_regression(self, data):
        # Perform linear regression analysis
        print('Performing linear regressions..')
        # ...
        pass


class WebScrape:
    def __init__(self, url):
        self.url = url

    # Scrape data using BS4
    def scrape_data(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Enable headless mode
        driver = webdriver.Chrome()  # or any other browser driver
        driver.get(self.url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table_div = soup.find('div', {'id': 'sticky-table'})
        rows = table_div.find('tbody').find_all('tr')
        data = []

        for row in rows:
            cells = row.find_all('td')
            row_data = [cell.get_text(strip=True) for cell in cells]
            data.append(row_data[2:])  # Drop the first two columns
        driver.quit()

        columns = ['Ticker', 'Company Name', 'Current Price', '1 Day', '1 Week', '1 Month', '1 Year', 'Sector', 'Market Cap']
        df = pd.DataFrame(data, columns=columns)
        return df
