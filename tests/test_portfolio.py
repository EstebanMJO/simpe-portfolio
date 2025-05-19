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
def even_allocation_stockcollection(stocks):
    stock_collection = StockCollection(stocks_allocation={'S100': 1/3,
                                                          'S200': 1/3,
                                                          'S300': 1/3},
                                       total_value=1000.0)
    return stock_collection


@pytest.fixture
def even_allocation(stocks, even_allocation_stockcollection):

    return even_allocation_stockcollection.get_allocation()


@pytest.fixture
def same_qty_stockcollection(stocks):
    stock_collection = StockCollection(stocks_qty={'S100': 1,
                                                   'S200': 1,
                                                   'S300': 1})
    return stock_collection


@pytest.fixture
def same_qty_allocation(stocks, same_qty_stockcollection):

    return same_qty_stockcollection.get_allocation()


def test_portfolio_initialization(stocks, same_qty_stockcollection):
    portfolio = Portfolio(
        name='Test Portfolio',
        stocks_collection=same_qty_stockcollection)

    assert isinstance(portfolio, Portfolio)
    assert portfolio.name == 'Test Portfolio'
    assert portfolio.stocks_collection == same_qty_stockcollection
    assert math.isclose(portfolio.stocks_collection.get_value(), 600)


def test_invert_money(stocks, same_qty_stockcollection, same_qty_allocation):
    '''
    This tests the invert_money method of the Portfolio class. The invert_money
    method is used to invert money in the portfolio. The method should update
    the qty of the stocks in the portfolio while keeping the stocks allocation.
    '''
    portfolio = Portfolio(
        name='Test Portfolio',
        stocks_collection=same_qty_stockcollection)

    portfolio.invert_money(1000)
    assert math.isclose(portfolio.stocks_collection.get_value(), 1600)
    assert len(portfolio.stocks_collection.get_allocation()) == \
        len(same_qty_allocation)

    portfolio_allocation = portfolio.stocks_collection.get_allocation()
    for stock, allocation in portfolio_allocation.items():
        assert math.isclose(allocation, same_qty_allocation[stock])


def test_retire_money(stocks, same_qty_stockcollection,
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
        stocks_collection=same_qty_stockcollection)

    portfolio.retire_money(300)
    assert math.isclose(portfolio.stocks_collection.get_value(), 300)
    assert len(portfolio.stocks_collection.get_allocation()) == \
        len(same_qty_allocation)

    portfolio_allocation = portfolio.stocks_collection.get_allocation()
    for stock, allocation in portfolio_allocation.items():
        assert math.isclose(allocation, same_qty_allocation[stock])

    with pytest.raises(ValueError):
        portfolio.retire_money(1000)


def test_get_stocks_qty_deviation(stocks,
                                  same_qty_stockcollection,
                                  even_allocation_stockcollection,
                                  even_allocation):
    '''
    This tests the get_stocks_qty_deviation method of the Portfolio class. The
    get_stocks_qty_deviation method is used to get the deviation of the stocks
    qty in the portfolio. The method should return a dictionary with the stock
    symbol as the key and the deviation as the value.
    '''
    portfolio = Portfolio(
        name='Test Portfolio',
        stocks_collection=same_qty_stockcollection)

    assert math.isclose(portfolio.stocks_collection.get_value(), 600)

    portfolio.invert_money(400)
    assert math.isclose(portfolio.stocks_collection.get_value(), 1000)

    portfolio.set_allocation_target(even_allocation)

    deviation = portfolio.get_stocks_qty_deviation()

    for stock, stock_deviation in deviation.items():
        target_deviation = even_allocation_stockcollection.stocks[stock] - \
            same_qty_stockcollection.stocks[stock]

        assert math.isclose(stock_deviation, target_deviation)



