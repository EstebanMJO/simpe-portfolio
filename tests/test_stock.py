import pytest
from src.stock import Stock


def test_stock_initialization():
    stock = Stock("AAPL", 150)
    assert stock.symbol == "AAPL"
    assert stock.price == 150


def test_stock_update_price():
    stock = Stock("AAPL", 150)
    stock.current_price(155)
    assert stock.price == 155


def test_stock_invalid_price():
    with pytest.raises(ValueError):
        Stock("AAPL", -150)


def test_stock_invalid_symbol():
    with pytest.raises(ValueError):
        Stock(12, 150)


def test_stock_invalid_price_update():
    stock = Stock("AAPL", 150)
    with pytest.raises(ValueError):
        stock.current_price(-155)


def test_stock_singleton():
    stock1 = Stock("AAPL", 150)
    stock2 = Stock("AAPL", 155)
    assert stock1 is stock2
    assert stock1.price == 155  # The price should be updated to the latest one
    assert stock2.price == 155
    assert stock1.symbol == "AAPL"
    assert stock2.symbol == "AAPL"


def test_stock_singleton_lowercase_symbols():
    stock1 = Stock("aapl", 150)
    stock2 = Stock("AAPL", 155)
    assert stock1 is stock2
    assert stock1.price == 155  # The price should be updated to the latest one
    assert stock2.price == 155
    assert stock1.symbol == "AAPL"
    assert stock2.symbol == "AAPL"


def test_stock_singleton_different_symbols():
    stock1 = Stock("AAPL", 150)
    stock2 = Stock("GOOGL", 155)
    assert stock1 is not stock2
    assert stock1.price == 150
    assert stock2.price == 155
    assert stock1.symbol == "AAPL"
    assert stock2.symbol == "GOOGL"