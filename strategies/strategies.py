import pandas as pd
import numpy as np
from modules.tradelogger import TradeLogger

class Strategy:
    def __init__(self):
        self.name = None

    @staticmethod
    def mean_reversion_strategy(
            data,
            rsi_oversold=45,
            target_percent=0.05,
            stop_loss_percent=0.01,
            report=True,
            allocated_capital = None,
            dca_entry=None,
            dca_exit=None
    ):
        # Ensure that the 'Close' column is present in the DataFrame
        if 'Close' not in data.columns:
            raise KeyError("Column 'Close' not found in the input data DataFrame.")

        # Initialize position
        position = None

        # Initialize columns for buy/sell signals, position dates, and trade profits/losses
        data['Signal'] = ""
        data['Position Date'] = pd.NaT
        data['Trade'] = 0.0

        # Trade logger for reporting
        if report:
            logger = TradeLogger()

        # Iterate over data
        for i in range(len(data)):
            if position:  # If we are already in a position

                if data['Close'][i] >= position['price'] * (1 + target_percent):
                    data.loc[i, 'Signal'] = "SELL"
                    data.loc[i, 'Trade'] = (data['Close'][i] - position['price']) / position['price']

                    # Set position size using dca_exit
                    position_size = position['size'] * dca_exit
                    logger.log_trade('SELL', data['Close'][i], data.index[i], position_size=position_size)
                    position = None  # Sell if price exceeds target

                elif data['Close'][i] <= position['price'] * (1 - stop_loss_percent):
                    data.loc[i, 'Signal'] = "SELL"
                    data.loc[i, 'Trade'] = (data['Close'][i] - position['price']) / position['price']

                    # Set position size using dca_exit
                    position_size = position['size'] * dca_exit
                    logger.log_trade('SELL', data['Close'][i], data.index[i], position_size=position_size)
                    position = None  # Sell if price drops below stop loss

            else:  # If we are not in a position
                if data['Close'][i] < data['BB_LOWER'][i] and data['RSI'][i] < rsi_oversold:
                    data.loc[i, 'Signal'] = "BUY"

                    position_size = Strategy.calculate_position_size(allocated_capital, dca_entry, data['Close'][i])

                    position = {'price': data['Close'][i], 'date': data.index[i], 'size': position_size}
                    data.loc[i, 'Position Date'] = position['date']

                    # Calculate position size
                    logger.log_trade('BUY', data['Close'][i], data.index[i], position_size=position_size)

        # Print logger
        if report:
            logger.print_records()
            profit_loss = logger.calculate_profit_loss()
            print(f"Total Profit/Loss: {profit_loss}")

        return data

    @staticmethod
    def calculate_position_size(allocated_capital, dca_entry, price):
        # Calculate position size based on allocated capital, dca_entry, and price
        cash_amount = allocated_capital * dca_entry
        position_size = cash_amount / price
        return position_size