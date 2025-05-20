'''
This test file aims to test the Portfolio class. Here we will test the system
as a whole, including the StockCollection class and the Stock class.
'''

import pytest
import math
from src.stocks import StockCollection, Stock
from src.portfolio import Portfolio


@pytest.fixture
def stocks():
    Stock(symbol='S100', price=100)
    Stock(symbol='S200', price=200)
    Stock(symbol='S300', price=300)
    return Stock


@pytest.fixture
def even_allocation(stocks) -> dict[Stock: float]:
    return {Stock('S100'): 1/3,
            Stock('S200'): 1/3,
            Stock('S300'): 1/3}


@pytest.fixture
def even_allocation_stockcollection(stocks, even_allocation) -> StockCollection:

    stock_collection = StockCollection(stocks_allocation=even_allocation,
                                       total_value=1000)
    return stock_collection


@pytest.fixture
def same_qty_allocation(stocks) -> dict[Stock: float]:
    return {Stock('S100'): 1/6,
            Stock('S200'): 1/3,
            Stock('S300'): 1/2}


@pytest.fixture
def same_qty_stockcollection(stocks, same_qty_allocation) -> StockCollection:
    stock_collection = StockCollection(stocks_allocation=same_qty_allocation,
                                       total_value=1000)
    return stock_collection


def test_portfolio_initialization(stocks,
                                  same_qty_allocation,
                                  same_qty_stockcollection):
    '''
    This test creates a portfolio with a collection of stocks whith same qty
    stocks (total value = 1000). The portfolio should be initialized with the
    the same qty allocation.
    '''

    portfolio = Portfolio(
        name='Test Portfolio',
        stocks_allocation=same_qty_allocation,
        total_value=1000)

    assert isinstance(portfolio, Portfolio)
    assert portfolio.name == 'Test Portfolio'
    assert portfolio.stocks_collection == same_qty_stockcollection
    assert math.isclose(portfolio.stocks_collection.get_value(), 1000)


def test_invest_money(stocks,
                      same_qty_allocation):
    '''
    This tests the invert_money method of the Portfolio class. The invert_money
    method is used to invert money in the portfolio. The method should update
    the qty of the stocks in the portfolio while keeping the stocks allocation.
    '''
    portfolio = Portfolio(
        name='Test Portfolio',
        stocks_allocation=same_qty_allocation,
        total_value=600)

    portfolio.invest_money(1000)
    assert math.isclose(portfolio.stocks_collection.get_value(), 1600)

    portfolio_allocation = portfolio.stocks_collection.get_allocation()
    for stock, allocation in portfolio_allocation.items():
        assert math.isclose(allocation, same_qty_allocation[stock])


def test_retire_money(stocks,
                      same_qty_allocation):
    '''
    This tests the retire_money method of the Portfolio class. The retire_money
    method is used to retire money from the portfolio. The method should update
    the qty of the stocks in the portfolio while keeping the stocks allocation.
    It should also raise a ValueError if the amount to retire is greater than
    the total value of the portfolio.
    '''
    portfolio = Portfolio(
        name='Test Portfolio',
        stocks_allocation=same_qty_allocation,
        total_value=600)

    portfolio.retire_money(300)
    assert math.isclose(portfolio.stocks_collection.get_value(), 300)

    portfolio_allocation = portfolio.stocks_collection.get_allocation()
    for stock, allocation in portfolio_allocation.items():
        assert math.isclose(allocation, same_qty_allocation[stock])

    with pytest.raises(ValueError):
        portfolio.retire_money(1000)


def test_set_allocation_target(stocks,
                               same_qty_allocation,
                               even_allocation):
    '''
    This tests the set_allocation_target method of the Portfolio class.
    '''
    portfolio = Portfolio(
        name='Test Portfolio',
        stocks_allocation=same_qty_allocation,
        total_value=600)

    portfolio.set_allocation_target(even_allocation)

    assert portfolio.allocation_target == even_allocation


def test_update_stocks_qty_target(stocks,
                                  even_allocation,
                                  same_qty_allocation,
                                  even_allocation_stockcollection):
    '''
    This test creates a portfolio with a collection of stocks whith same qty
    stocks (total value = 1000).

    Then, it changes the allocation target to even allocation and updates the
    stocks qty target. The stocks qty target should be the same as the
    even_allocation_stockcollection.
    '''
    portfolio = Portfolio(
        name='Test Portfolio',
        stocks_allocation=same_qty_allocation,
        total_value=1000)

    portfolio.set_allocation_target(even_allocation)
    portfolio.update_stocks_qty_target()

    assert portfolio.stocks_qty_target == even_allocation_stockcollection


def test_get_stocks_qty_deviation(stocks,
                                  same_qty_allocation,
                                  same_qty_stockcollection,
                                  even_allocation_stockcollection,
                                  even_allocation):
    '''
    This test creates a portfolio with a collection of stocks whith same qty
    stocks (total value = 1000).

    Then, it changes the allocation target to even allocation and get the stocks
    qty deviation. The deviation should be the same as the difference between
    same_qty_stockcollection and even_allocation_stockcollection.
    '''

    portfolio = Portfolio(
        name='Test Portfolio',
        stocks_allocation=same_qty_allocation,
        total_value=1000)

    portfolio.set_allocation_target(even_allocation)

    deviation = portfolio.get_stocks_qty_deviation()

    for stock, stock_deviation in deviation.items():
        target_deviation = even_allocation_stockcollection.stocks[stock] - \
            same_qty_stockcollection.stocks[stock]

        assert math.isclose(stock_deviation, target_deviation)


def test_rebalance(stocks,
                   even_allocation,
                   same_qty_stockcollection,
                   same_qty_allocation):
    '''
    This test creates a portfolio with a collection of stocks whith same qty
    stocks (total value = 1000).

    Then, it changes the allocation target to even allocation and rebalances the
    portfolio. The stocks collection should be the same as the
    even_allocation_stockcollection while mantainng the portfolio value.
    '''
    portfolio = Portfolio(
        name='Test Portfolio',
        stocks_allocation=even_allocation,
        total_value=1000)

    portfolio.set_allocation_target(same_qty_allocation)
    portfolio.rebalance()
    assert math.isclose(portfolio.stocks_collection.get_value(), 1000)

    assert portfolio.stocks_collection == same_qty_stockcollection


def test_update_stock_price(stocks):
    '''
    This test updates the stock price and checks if the portfolio updates the
    allocation to reflect the new prices.
    '''
    stock_1 = Stock('TEST1', price=600)
    stock_2 = Stock('TEST2', price=400)

    portfolio = Portfolio(
        name='Test Portfolio',
        stocks_allocation={'TEST1': 0.6,
                           'TEST2': 0.4},
        total_value=1000)

    portfolio_allocation = portfolio.stocks_collection.get_allocation()
    portfolio.set_allocation_target(portfolio_allocation)

    assert math.isclose(portfolio_allocation[stock_1], 0.6)
    assert math.isclose(portfolio_allocation[stock_2], 0.4)
    assert math.isclose(portfolio.allocation_target[stock_1], 0.6)
    assert math.isclose(portfolio.allocation_target[stock_2], 0.4)

    # Updating the stock prices
    stock_1.update_price(400)
    stock_2.update_price(600)

    assert math.isclose(portfolio.stocks_collection.get_value(), 1000)

    portfolio_allocation = portfolio.stocks_collection.get_allocation()

    assert math.isclose(portfolio_allocation[stock_1], 0.4)
    assert math.isclose(portfolio_allocation[stock_2], 0.6)
    assert math.isclose(portfolio.allocation_target[stock_1], 0.6)
    assert math.isclose(portfolio.allocation_target[stock_2], 0.4)

    # Rebalancing the portfolio
    stock_1.update_price(1200)
    stock_2.update_price(800)
    assert math.isclose(portfolio.stocks_collection.get_value(), 2000)
