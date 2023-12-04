import sqlite3
import json

def percentage_difference(a, b):
    return abs(a - b) / ((a + b) / 2) * 100

def filter_price_near_atl(stock):
    current_price = float(stock.get("current_price", 0))
    ATL = float(stock.get("ATL", 0))
    return percentage_difference(current_price, ATL) <= 10

def filter_dividend_yield(stock):
    return float(stock.get("dividend_yield", 0)) > 8

def main():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    # Select relevant columns from the 'asx' table
    cursor.execute("SELECT code, name, current_price, ATL, dividend_yield FROM asx")
    rows = cursor.fetchall()

    filtered_stocks = []

    for row in rows:
        stock = {
            "code": row[0],
            "name": row[1],
            "current_price": row[2],
            "ATL": row[3],
            "dividend_yield": row[4]
        }

        # Skip rows with None values
        if any(v is None for v in stock.values()):
            continue

        if all([
            filter_price_near_atl(stock),
            filter_dividend_yield(stock)
        ]):
            filtered_stocks.append(stock)

    if filtered_stocks:
        print("Stocks that meet the criteria:")
        for stock in filtered_stocks:
            print(stock)

        # Export to JSON file
        with open("filtered_asx_whole.json", "w") as f:
            json.dump(filtered_stocks, f, indent=4)
    else:
        print("No stocks meet the criteria.")

if __name__ == "__main__":
    main()
