'''
This test file is for testing the SockCollection class.
It contains tests for the initialization and its methods.
'''

import pytest
import math
from src.stocks import StockCollection
from src.stocks import Stock


@pytest.fixture
def stock_singleton():
    Stock(symbol='S100', price=100)
    Stock(symbol='S200', price=200)
    Stock(symbol='S300', price=300)
    return Stock


def test_initialization_empty(stock_singleton):
    stock_collection = StockCollection()
    assert isinstance(stock_collection, StockCollection)
    assert len(stock_collection.stocks) == 0


def test_initialization_from_qty(stock_singleton):
    stock_collection = StockCollection(stocks_qty={'S100': 1,
                                                   'S200': 1})
    assert isinstance(stock_collection, StockCollection)
    assert len(stock_collection.stocks) == 2
    assert stock_collection.stocks[Stock('S100')] == 1
    assert stock_collection.stocks[Stock('S200')] == 1


def test_initialization_from_allocation(stock_singleton):
    stock_collection = StockCollection(stocks_allocation={'S100': 0.5,
                                                          'S200': 0.5},
                                       total_value=1000.0)

    assert isinstance(stock_collection, StockCollection)
    assert len(stock_collection.stocks) == 2

    assert math.isclose(stock_collection.get_value(), 1000)

    assert stock_collection.stocks[Stock('S100')] == 5
    assert stock_collection.stocks[Stock('S200')] == 2.5


def test_set_stock_qty(stock_singleton):
    stock_collection = StockCollection()
    stock_collection.set_stock_qty('S100', 10)
    assert stock_collection.stocks[Stock('S100')] == 10
    assert math.isclose(stock_collection.get_value(), 1000)

    stock_collection.set_stock_qty('S200', 20)
    assert stock_collection.stocks[Stock('S200')] == 20
    assert stock_collection.stocks[Stock('S100')] == 10
    assert math.isclose(stock_collection.get_value(), 5000)

    stock_collection.set_stock_qty('S100', 5)
    assert stock_collection.stocks[Stock('S100')] == 5
    assert math.isclose(stock_collection.get_value(), 4500)


def test_set_stock_qty_invalid(stock_singleton):
    stock_collection = StockCollection()

    with pytest.raises(ValueError):
        stock_collection.set_stock_qty('S100', -10)
    with pytest.raises(ValueError):
        stock_collection.set_stock_qty('S100', 0)
    with pytest.raises(ValueError):
        stock_collection.set_stock_qty('S100', 'invalid')
    with pytest.raises(ValueError):
        stock_collection.set_stock_qty(123, 10)


def test_get_stocks_set(stock_singleton):
    stock_collection = StockCollection(stocks_qty={'S100': 1,
                                                   'S200': 1})

    assert len(stock_collection.get_stocks_set()) == 2
    assert Stock('S100') in stock_collection.get_stocks_set()
    assert Stock('S200') in stock_collection.get_stocks_set()
    assert Stock('S300') not in stock_collection.get_stocks_set()


def test_delete_stock(stock_singleton):
    stock_collection = StockCollection(stocks_qty={'S100': 1,
                                                   'S200': 1})
    stock_collection.delete_stock(Stock('S100'))
    assert len(stock_collection.stocks) == 1
    assert Stock('S100') not in stock_collection.get_stocks_set()
    assert Stock('S200') in stock_collection.get_stocks_set()

    with pytest.raises(ValueError):
        stock_collection.delete_stock('S300')


def test_modify_stock_qty(stock_singleton):
    stock_collection = StockCollection(stocks_qty={'S100': 1,
                                                   'S200': 1})
    stock_collection.modify_stock_qty(Stock('S100'), 2)
    assert stock_collection.stocks[Stock('S100')] == 3

    stock_collection.modify_stock_qty(Stock('S300'), 2)
    assert stock_collection.stocks[Stock('S300')] == 2

    stock_collection.modify_stock_qty(Stock('S300'), -2)
    assert Stock('S300') not in stock_collection.get_stocks_set()

    with pytest.raises(ValueError):
        stock_collection.modify_stock_qty(Stock('S100'), -10)
