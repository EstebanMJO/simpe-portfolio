'''
Simple demo of a portfolio manager.
'''

from src.portfolio import Portfolio
from src.stocks import Stock
import os
import yaml

ALLOCATION_PATH = 'data/allocations'
STOCKS_FILE = 'data/stocks.yaml'


def create_stocks(stocks_file):
    '''
    This function instantiate the stocks in the stocks.yaml file.
    '''
    with open(stocks_file, 'r') as f:
        stocks = yaml.safe_load(f)
        for symbol, price in stocks.items():
            Stock(symbol=symbol, price=price)


def print_allocations_list(allocations_list: list[str],
                           allocations_path) -> None:
    print('Available allocations:')
    for indx, file in enumerate(allocations_list):
        if file.endswith('.yaml'):
            with open(os.path.join(allocations_path, file), 'r') as f:
                data = yaml.safe_load(f)
                print(f'    - {data['name']}: {indx}')


def get_allocations_list(allocations_path: str) -> list[str]:
    '''
    This function returns a list of all the allocation files in the
    allocations_path directory.
    '''
    allocations_list = os.listdir(allocations_path)
    return allocations_list


def select_allocation(allocation_path):
    print('Please choose an allocation from the list below:')
    print('--------------------------------------------------')

    allocations = get_allocations_list(allocation_path)
    print_allocations_list(allocations, allocation_path)

    allocation_number = input('Enter the number of the allocation file: ')
    while True:
        if allocation_number.isdigit():
            allocation_number = int(allocation_number)
            if allocation_number < len(allocations):
                break
            else:
                print('Invalid number. Please try again.')
                print_allocations_list(allocations, allocation_path)
                allocation_number = input(
                    'Enter the number of the allocation file: ')
        else:
            print('Invalid input. Please enter a number.')
            print_allocations_list(allocations, allocation_path)
            allocation_number = input(
                'Enter the number of the allocation file: ')

    allocation_file = allocations[allocation_number]
    allocation_file_path = os.path.join(allocation_path, allocation_file)

    with open(allocation_file_path, 'r') as f:
        data = yaml.safe_load(f)

    return data


def main():

    create_stocks(STOCKS_FILE)
    print('Welcome to the Portfolio Manager!')
    print('Let\'s create a new portfolio.')

    allocation_data = select_allocation(ALLOCATION_PATH)
    name = allocation_data['name']
    stocks_allocation = allocation_data['allocation']

    portfolio_value = input(
        f'Enter how much money do you want to invest in {name}?')

    while True:
        try:
            portfolio_value = float(portfolio_value)
            if portfolio_value > 0:
                break
            else:
                print('Invalid input. Please enter a positive number.')
                portfolio_value = input(
                    f'Enter how much money do you want to invest in {name}?')
        except ValueError:
            print('Invalid input. Please enter a number.')
            portfolio_value = input(
                f'Enter how much money do you want to invest in {name}?')

    portfolio = Portfolio(
        name=name,
        stocks_allocation=stocks_allocation,
        total_value=portfolio_value)

    print(f'You invested {portfolio_value} in {name} successfully!')

    print('--------------------------------------------------')
    print('Want to change your risk profile?')
    print('Let\'s change the allocation of the portfolio:')
    allocation_data = select_allocation(ALLOCATION_PATH)

    stocks_allocation = allocation_data['allocation']
    portfolio.set_allocation_target(stocks_allocation)
    deviation = portfolio.get_stocks_qty_deviation()

    print(f'You changed the allocation target of the portfolio to {name}!')

    print('To rebalance the portfolio we need to do the following:')
    print('--------------------------------------------------')
    for stock, qty in deviation.items():
        if qty > 0:
            print('Buy {:.5f}  of {}'.format(qty, stock.symbol))
        elif qty < 0:
            print('Sell {:.5f} of {}'.format(-qty, stock.symbol))
        else:
            print(f'No action needed for {stock.symbol}')
    print('--------------------------------------------------')


if __name__ == '__main__':
    main()
