from utils import get_valid_symbol


class Stock:
    '''
    This class represents a stock with a symbol and price.
    It is implemented as a Singleton to ensure only one instance of each stock
    exists. This is useful for managing stock prices and ensuring that the same
    stock is not duplicated in the portfolio and also avoid having one stock
    with different prices.
    '''

    # This class variable holds the instances of the stocks
    _instances = {}

    @classmethod
    def exists_instance(cls, symbol: str) -> bool:
        '''
        This method checks if an instance of the stock with the given symbol
        already exists.
        '''
        # Check if the symbol is valid
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
        symbol = get_valid_symbol(symbol)

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

    def get_all_instances(self):
        '''
        This method returns all the instances of the stocks.
        '''
        return self._instances

    def get_stock_symbol(self):
        '''
        This method returns the symbol of the stock.
        '''
        return self.symbol


class StockCollection:

    def __init__(self,
                 stocks_qty: dict[str: float] = {},
                 target_value: float = None):
        '''
        This method initializes the collection with the stocks and their
        quantities.
        The stocks_qty parameter is a dictionary with the stock symbol as the
        key and the quantity as the value.
        The target_value parameter is the total value of the stocks in the
        collection. If it is provided, the quantities will be scaled
        according to the target value.
        '''

        self.stocks = {}
        self.create_from_qty(stocks_qty)

        # If the total value is provided, scale the quantities
        # according to the total value

        if target_value is not None:
            print(f"Scaling stocks to target value {target_value}")
            self.scale_stocks(target_value)

    def set_stock_qty(self, symbol: str, quantity: float) -> None:
        '''
        This method sets the quantity of a stock in the collection.
        '''

        if not Stock.exists_instance(symbol):
            raise ValueError(
                f"Stock {symbol} not found. Please create the stock first.")

        if quantity <= 0 or not isinstance(quantity, (int, float)):
            raise ValueError("Quantity must be a number greater than zero")

        stock = Stock(symbol)
        self.stocks[stock] = quantity

    def create_from_qty(self, stocks_qty: dict[str: float]):
        '''
        This method creates a collection of stocks from a dictionary.
        The dictionary must have the stock symbol as the key and the quantity
        as the value.
        '''
        for symbol, qty in stocks_qty.items():
            self.set_stock_qty(symbol, qty)

    def scale_stocks(self, target_value: float):
        '''
        This method scales the stocks according to the total value.
        '''
        current_value = self.get_value()

        if target_value <= 0:
            raise ValueError("Target value must be greater than zero")

        for stock, qty in self.stocks.items():
            # Scale the quantity according to the target value
            target_qty = qty * target_value / current_value
            self.set_stock_qty(stock.symbol, target_qty)

    def get_value(self):
        '''
        This method returns the total value of the stocks in the collection.
        '''
        total_value = sum(
            stock.price * qty for stock, qty in self.stocks.items())

        return total_value

    def get_allocation(self):
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

    def delete_stock(self, symbol: str) -> None:
        '''
        This method deletes a stock from the collection.
        '''
        if not Stock.exists_instance(symbol):
            raise ValueError(
                f"{symbol} is not a Stock")

        stock = Stock(symbol)
        if stock not in self.stocks:
            raise ValueError(
                f"Stock {symbol} not found in the collection.")

        del self.stocks[stock]

    def get_stocks_set(self):
        '''
        This method returns the set of stocks in the collection.
        '''
        return set(self.stocks.keys())

    def modify_stock_qty(self, symbol: str, qty: float) -> None:
        '''
        This method modifies the quantity of a stock in the collection.
        '''
        if not Stock.exists_instance(symbol):
            raise ValueError(
                f"Stock {symbol} not found. Please create the stock first.")

        stock = Stock(symbol)
        cuurent_qty = self.stocks[stock]
        if cuurent_qty + qty < 0:
            raise ValueError(
                f'''
                Stock {symbol} quantity cannot be negative.
                Current quantity: {cuurent_qty}, modification: {qty}''')

        self.stocks[stock] = qty
