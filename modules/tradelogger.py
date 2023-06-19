class TradeLogger:
    def __init__(self):
        self.records = []

    # add position_size
    def log_trade(self, action, price, date, position_size):
        trade = {
            'Action': action,
            'Price': price,
            'Date': date,
            'Position Size': position_size
        }
        self.records.append(trade)

    def calculate_profit_loss(self):
        total_profit_loss = 0
        for trade in self.records:
            if trade['Action'] == 'BUY':
                total_profit_loss -= trade['Price'] * trade['Position Size']
            elif trade['Action'] == 'SELL':
                total_profit_loss += trade['Price'] * trade['Position Size']
        return total_profit_loss

    def print_records(self):
        for trade in self.records:
            print(f"Action: {trade['Action']}, Price: {trade['Price']}, Date: {trade['Date']}, Position Size: {trade['Position Size']}")
            # print(f"Action: {trade['Action']}, Price: {trade['Price']}, Date: {trade['Date']}")