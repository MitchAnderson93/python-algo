import os
import sys
import pandas as pd

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from system.utils.common import log_message
import logging
import yfinance as yf
logging.getLogger("yfinance").setLevel(logging.CRITICAL)

def get_dividend_yield(stock_info, current_price):
    """Get dividend yield from Yahoo Finance with manual verification flag."""
    try:
        info = stock_info.info
        if 'dividendYield' in info and info['dividendYield'] is not None:
            div_yield = round(info['dividendYield'] * 100, 2)
            if div_yield > 15:  # Flag suspicious yields
                log_message(f"Warning: High dividend yield ({div_yield}%) detected for {stock_info.ticker}. Please verify manually.")
            return div_yield
    except Exception as e:
        log_message(f"Error getting dividend yield from Yahoo Finance: {e}")
        return None

def calculate_metrics(stock_code):
    stock_data = yf.download(stock_code, period="max", progress=False)
    if stock_data.empty:
        log_message(f"{stock_code} is empty or delisted.")
        return {
            'RSI14': None,
            'SMA20': None,
            'SMA50': None,
            'SMA200': None,
            'dividend_yield': None,
            'ATH': None,
            'ATL': None,
            'current_price': None
        }
    
    stock_info = yf.Ticker(stock_code)

    delta = stock_data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    RS = gain / loss
    RSI = 100 - (100 / (1 + RS))
    SMA20 = stock_data['Close'].rolling(window=20).mean()
    SMA50 = stock_data['Close'].rolling(window=50).mean()
    SMA200 = stock_data['Close'].rolling(window=200).mean()

    ATH = stock_data['Close'].max()
    ATL = stock_data['Close'].min()
    current_price = stock_data['Close'].iloc[-1]

    dividend_yield = get_dividend_yield(stock_info, current_price)

    return {
        'RSI14': RSI.iloc[-1],
        'SMA20': SMA20.iloc[-1],
        'SMA50': SMA50.iloc[-1],
        'SMA200': SMA200.iloc[-1],
        'dividend_yield': dividend_yield,
        'ATH': ATH,
        'ATL': ATL,
        'current_price': current_price
    }