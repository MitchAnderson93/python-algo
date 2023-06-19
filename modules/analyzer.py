import ta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd


class TrendAnalyzer:
    def __init__(self, ticker, data):
        self.ticker = ticker
        self.data = data

    def calculate_technical_indicators(self):
        self.calculate_moving_averages()
        self.calculate_rsi()
        self.calculate_bollinger_bands()

    def calculate_moving_averages(self):
        self.data['MA25'] = ta.trend.sma_indicator(self.data['Close'], window=25)
        self.data['MA50'] = ta.trend.sma_indicator(self.data['Close'], window=50)
        self.data['MA75'] = ta.trend.sma_indicator(self.data['Close'], window=75)
        self.data['MA200'] = ta.trend.sma_indicator(self.data['Close'], window=200)

    def calculate_rsi(self):
        self.data['RSI'] = ta.momentum.rsi(self.data['Close'])

    def calculate_bollinger_bands(self):
        indicator_bb = ta.volatility.BollingerBands(self.data['Close'])
        self.data['BB_UPPER'] = indicator_bb.bollinger_hband()
        self.data['BB_LOWER'] = indicator_bb.bollinger_lband()

    # Defaults without order but can show a merged dataset (BUY/SELL)
    def fundamentals_chart(self, orders=False, filter=0, RSI=False):
        # Set dark mode style
        plt.style.use('dark_background')

        # Create a figure and subplots for the two visualizations
        if RSI:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        else:
            fig, ax1 = plt.subplots(1, figsize=(10, 8))

        # Convert 'Date' column to datetime format
        self.data['Date'] = pd.to_datetime(self.data['Date'])

        if filter == 0:
            # Get the date range for the last 90 days
            last_90_days = datetime.now() - timedelta(days=90)
            filtered_data = self.data[self.data['Date'] >= last_90_days]
        else:
            custom_filter = datetime.now() - timedelta(days=filter)
            filtered_data = self.data[self.data['Date'] >= custom_filter]

        # Calculate technical indicators
        self.calculate_technical_indicators()

        # Plot the stock price with moving averages and Bollinger Bands
        ax1.plot(filtered_data['Date'], filtered_data['Close'], label='Closing Price')
        ax1.plot(filtered_data['Date'], filtered_data['MA25'], label='SMA 25')
        ax1.plot(filtered_data['Date'], filtered_data['MA50'], label='SMA 50')
        ax1.plot(filtered_data['Date'], filtered_data['MA75'], label='SMA 75')
        ax1.plot(filtered_data['Date'], filtered_data['MA200'], label='SMA 200')
        ax1.fill_between(filtered_data['Date'], filtered_data['BB_UPPER'], filtered_data['BB_LOWER'], color='lightblue', alpha=0.2, label='Bollinger Bands')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price')
        ax1.set_title('Fundamentals for ' + self.ticker)
        ax1.legend()

        # Format the x-axis tick labels as year/month/day
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        if RSI:
            # Plot the RSI
            ax2.plot(filtered_data['Date'], filtered_data['RSI'], label='RSI')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('RSI')
            ax2.set_title('Relative strength index')
            ax2.legend()

            # Format the x-axis tick labels as year/month/day
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        if orders:
            # Plot buy markers
            buy_dates = filtered_data[filtered_data['Trade'] > 0]['Date']
            buy_prices = filtered_data[filtered_data['Trade'] > 0]['Close']
            ax1.scatter(buy_dates, buy_prices, color='green', marker='^', label='Buy')

            for date in buy_dates:
                print(date)

            # Plot sell markers
            sell_dates = filtered_data[filtered_data['Trade'] < 0]['Date']
            sell_prices = filtered_data[filtered_data['Trade'] < 0]['Close']
            ax1.scatter(sell_dates, sell_prices, color='red', marker='v', label='Sell')

            for date in sell_dates:
                print(date)

        # Rotate the x-axis tick labels for better readability
        plt.xticks(rotation=45)

        # Adjust the layout and spacing between subplots
        fig.tight_layout()

        # Show the plot
        plt.show()