import backtrader as bt
from backtrader.indicators import BollingerBands

class Strategy(bt.Strategy):
    params = (
        ('bb_period', 20),      # Bollinger Bands period
        ('bb_devfactor', 2),    # Bollinger Bands deviation factor
        ('rsi_period', 14),     # RSI period
        ('rsi_oversold', 45),   # RSI oversold level
        ('target_percent', 0.05),   # Target percentage (5%)
        ('stop_loss_percent', 0.01)  # Stop-loss percentage (1%)
    )
    
    def __init__(self):
        self.bbands = BollingerBands(self.data.close, period=self.params.bb_period, devfactor=self.params.bb_devfactor)
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        
    def next(self):
        if self.position:  # If we are already in a position
            if self.data.close[0] >= self.position.price * (1 + self.params.target_percent):
                self.sell()  # Sell if price exceeds target
            elif self.data.close[0] <= self.position.price * (1 - self.params.stop_loss_percent):
                self.sell()  # Sell if price drops below stop loss
        else:  # If we are not in a position
            if self.data.close[0] < self.bbands.lines.bot[0] and self.rsi < self.params.rsi_oversold:
                self.buy()  # Buy if price is below lower Bollinger Band and RSI is below oversold level
