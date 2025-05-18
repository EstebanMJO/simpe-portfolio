from stock import StockCollection


class Portfolio:
    def __init__(self,
                 name: str,
                 stocks_collection: StockCollection) -> None:

        self.name = name
        self.stocks_collection = stocks_collection
        self.allocation_target = StockCollection()

    def set_allocation_target(self,
                              allocation_target: dict[str, float]) -> None:
        """
        This method sets the allocation target for the portfolio.
        The allocation target is a dictionary with the stock symbol as the
        key and the target quantity as the value.
        """
        portfolio_value = self.stocks_collection.get_value()

        self.allocation_target = StockCollection(
            stocks_qty=allocation_target,
            target_value=portfolio_value)

    def get_allocation_deviation(self):

        deviation = {}

        target_stocks = self.allocation_target.get_stocks_set()
        current_stocks = self.stocks_collection.get_stocks_set()

        modified_stocks = target_stocks.intersection(current_stocks)
        new_stocks = target_stocks - current_stocks
        removed_stocks = current_stocks - target_stocks

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
