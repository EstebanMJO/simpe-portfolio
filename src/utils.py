
def get_valid_symbol(symbol: str):
    '''
    This method checks if the symbol is valid.
    The symbol is valid if it is a string and it is in uppercase.
    '''
    if not isinstance(symbol, str):
        raise ValueError("Symbol must be a string")

    symbol = symbol.upper()

    return symbol


def check_valid_allocation(stocks_allocation: dict[str: float]):

    if sum(stocks_allocation.values()) != 1:
        raise ValueError("The sum of the allocations must be equal to 1")

    for symbol, allocation in stocks_allocation.items():
        if not isinstance(allocation, (int, float)):
            raise ValueError("Allocation must be a number")

        if allocation <= 0:
            raise ValueError("Allocation must be a number greater than zero")
