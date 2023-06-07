import ta

class TrendAnalyzer:
    def __init__(self, ticker, data):
        self.ticker = ticker
        self.data = data

    def calculate_moving_averages(self):
        self.data['ma50'] = ta.trend.sma_indicator(self.data['Close'], window=50)
        self.data['ma200'] = ta.trend.sma_indicator(self.data['Close'], window=200)

    def calculate_rsi(self):
        self.data['rsi'] = ta.momentum.rsi(self.data['Close'])

    def calculate_bollinger_bands(self):
        indicator_bb = ta.volatility.BollingerBands(self.data['Close'])
        self.data['bb_upper'] = indicator_bb.bollinger_hband()
        self.data['bb_lower'] = indicator_bb.bollinger_lband()