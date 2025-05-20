![Flake8 Linting](https://github.com/EstebanMJO/simpe-portfolio/actions/workflows/lint.yml/badge.svg) ![Flake8 Linting](https://github.com/EstebanMJO/simpe-portfolio/actions/workflows/pytest.yml/badge.svg)

# simple-portfolio
Implementation of a simple stock portfolio. This repo was created following this instructions:

*Construct a simple Portfolio class that has a collection of Stocks. Assume each Stock has a “Current Price” method that receives the last available price. Also, the Portfolio class has a collection of “allocated” Stocks that represents the distribution of the Stocks the Portfolio is aiming (i.e. 40% META, 60% APPL)
Provide a portfolio rebalance method to know which Stocks should be sold and which ones should be bought to have a balanced Portfolio based on the portfolio’s allocation.
Add documentation/comments to understand your thinking process and solution*

# Repo sructure
## src/stocks
In the file stocks.py are implemented the classes Stock and StockCollection.
- The class Stock has a class variable that lists all instances of stocks created. This is usefull to avoid stocks duplicated. This objects has an attribute that stores the stock price and has the method to update it.
- The class StockCollection handles groups of stock. You can add, delete and modify stocks of the collection, and also, has methods to calculate the total value of the collection and its allocation.

## src/portfolio
In the file portfolio.py is implemented the class Portfolio. This objects can be initializated from a given allocation and the portfolio value. This class implements methods to invest/retire money, change the allocation target, get the stocks desviation from its target and a rebalance method that sell/buy stocks to meet the allocation target while maintaining the portfolio value.

## tests/*
In this directory are implemented some test to ensure that all classes are working as intended.

## main.py
This is a demo of the repo functionalities. This demo creates a portfolio and let you now which stocks you should sell and buy to meet a desired allocation.
You can add stocks allocations in the directory data/allocations/ as .yaml files. There a some already created (you may know some of those).
Also, you can modify the stocks prices and add new stocks in the file data/stocks.yaml. There are some real stocks prices and some random prices too (I didn't found all of them, I did't want to put much time in it).

