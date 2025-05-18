from stock import Stock


class Portfolio:
    def __init__(self,
                 name: str = 'Risky Norris',
                 stocks_collection: dict[str: float] = None) -> None:

        self.name = name
        self.stocks_collection = self.set_stocks_from_dict(stocks_collection)
        self.stocks_allocation = self.get_portfolio_allocation()
        self.allocation_target = {}

    def set_stocks_from_dict(self, stocks_collection: dict[str: float]):
        '''
        This method sets the stocks collection from a dictionary of stocks
        symbols as key and quantity as value.
        '''
        if len(stocks_collection) == 0:
            raise ValueError("The stocks collection cannot be empty")

        for symbol, quantity in stocks_collection.items():
            self.set_stock_qty(symbol, quantity)

    def set_stock_qty(self, symbol: str, quantity: float) -> None:
        '''
        This method sets the quantity of a stock in the collection.
        '''

        if not Stock.exists_instance(symbol):
            raise ValueError(
                f"Stock {symbol} not found. Please create the stock first.")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        stock = Stock(symbol)
        self.stocks_collection[stock] = quantity

    def delete_stock(self, stock: Stock) -> None:
        '''
        This method deletes a stock from the collection.
        '''

        del self.stocks_collection[stock]

    def get_portfolio_valuation(self):

        total_value = sum(stock.price * qty
                          for stock, qty in self.stocks_collection.items())
        return total_value

    def get_portfolio_allocation(self):

        allocation = {}
        total_value = self.get_portfolio_valuation()
        for stock, qty in self.stocks_collection.stocks.items():
            allocation[stock] = qty*stock.price / total_value

        return allocation

    def set_portfolio_target_allocation(self,
                                        allocation_target: dict[str: float]):

        # Check if the stock allocation is valid
        sum_allocation = sum(allocation_target.values())
        if sum_allocation != 1:
            raise ValueError("The sum of the allocation must be equal to 1")

        for symbol, allocation in allocation_target.items():
            self.set_stock_allocation(symbol, allocation)

    def set_stock_allocation(self, symbol: str, allocation: float):

        # Check if the stock allocation is valid
        if allocation < 0 or allocation > 1:
            raise ValueError("The allocation must be between 0 and 1")

        # Check if the stock exists in the collection
        if not Stock.exists_instance(symbol):
            raise ValueError(
                f"Stock {symbol} not found. Please create the stock first.")

        # Set the stock allocation
        stock = Stock(symbol)
        self.allocation_target[stock] = allocation

    def get_target_stock_collection(self):
        target_collection = {}
        portfolio_valuation = self.get_portfolio_valuation()
        for stock, allocation in self.allocation_target.items():
            stock_target_value = allocation * portfolio_valuation
            target_collection[stock] = stock_target_value / stock.price

        return target_collection

    def get_allocation_deviation(self):

        deviation = {}

        target_stocks = self.get_target_stock_collection()

        target_stocks_symbols = target_stocks.get_stocks_set()
        current_stocks = self.stocks_collection.get_stocks_set()

        modified_stocks = target_stocks_symbols.intersection(current_stocks)
        new_stocks = target_stocks_symbols - current_stocks
        removed_stocks = current_stocks - target_stocks_symbols

        for stock in modified_stocks:
            target_qty = self.allocation_target.stocks[stock]
            current_qty = self.stocks_collection.stocks[stock]
            deviation[stock] = current_qty - target_qty

        for stock in new_stocks:
            target_qty = self.allocation_target.stocks[stock]
            deviation[stock] = -target_qty

        for stock in removed_stocks:
            current_qty = self.stocks_collection.stocks[stock]
            deviation[stock] = current_qty

        return deviation

    def is_balanced(self):
        return self.stocks_allocation == self.allocation_target



