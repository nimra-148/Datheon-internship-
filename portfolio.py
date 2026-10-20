"""
Investment Portfolio Tracker
A simple command-line Python project that calculates stock investment value
and exports a portfolio summary to CSV.

Note: Built-in prices are sample/demo prices, not live market data.
"""

import csv
import os


SAMPLE_PRICES = {
    "AAPL": 195.50,
    "MSFT": 420.10,
    "GOOGL": 165.30,
    "TSLA": 250.75,
    "AMZN": 180.20,
    "META": 485.00,
    "NVDA": 950.00,
    "SPY": 510.25,
}


def load_market_prices():
    """Load prices from a supported CSV file, or use demo prices."""
    prices = {}
    possible_files = [
        "S&P 500 Ticker Dataset.csv",
        "sp500.csv",
        "tickers.csv",
        "sample_prices.csv",
    ]

    for filename in possible_files:
        if not os.path.exists(filename):
            continue

        try:
            with open(filename, "r", newline="", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    ticker = (
                        row.get("Ticker")
                        or row.get("Symbol")
                        or row.get("ticker")
                        or row.get("symbol")
                    )
                    price = (
                        row.get("Price")
                        or row.get("Current Price")
                        or row.get("Close")
                        or row.get("price")
                        or row.get("close")
                    )

                    if ticker and price:
                        try:
                            numeric_price = float(price)
                            if numeric_price > 0:
                                prices[ticker.strip().upper()] = numeric_price
                        except (TypeError, ValueError):
                            continue

            if prices:
                print(f"Loaded market prices from {filename}")
                return prices
        except (OSError, csv.Error):
            continue

    print("Using sample/demo prices (not live market data).")
    return SAMPLE_PRICES.copy()


def get_positive_float(prompt):
    """Ask until the user enters a positive number."""
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Please enter a number greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_positive_int(prompt):
    """Ask until the user enters a positive whole number."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Please enter a whole number greater than zero.")
        except ValueError:
            print("Invalid input. Please enter a valid whole number.")


def main():
    portfolio = {}
    market_prices = load_market_prices()

    print("\n=== Investment Portfolio Tracker ===")
    print("Enter stock holdings. Type 'done' when you have finished.\n")

    while True:
        ticker = input("Enter ticker symbol: ").strip().upper()

        if ticker in ("DONE", ""):
            break

        if not ticker.isalnum() and "." not in ticker and "-" not in ticker:
            print("Invalid ticker symbol. Try again.\n")
            continue

        buy_price = get_positive_float(f"  Buy price for {ticker} ($): ")
        quantity = get_positive_int(f"  Quantity for {ticker}: ")

        if ticker in portfolio:
            portfolio[ticker]["quantity"] += quantity
            # Combine purchases using a weighted average buy price.
            old_qty = portfolio[ticker]["quantity"] - quantity
            old_cost = portfolio[ticker]["buy_price"] * old_qty
            new_cost = buy_price * quantity
            portfolio[ticker]["buy_price"] = (old_cost + new_cost) / (old_qty + quantity)
        else:
            portfolio[ticker] = {"buy_price": buy_price, "quantity": quantity}

        print(f"  Added {ticker}.\n")

    if not portfolio:
        print("No holdings entered. Nothing to save.")
        return

    total_invested = 0.0
    total_current_value = 0.0
    rows_to_write = []

    print("\n--- Portfolio Summary ---")
    print(
        f"{'Ticker':<8} {'Qty':>6} {'Buy Price':>12} {'Current':>12} "
        f"{'Invested':>12} {'Value':>12} {'Gain/Loss':>12}"
    )
    print("-" * 80)

    for ticker, info in portfolio.items():
        buy_price = info["buy_price"]
        quantity = info["quantity"]

        # If no current price is available, use the buy price rather than
        # inventing a gain/loss estimate.
        current_price = market_prices.get(ticker, buy_price)
        invested = buy_price * quantity
        current_value = current_price * quantity
        gain_loss_pct = ((current_value - invested) / invested * 100) if invested else 0.0

        total_invested += invested
        total_current_value += current_value

        print(
            f"{ticker:<8} {quantity:>6} ${buy_price:>10.2f} "
            f"${current_price:>10.2f} ${invested:>10.2f} "
            f"${current_value:>10.2f} {gain_loss_pct:>10.2f}%"
        )

        rows_to_write.append([
            ticker,
            quantity,
            f"{buy_price:.2f}",
            f"{current_price:.2f}",
            f"{invested:.2f}",
            f"{current_value:.2f}",
            f"{gain_loss_pct:.2f}%",
        ])

    total_gain_loss = (
        (total_current_value - total_invested) / total_invested * 100
        if total_invested
        else 0.0
    )

    print("-" * 80)
    print(f"Total invested:       ${total_invested:.2f}")
    print(f"Total current value:  ${total_current_value:.2f}")
    print(f"Total gain/loss:      {total_gain_loss:.2f}%")

    output_file = "portfolio_summary.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Ticker",
            "Quantity",
            "Buy_Price",
            "Current_Price",
            "Total_Invested",
            "Current_Value",
            "Gain_Loss_Percentage",
        ])
        writer.writerows(rows_to_write)
        writer.writerow([])
        writer.writerow([
            "TOTAL", "", "", "",
            f"{total_invested:.2f}",
            f"{total_current_value:.2f}",
            f"{total_gain_loss:.2f}%",
        ])

    print(f"\nSummary saved to: {output_file}")
    print("Reminder: prices are sample data unless you provide a price CSV.")


if __name__ == "__main__":
    main()
