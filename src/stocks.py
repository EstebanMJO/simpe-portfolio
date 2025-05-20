'''
This module contains Stock and StockCollection classes. I decided to modularize
the code to make it easier to test and maintain.

The Stock class is implemented as a Singleton to ensure that only one instance
of each stock exists. This is useful for managing stock prices and ensuring
that the same stock is not duplicated in the portfolio and also avoid having
one stock with different prices.

The StockCollection class is used to manage a collection of stocks. It allows
to create a collection of stocks from a dictionary of stock symbols and
quantities or from a dictionary of stock symbols, allocations and total value.
I decided to implement this class to make it easier to manage a collection of
stocks and to provide a way to calculate the total value of the collection
and the allocation of each stock in the collection.
'''

from src.utils import get_valid_symbol, check_valid_allocation
import math


class Stock:
    '''
    This class represents a stock with a symbol and price.It is implemented as
    a Singleton to ensure only one instance of each stock exists.
    '''

    # This class variable holds the instances of the stocks
    _instances = {}

    @classmethod
    def exists_instance(cls, symbol: str) -> bool:
        '''
        This method checks if an instance of the stock with the given symbol
        already exists.
        '''
        symbol = get_valid_symbol(symbol)
        return symbol in cls._instances

    def __new__(cls, symbol: str, price: float = None):
        '''
        This method is called every time a new instance of the class is created.
        It checks if an instance with the same symbol already exists.
        If it does, it returns the existing instance.
        '''
        symbol = get_valid_symbol(symbol)

        # If the stock already exists, return the existing instance
        if cls.exists_instance(symbol):
            stock = cls._instances[symbol]

            # If the price is provided update the existing instance.
            if price is not None:
                stock.update_price(price)

            print(f"Returning existing stock instance of {symbol}")
            return stock

        # If the stock does not exist and price is None, raise an error
        if price is None:
            raise ValueError(
                f'''Stock {symbol} not found. Price must be provided to create
                a new instance.''')

        # If the stock does not exist, create a new instance and store it in
        # the class variable
        stock = super(Stock, cls).__new__(cls)
        stock._initialize(symbol, price)
        cls._instances[symbol] = stock
        return stock

    def _initialize(self, symbol: str, price: float):
        '''
        This method initializes the instance with the symbol and price.
        It is called only once when the instance is created.
        '''
        # If the price is not valid, raise an error
        if price <= 0:
            raise ValueError("Price must be greater than zero")

        print(f"Creating new stock instance for {symbol} with price {price}")
        self.price = price
        self.symbol = symbol

    def update_price(self, price: float):
        '''
        This method updates the price of the stock.
        '''
        # Check if the price is valid
        if price <= 0:
            raise ValueError("Price must be greater than zero")

        print(f"Updating price for {self.symbol} from {self.price} to {price}")
        self.price = price


class StockCollection:
    '''
    The main objective of this class is to handle a group of stocks. You can
    create a collection of stocks from a dictionary of stock symbols and
    quantities or from a dictionary of stock symbols, allocations and total
    value.
    The class also provides methods modify the collection of stocks and
    calculate its main properties, such as the total value and the allocation
    of each stock in the collection.
    '''
    def __init__(
            self, *,   # the * is used to force the use of keyword arguments
            stocks_qty: dict[str: float] = {},
            stocks_allocation: dict[str: float] = None,
            total_value: float = None):
        '''
        This method initializes the collection with the stocks and their
        quantities.
        '''
        self.stocks = {}

        if stocks_allocation is not None and total_value is not None:
            print('Creating stock collection using stocks_allocation')
            self._create_from_allocation(stocks_allocation, total_value)

        else:
            print('Creating stock collection using stocks_qty')
            self._create_from_qty(stocks_qty)

    def __eq__(self, other):
        '''
        This method is used to compare two stock collections. It returns True
        if the collections have the same stocks and quantities.
        '''

        if not isinstance(other, StockCollection):
            return False

        if len(self.stocks) != len(other.stocks):
            return False

        if set(self.stocks.keys()) != set(other.stocks.keys()):
            return False

        is_equal = True
        for stock, qty in self.stocks.items():
            if not math.isclose(other.stocks[stock], qty):
                is_equal = False
                break

        return is_equal

    def set_stock_qty(self, symbol: str, quantity: float) -> None:
        '''
        This method sets the quantity of a stock in the collection.
        '''

        if not isinstance(quantity, (int, float)):
            raise ValueError("Quantity must be a number")

        if not Stock.exists_instance(symbol):
            raise ValueError('''Stock {symbol} not created. Please instanciate
                             the stock first.''')

        if quantity <= 0:
            raise ValueError("Quantity must be a number greater than zero")

        stock = Stock(symbol)
        self.stocks[stock] = quantity

    def _create_from_qty(self, stocks_qty: dict[str: float]):
        '''
        This method creates a collection of stocks from a dictionary.
        The stock_qty dictionary must have the stock symbol as the key and the
        quantity as the value.
        '''
        for symbol, qty in stocks_qty.items():
            self.set_stock_qty(symbol, qty)

    def _create_from_allocation(self,
                                stocks_allocation: dict[str: float],
                                total_value: float):
        '''
        This method creates a collection of stocks from is allocation and total
        value.
        The stock_allocation dictionary must have the stock symbol as the key
        and the allocation as the value. The allocation is the percentage of }
        the total value of the collection (it should sum 1).
        '''
        check_valid_allocation(stocks_allocation)

        for stock, allocation in stocks_allocation.items():
            if not isinstance(stock, Stock):
                stock = Stock(stock)

            stock_value = allocation * total_value
            stock_qty = stock_value / stock.price
            self.stocks[stock] = stock_qty

    def get_value(self) -> float:
        '''
        This method returns the total value of the stocks in the collection.
        '''
        total_value = sum(
            stock.price * qty for stock, qty in self.stocks.items())

        return total_value

    def get_allocation(self) -> dict[Stock: float]:
        '''
        This method returns the allocation of the stocks in the collection.
        The allocation is the percentage of each stock in the total value of
        the collection.
        '''
        allocation = {}
        total_value = self.get_value()
        for stock, qty in self.stocks.items():
            allocation[stock] = qty*stock.price / total_value

        return allocation

    def delete_stock(self, stock: Stock) -> None:
        '''
        This method deletes a stock from the collection.
        '''
        if not isinstance(stock, Stock):
            raise ValueError(
                f"Stock {stock} is not a valid stock instance.")

        if stock not in self.stocks:
            raise ValueError(
                f"Stock {stock} not found in the collection.")

        del self.stocks[stock]

    def get_stocks_set(self) -> set[Stock]:
        '''
        This method returns a set of stocks in the collection.
        '''
        return set(self.stocks.keys())

    def modify_stock_qty(self, stock: Stock, qty: float) -> None:
        '''
        This method modifies the quantity of a stock in the collection.
        '''
        if not isinstance(stock, Stock):
            raise ValueError(
                f"Stock {stock} is not a valid stock instance.")

        if stock not in self.stocks:
            current_qty = 0
        else:
            current_qty = self.stocks[stock]
        target_qty = current_qty + qty
        if target_qty < 0:
            raise ValueError(f'''Not enough quantity of stock {stock} to modify.
                Current quantity: {current_qty}, modification: {qty}''')

        if target_qty == 0:
            self.delete_stock(stock)

        else:
            self.stocks[stock] = target_qty
