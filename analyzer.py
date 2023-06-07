import ta
import matplotlib.pyplot as plt


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

    def chart(self):
        # Set dark mode style
        plt.style.use('dark_background')

        # Create a figure and subplots for the two visualizations
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # Plot the stock price with moving averages and Bollinger Bands
        ax1.plot(self.data['Date'], self.data['Close'], label='Closing Price')
        ax1.plot(self.data['Date'], self.data['ma25'], label='SMA 25')
        ax1.plot(self.data['Date'], self.data['ma50'], label='SMA 50')
        ax1.plot(self.data['Date'], self.data['ma75'], label='SMA 75')
        ax1.plot(self.data['Date'], self.data['ma200'], label='SMA 200')
        ax1.plot(self.data['Date'], self.data['bb_upper'], label='Bollinger Bands Upper')
        ax1.plot(self.data['Date'], self.data['bb_lower'], label='Bollinger Bands Lower')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price')
        ax1.set_title(self.ticker)
        ax1.legend()

        # Plot the RSI
        ax2.plot(self.data['Date'], self.data['rsi'], label='RSI')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('RSI')
        ax2.set_title('RSI')
        ax2.legend()

        # Adjust the layout and spacing between subplots
        fig.tight_layout()

        # Show the plot
        plt.show()
