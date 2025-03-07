import threading
import random
import time

# Maximum tickers allowed in the system.
MAX_TICKERS = 1024

# Global list to hold ticker order books.
# Each order book is maintained in a TickerBook object.
ticker_books = []  # Contains TickerBook objects

#----------------------------------------------------------------------------
# Order and TickerBook classes
#----------------------------------------------------------------------------

class Order:
    def __init__(self, order_type, ticker, quantity, price):
        self.order_type = order_type  # 'Buy' or 'Sell'
        self.ticker = ticker
        self.quantity = quantity
        self.price = price
        # Timestamp to help preserve FIFO order among orders with the same price.
        self.timestamp = time.time()

class TickerBook:
    def __init__(self, ticker):
        self.ticker = ticker
        # Buy orders are kept sorted in descending order (highest price first).
        self.buy_orders = []  
        # Sell orders are kept sorted in ascending order (lowest price first).
        self.sell_orders = [] 

#----------------------------------------------------------------------------
# Helper functions
#----------------------------------------------------------------------------

def insert_sorted(order_list, order, reverse=False):
    """
    Insert the order into order_list such that the list remains sorted.
    If reverse is True, sort descending (for Buy orders); else ascending (for Sell orders).
    In case of equal price, earlier orders (by timestamp) come first.
    """
    index = 0
    while index < len(order_list):
        current = order_list[index]
        if reverse:
            # For buys, higher price comes first.
            if order.price > current.price:
                break
            elif order.price == current.price and order.timestamp < current.timestamp:
                break
        else:
            # For sells, lower price comes first.
            if order.price < current.price:
                break
            elif order.price == current.price and order.timestamp < current.timestamp:
                break
        index += 1
    order_list.insert(index, order)

def find_ticker_book(ticker):
    """
    Searches the global ticker_books list for the given ticker.
    If not found and the limit is not reached, creates a new TickerBook.
    """
    for book in ticker_books:
        if book.ticker == ticker:
            return book
    if len(ticker_books) < MAX_TICKERS:
        new_book = TickerBook(ticker)
        ticker_books.append(new_book)
        return new_book
    else:
        print("Max tickers reached!")
        return None

#----------------------------------------------------------------------------
# Order entry and matching functions
#----------------------------------------------------------------------------

def addOrder(order_type, ticker, quantity, price):
    """
    Adds an order to the order book for the given ticker.
    The order is inserted in sorted order:
      - Buy orders in descending order by price.
      - Sell orders in ascending order by price.
    """
    book = find_ticker_book(ticker)
    if book is None:
        return
    order = Order(order_type, ticker, quantity, price)
    if order_type == 'Buy':
        insert_sorted(book.buy_orders, order, reverse=True)
    elif order_type == 'Sell':
        insert_sorted(book.sell_orders, order, reverse=False)
    else:
        print("Unknown order type:", order_type)

def matchOrder():
    """
    Scans each ticker's order book and matches orders according to:
      Buy price >= lowest Sell price.
    Matching is performed in a loop until no further matches exist.
    When matching, the trade quantity is the minimum of the two orders’ quantities,
    and orders with zero quantity left are removed.
    This routine runs in O(n) time relative to the number of orders in each ticker book.
    """
    # Loop through each ticker book.
    for book in ticker_books:
        # Continue matching while there is at least one buy and one sell,
        # and the highest buy price meets the lowest sell price.
        while (book.buy_orders and book.sell_orders and 
               (book.buy_orders[0].price >= book.sell_orders[0].price)):
            buy_order = book.buy_orders[0]
            sell_order = book.sell_orders[0]
            trade_qty = min(buy_order.quantity, sell_order.quantity)
            # For simplicity, execute the trade at the sell order price.
            trade_price = sell_order.price
            print(f"Trade executed for {book.ticker}: {trade_qty} units at price {trade_price}")

            # Adjust order quantities.
            buy_order.quantity -= trade_qty
            sell_order.quantity -= trade_qty

            # Remove orders that have been fully filled.
            if buy_order.quantity == 0:
                del book.buy_orders[0]
            if sell_order.quantity == 0:
                del book.sell_orders[0]

#----------------------------------------------------------------------------
# Wrapper functions to simulate active trading with threads.
#----------------------------------------------------------------------------

def random_order_wrapper():
    """
    Continuously creates random orders.
    Ticker names are generated as "TICKER0" ... "TICKER1023" to support up to MAX_TICKERS.
    """
    tickers = [f"TICKER{i}" for i in range(MAX_TICKERS)]
    while True:
        order_type = random.choice(['Buy', 'Sell'])
        ticker = random.choice(tickers)
        quantity = random.randint(1, 100)
        price = round(random.uniform(10, 500), 2)
        addOrder(order_type, ticker, quantity, price)
        # Sleep for a short random duration to simulate real-time activity.
        time.sleep(random.uniform(0.01, 0.1))

def matching_thread_func():
    """
    Periodically calls matchOrder to process the order book.
    """
    while True:
        matchOrder()
        time.sleep(0.05)

#----------------------------------------------------------------------------
# Main simulation: spawn threads for order entry and matching.
#----------------------------------------------------------------------------

if __name__ == "__main__":
    # Start several threads that add orders concurrently.
    adder_threads = []
    for _ in range(5):  # For example, 5 concurrent order-entry threads.
        t = threading.Thread(target=random_order_wrapper, daemon=True)
        t.start()
        adder_threads.append(t)
    
    # Start one thread to continuously match orders.
    matcher_thread = threading.Thread(target=matching_thread_func, daemon=True)
    matcher_thread.start()
    
    # Keep the simulation running.
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Simulation terminated.")
