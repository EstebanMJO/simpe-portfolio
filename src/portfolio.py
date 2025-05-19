from src.stock import StockCollection
from src.utils import check_valid_allocation


class Portfolio:
    def __init__(self,
                 name: str,
                 stocks_collection: StockCollection) -> None:

        self.name = name
        self.stocks_collection = stocks_collection
        self.stocks_qty_target = {}
        self.allocation_target = {}

    def set_allocation_target(self,
                              allocation_target: dict[str: float]) -> None:
        check_valid_allocation(allocation_target)
        self.allocation_target = allocation_target

    def update_stocks_qty_target(self) -> None:
        '''
        This method sets the allocation target for the portfolio.
        '''
        portfolio_value = self.stocks_collection.get_value()
        self.stocks_qty_target = StockCollection(
            stocks_allocation=self.allocation_target,
            total_value=portfolio_value)

    def get_allocation_deviation(self):

        self.update_stocks_qty_target()
        deviation = {}

        target_stocks = self.stocks_qty_target.get_stocks_set()
        current_stocks = self.stocks_collection.get_stocks_set()

        modified_stocks = target_stocks.intersection(current_stocks)
        new_stocks = target_stocks - current_stocks
        removed_stocks = current_stocks - target_stocks

        for stock in modified_stocks:
            target_qty = self.stocks_qty_target.stocks[stock]
            current_qty = self.stocks_collection.stocks[stock]
            deviation[stock] = current_qty - target_qty

        for stock in new_stocks:
            target_qty = self.stocks_qty_target.stocks[stock]
            deviation[stock] = -target_qty

        for stock in removed_stocks:
            current_qty = self.stocks_collection.stocks[stock]
            deviation[stock] = current_qty

        return deviation
