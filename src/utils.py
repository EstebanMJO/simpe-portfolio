
def get_valid_symbol(symbol: str):
    '''
    This method checks if the symbol is valid.
    The symbol is valid if it is a string and it is in uppercase.
    '''
    if not isinstance(symbol, str):
        raise ValueError("Symbol must be a string")

    symbol = symbol.upper()

    return symbol
