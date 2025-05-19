from src.stocks import StockCollection, Stock
from src.utils import check_valid_allocation


class Portfolio:
    def __init__(self,
                 name: str,
                 stocks_collection: StockCollection) -> None:
        '''
        This class represents a portfolio of stocks. It contains a collection
        of stocks and a target allocation for each stock. The target allocation
        is the percentage of the total value of the portfolio that should be
        allocated to each stock. The portfolio can be used to track the
        performance of the stocks and to rebalance the portfolio to meet the
        target allocation.
        '''
        self.name = name
        self.stocks_collection = stocks_collection
        self.stocks_qty_target = {}
        self.allocation_target = {}

    def set_allocation_target(self,
                              allocation_target: dict[str: float]) -> None:
        '''
        Sets the allocation target for the portfolio. The allocation target
        is a dictionary with the stock symbol as the key and the allocation
        as the value. The allocation is the percentage of the total value of
        the portfolio that should be allocated to each stock. The allocation
        target must sum to 1.
        '''
        check_valid_allocation(allocation_target)
        self.allocation_target = allocation_target

    def update_stocks_qty_target(self) -> None:
        '''
        This method sets the target quantity of stocks in the portfolio. The
        target quantity is calculated based on the target allocation and the
        total value of the portfolio.
        '''
        portfolio_value = self.stocks_collection.get_value()
        self.stocks_qty_target = StockCollection(
            stocks_allocation=self.allocation_target,
            total_value=portfolio_value)

    def get_stocks_qty_deviation(self) -> dict[Stock: float]:
        '''
        this method returns the deviation of the current stocks in the portfolio
        from the target stocks. The deviation is a dictionary with the stock
        symbol as the key and the deviation as the value.
        '''

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

    def get_rebalance(self) -> None:
        '''
        This method rebalances the portfolio to meet the target allocation.
        It sells stocks that are overallocated and buys stocks that are
        underallocated.
        '''
        deviation = self.get_stocks_qty_deviation()

        for stock, qty in deviation.items():
            self.stocks_collection.modify_stock_qty(stock, qty)

    def invert_money(self, value: float) -> None:
        '''
        This method inverts the money in the portfolio. It buys stocks to
        augment the portfolio value while keeping the previous allocation.
        '''
        current_allocation = self.stocks_collection.get_allocation()

        for stock in current_allocation.keys():
            stock_new_investment = current_allocation[stock] * value
            adding_stock_qty = stock_new_investment / stock.price

            self.stocks_collection.modify_stock_qty(
                stock, adding_stock_qty)

    def retire_money(self, value: float) -> None:
        '''
        This method retires money from the portfolio. It sells stocks to
        reduce the portfolio value while keeping the previous allocation.
        '''
        current_value = self.stocks_collection.get_value()
        if value > current_value:
            raise ValueError(
                f'''Cannot retire more money than the portfolio value:
                {current_value}''')

        current_allocation = self.stocks_collection.get_allocation()
        for stock in current_allocation.keys():
            stock_new_investment = current_allocation[stock] * value
            removing_stock_qty = stock_new_investment / stock.price

            self.stocks_collection.modify_stock_qty(
                stock, -removing_stock_qty)
