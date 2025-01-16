import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json
import argparse
from tqdm import tqdm

import os
import sys

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, project_root)

from system.utils.common import log_message

class PortfolioBacktest:
    def __init__(self, portfolio_file, months=24, amount=10000, debug=False):
        with open(portfolio_file, 'r') as f:
            self.portfolio = pd.DataFrame(json.load(f))
        self.test_period = months
        self.amount = amount
        self.start_date = datetime.now() - timedelta(days=months * 30)
        self.results = []
        self.debug = debug

    def run(self):
        print(f"\nSimulating {len(self.portfolio)} positions over {self.test_period} months")
        print(f"Investment amount per position: ${self.amount:,.2f}")
        print("-" * 50)

        for _, stock in tqdm(self.portfolio.iterrows(), total=len(self.portfolio)):
            try:
                ticker = stock['code'] + '.AX'
                if self.debug:
                    print(f"\nProcessing {ticker}")
                
                hist = yf.download(ticker, start=self.start_date, progress=False)
                
                if hist.empty:
                    log_message(f"No historical data for {ticker}")
                    continue
                    
                if self.debug:
                    print(f"Got {len(hist)} days of data for {ticker}")
                
                # Ensure we have enough data
                if len(hist) < 30:  # Minimum 30 days of data
                    log_message(f"Insufficient historical data for {ticker}")
                    continue
                
                # Get valid dates (excluding last trading day)
                valid_dates = hist.index.tolist()[:-1]
                entry_date = random.choice(valid_dates)
                
                if self.debug:
                    print(f"Selected entry date: {entry_date}")
                
                entry_price = float(hist.loc[entry_date, 'Close'])
                current_price = float(hist['Close'].iloc[-1])
                
                if entry_price <= 0 or current_price <= 0:
                    log_message(f"Invalid price data for {ticker}")
                    continue
                
                # Calculate position metrics
                shares = self.amount / entry_price
                current_value = shares * current_price
                gain_loss = ((current_value - self.amount) / self.amount) * 100
                
                self.results.append({
                    'Code': stock['code'],
                    'Entry Date': entry_date.strftime('%Y-%m-%d'),
                    'Entry': f"${entry_price:.2f}",
                    'Current': f"${current_price:.2f}",
                    'Gain/Loss': f"{gain_loss:+.1f}%",
                    'Value': f"${current_value:,.2f}"
                })
                
                if self.debug:
                    print(f"Successfully added {ticker} to results")
            
            except Exception as e:
                log_message(f"Error processing {ticker}: {str(e)}")
                continue

    def report(self):
        if not self.results:
            print("\nNo valid results to display. Check the logs for errors.")
            return
        
        df = pd.DataFrame(self.results)
        df = df.sort_values('Gain/Loss', ascending=False)
        
        total_invested = self.amount * len(self.results)
        total_value = sum([float(r['Value'].replace('$','').replace(',','')) for r in self.results])
        total_return = ((total_value - total_invested) / total_invested) * 100
        
        print("\nPortfolio Performance Summary")
        print("=" * 50)
        print(f"Positions Analyzed: {len(self.results)} of {len(self.portfolio)}")
        print(f"Total Invested: ${total_invested:,.2f}")
        print(f"Current Value:  ${total_value:,.2f}")
        print(f"Overall Return: {total_return:+.1f}%")
        print("\nPosition Details:")
        print(df.to_string(index=False))

def main():
    parser = argparse.ArgumentParser(description="Backtest ASX portfolio with random entries")
    parser.add_argument('portfolio', help='Path to portfolio JSON file')
    parser.add_argument('--months', type=int, default=24, help='Test period in months')
    parser.add_argument('--amount', type=float, default=10000, help='Investment amount per position')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    bt = PortfolioBacktest(args.portfolio, args.months, args.amount, args.debug)
    bt.run()
    bt.report()

if __name__ == "__main__":
    main()