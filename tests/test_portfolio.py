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
    stock_collection = StockCollection(stocks_allocation={'S100': 0.5,
                                                          'S200': 0.5},
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

