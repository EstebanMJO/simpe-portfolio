import pytest


@pytest.fixture
def stocks_allocation():
    allocation = {'META': 0.4,
                  'APPL': 0.6}
    return allocation


def test_allocation(stocks_allocation):
    assert stocks_allocation['META'] == 0.4
