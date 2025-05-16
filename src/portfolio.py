from src.stock import Stock


class Portfolio:
    def __init__(self, name: str, stocks_collection: dict = None):
        self.name = name
        self.stocks_collection = {}
        self.allotcation_target = {}

    def add_stock(self, stock: Stock, quantity: float):
        if stock in self.stocks_collection:
            self.stocks_collection[stock] += quantity
        else:
            self.stocks_collection[stock] = quantity

    def remove_stock(self, stock: Stock, quantity: float):
        # Check if the stock exists in the portfolio
        if stock not in self.stocks_collection:
            raise ValueError("Stock not found in portfolio")

        # Check if the quantity to remove is valid
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        # Check if the stock quantity is sufficient
        if self.stocks_collection[stock] < quantity:
            raise ValueError("Not enough stock to remove")

        # Remove the stock from the portfolio
        self.stocks_collection[stock] -= quantity

        # If the stock quantity is zero, remove it from the portfolio
        if self.stocks_collection[stock] == 0:
            del self.stocks_collection[stock]

    def _is_balanced(self):
        return self.stocks_collection == self.allotcation_target

    def rebalance(self):
        if self._is_balanced():
            print("Portfolio is already balanced.")
            return
