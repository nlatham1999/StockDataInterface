A Python API for Yahoo Finance

scrapes Yahoo Finance and collects stock data:

current functionalities:

  -initializeStockData(symbol)  - takes in a stock symbol and collects the needed data to be processed. If the symbol is invalid or the connection refused then None is returned

  -getStockPrice(Symbol)        - takes in the stock symobol and gets the stock price. If no data is available or if the stock has not been initialized then None is returned 

  -getChangeAtClose(Symbol)     -takes in the stock symbol and returns the point change and percentage change in an array. If no data is available or if the stock has not been initialized then None is returned 

  -getPointChangeAtClose(Symbol) - takes in the stock symbol and returns the point change at close. If no data is available or if the stock has not been initialized then None is returned 

  -getPercentageChangeAtClose(Symbol) - takes in the stock symbol and returns the percentage change at close. If no data is available or if the stock has not been initialized then None is returned 

  -getPreviousClose(Symbol) - takes in the stock symbol and returns the previous close price. If no data is available or if the stock has not been initialized then None is returned 

  