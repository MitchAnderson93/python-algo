from system.common import yf, log_message

def calculate_metrics(stock_code):
    stock_data = yf.download(stock_code, period="5y", progress=False)
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

    one_year_ago = stock_info.history(period="1y").index[0]
    dividends_past_year = stock_info.dividends.loc[one_year_ago:]
    ttm_dividends = dividends_past_year.sum()
    dividend_yield = (ttm_dividends / current_price) * 100

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