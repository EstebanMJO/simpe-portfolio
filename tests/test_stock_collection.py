from src.stocks import StockCollection
from src.stocks import Stock
import pytest


@pytest.fixture
def stock_singleton():
    Stock(symbol='S100', price=100)
    Stock(symbol='S200', price=200)
    Stock(symbol='S300', price=300)
    return Stock


def test_stock_collection_initialization(stock_singleton):
    stock_collection = StockCollection(stocks_qty={'S100': 1, 'S200': 1})
    assert isinstance(stock_collection, StockCollection)
    assert len(stock_collection.stocks) == 2


def test_stock_collection_initialization_empty(stock_singleton):
    stock_collection = StockCollection()
    assert isinstance(stock_collection, StockCollection)
    assert len(stock_collection.stocks) == 0


def test_stock_collection_initialization_allocation(stock_singleton):
    stock_collection = StockCollection(stocks_allocation={'S100': 0.5,
                                                          'S200': 0.5},
                                       total_value=1000.0)

    assert isinstance(stock_collection, StockCollection)
    assert len(stock_collection.stocks) == 2

    assert round(stock_collection.get_value(), 6) == 1000

    assert stock_collection.stocks[Stock('S100')] == 5
    assert stock_collection.stocks[Stock('S200')] == 2.5


def test_stock_collection_set_stock_qty(stock_singleton):
    stock_collection = StockCollection()
    stock_collection.set_stock_qty('S100', 10)
    assert stock_collection.stocks[Stock('S100')] == 10
    assert len(stock_collection.stocks) == 1
    stock_collection.set_stock_qty('S200', 20)
    assert stock_collection.stocks[Stock('S200')] == 20
    assert len(stock_collection.stocks) == 2


def test_stock_collection_set_stock_qty_invalid(stock_singleton):
    stock_collection = StockCollection()
    with pytest.raises(ValueError):
        stock_collection.set_stock_qty('S100', -10)
    with pytest.raises(ValueError):
        stock_collection.set_stock_qty('S100', 0)
    with pytest.raises(ValueError):
        stock_collection.set_stock_qty('S100', 'invalid')
    with pytest.raises(ValueError):
        stock_collection.set_stock_qty(123, 10)


def test_stock_collection_create_from_qty(stock_singleton):
    stock_collection = StockCollection()
    stock_collection.create_from_qty({'S100': 10, 'S200': 20})
    assert len(stock_collection.stocks) == 2
    assert stock_collection.stocks[Stock('S100')] == 10
    assert stock_collection.stocks[Stock('S200')] == 20

