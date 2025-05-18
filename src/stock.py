
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
        return self.price


class StockCollection:
    '''
    This class represents a collection of stocks. This class should ensure the
    integrity of the stocks in the collection.
    '''

    def __init__(self, dict: dict[Stock: float] = None):
        '''
        This method initializes the collection with a dictionary of stocks.
        The dictionary should have the stock as the key and the quantity as the
        value.
        '''

        self.stocks = {}
        for stock, quantity in dict.items():
            self.add_stock(stock, quantity)

    def add_stock(self, stock: Stock, quantity: float):
        '''
        This method adds a stock to the collection.
        '''
        if not isinstance(stock, Stock):
            raise ValueError("Stock must be an instance of Stock class")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if stock.symbol in self.stocks:
            self.stocks[stock.symbol] += quantity
        else:
            self.stocks[stock.symbol] = quantity

    def remove_stock(self, stock: Stock, quantity: float):
        '''
        This method removes a stock from the collection.
        '''
        if not isinstance(stock, Stock):
            raise ValueError("Stock must be an instance of Stock class")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if stock.symbol not in self.stocks:
            raise ValueError("Stock not found in collection")

        if self.stocks[stock.symbol] < quantity:
            raise ValueError("Not enough stock to remove")

        self.stocks[stock.symbol] -= quantity

        if self.stocks[stock.symbol] == 0:
            del self.stocks[stock.symbol]