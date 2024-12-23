def filter_div_yield(stock):
    return float(stock.get("dividend_yield", 0)) >= 8

def filter_portfolio_lvr(stock):
    return float(stock.get("portfolio_lvr", 0)) > 30

def filter_price_near_atl(stock):
    current_price = float(stock.get("current_price", 0))
    ATL = float(stock.get("ATL", 0))
    return percentage_difference(current_price, ATL) <= 20

def percentage_difference(a, b):
    return abs(a - b) / ((a + b) / 2) * 100

def main():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    cursor.execute("SELECT code, name_x, dividend_yield, portfolio_lvr, current_price, ATL FROM LVR")
    rows = cursor.fetchall()

    filtered_stocks = []

    for row in rows:
        stock = {
            "code": row[0],
            "name": row[1],
            "dividend_yield": row[2],
            "portfolio_lvr": row[3],
            "current_price": row[4],
            "ATL": row[5]
        }

        # Skip rows with None values
        if any(v is None for v in stock.values()):
            continue

        if all([
            filter_div_yield(stock),
            filter_portfolio_lvr(stock),
            filter_price_near_atl(stock)
        ]):
            filtered_stocks.append(stock)

    if filtered_stocks:
        print("Stocks that meet the criteria:")
        for stock in filtered_stocks:
            print(stock)

        # Export to JSON file
        with open("filtered_securities_w_margin.json", "w") as f:
            json.dump(filtered_stocks, f, indent=4)
    else:
        print("No stocks meet the criteria.")

if __name__ == "__main__":
    main()
