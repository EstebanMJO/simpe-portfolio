
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

    def __new__(cls, symbol: str, price: float):
        '''
        This method is called every time a new instance of the class is created.
        It checks if an instance with the same symbol already exists.
        If it does, it returns the existing instance.
        '''
        symbol = symbol.upper()  # Ensure the symbol is in uppercase
        # If the stock already exists, return the existing instance
        if symbol in cls._instances:
            stock = cls._instances[symbol]
            # Update the price of the existing stock instance
            if price != stock.price:
                stock.current_price(price)

            print(f"Returning existing stock instance of {symbol}")
            return stock

        # If the stock does not exist, create a new instance and store it in
        # the class variable
        stock = super(Stock, cls).__new__(cls)
        # Initialize the instance with the symbol and price
        stock._initialize(symbol, price)
        cls._instances[symbol] = stock
        return stock

    def _initialize(self, symbol: str, price: float):
        '''
        This method initializes the instance with the symbol and price.
        It is called only once when the instance is created.
        '''
        print(f"Creating new stock instance for {symbol} with price {price}")
        self.symbol = symbol.upper()  # Ensure the symbol is in uppercase
        self.price = price

    def current_price(self, price: float):
        '''
        This method updates the price of the stock.
        '''
        # Check if the price is valid
        if price <= 0:
            raise ValueError("Price must be greater than zero")

        print(f"Updating price for {self.symbol} from {self.price} to {price}")
        self.price = price
        return self.price
