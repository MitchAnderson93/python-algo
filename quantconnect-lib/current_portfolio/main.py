''' 
Portfolio 1 - Allocation (100K)
    10% GOV BACKED BONDS (GOV)
    90% Split across:
        40% Australian equities (VAS)
        15% Property (VAP)
        30% International equity (VTS)
        15% Fixed interest (VAF/BOND)
    
Dollar cost averaged weekly
Dividends via DRP

Portfolio 2 - Allocation (150k cash)
    self.bitcoin_allocation = 0.35 (52,500)
    self.ethereum_allocation = 0.27 (40,500)
    self.cardano_allocation = 0.13 (19,500)
    self.polkadot_allocation = 0.10 (15,000)
    self.sol_allocation = 0.10 (15,000)
    self.dog_allocation = 0.3 (4,500)
    self.whole_market = 0.2 (3,000)

    Timeframe June 2021 - Dec 2021

Portfolio 3 - Longshot/HIO 0.035
    Bulk dollar cost (7.5k per buy)
    Target entry: under 0.040 (0.037)
    Target exit: at or over 0.055 (48.64% / $24,324.32)
    
Dollar cost averaged
Tiemframe: 6 months - expected high season Dec 


'''
from AlgorithmImports import *
from datetime import time
from QuantConnect import *
from QuantConnect.Algorithm import *

class CoinbaseStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2021, 6, 1)
        self.SetEndDate(2021, 12, 31)
        self.SetCash(150000)
        
        self.AddCrypto("ADAUSD", Resolution.Daily, Market.GDAX)
        self.AddCrypto("DOTUSD", Resolution.Daily, Market.GDAX)
        self.AddCrypto("ETHUSD", Resolution.Daily, Market.GDAX)
        self.AddCrypto("BTCUSD", Resolution.Daily, Market.GDAX)
        self.AddCrypto("DOGEUSD", Resolution.Daily, Market.GDAX)
        self.AddCrypto("SOLUSD", Resolution.Daily, Market.GDAX)
        
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.At(time(hour=10, minute=0)), self.Rebalance)
        
        self.bitcoin_allocation = 0.35
        self.ethereum_allocation = 0.27
        self.cardano_allocation = 0.13
        self.polkadot_allocation = 0.10
        self.sol_allocation = 0.10
        self.doge_allocation = 0.03
        self.whole_market_allocation = 0.02
        
        self.daily_budget = 200
    
    def Rebalance(self):
        if self.Portfolio.Invested:
            return
        
        total_allocation = self.daily_budget
        bitcoin_allocation_amount = total_allocation * self.bitcoin_allocation
        ethereum_allocation_amount = total_allocation * self.ethereum_allocation
        cardano_allocation_amount = total_allocation * self.cardano_allocation
        polkadot_allocation_amount = total_allocation * self.polkadot_allocation
        sol_allocation_amount = total_allocation * self.sol_allocation
        dogecoin_allocation_amount = total_allocation * self.doge_allocation
        whole_market_allocation_amount = total_allocation * self.whole_market_allocation
        
        self.MarketOrder("BTCUSD", bitcoin_allocation_amount)
        self.MarketOrder("ETHUSD", ethereum_allocation_amount)
        self.MarketOrder("ADAUSD", cardano_allocation_amount)
        self.MarketOrder("DOTUSD", polkadot_allocation_amount)
        self.MarketOrder("SOLUSD", sol_allocation_amount)
        self.MarketOrder("DOGEUSD", dogecoin_allocation_amount)
        
        self.BuyWholeMarket(whole_market_allocation_amount)
    
    def BuyWholeMarket(self, amount):
        available_symbols = self.Securities.Keys
        excluded_symbols = ["BTCUSD", "ETHUSD", "ADAUSD", "DOTUSD", "SOLUSD", "DOGEUSD"]
        buy_symbols = [symbol for symbol in available_symbols if symbol not in excluded_symbols]
        if len(buy_symbols) == 0:
            return
        
        allocation_per_symbol = amount / len(buy_symbols)
        
        for symbol in buy_symbols:
            self.MarketOrder(symbol, allocation_per_symbol)
