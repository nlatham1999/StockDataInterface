A Python API for Yahoo Finance

A fast, easy API that retrieves stock data from Yahoo Finance.
Data can be initialized by scraping data from yahoo finance or by reading from a json file saved by a previous session.
Data collected includes current data as well as all historical data for a stock up to the past 50 years.
Unlike other APIs that collect data from Yahoo Finance this API has built in easy to use functions to filter collected data.

current functionalities:

  - initializeStockData(symbol)  - takes in a stock symbol and collects the needed data to be processed. If the symbol is invalid or the connection refused then None is returned

  - initializeStockDataFRomJson - initializes the stock data from a previously generated json doc. Returns None if now json doc is available.

  - getStockPrice(Symbol)        - takes in the stock symobol and gets the stock price. If no data is available or if the stock has not been initialized then None is returned 

  - getStockPriceAfterHours(Symbol) - takes in the stock symobol and gets the stock price after hours. If no data is available or if the stock has not been initialized then None is returned 

  - getChangeAtClose(Symbol)     -takes in the stock symbol and returns the point change and percentage change in an array. If no data is available or if the stock has not been initialized then None is returned 

  - getPointChangeAtClose(Symbol) - takes in the stock symbol and returns the point change at close. If no data is available or if the stock has not been initialized then None is returned 

  - getPercentageChangeAtClose(Symbol) - takes in the stock symbol and returns the percentage change at close. If no data is available or if the stock has not been initialized then None is returned 

  - getPointChangeAfterHours(Symbol) - takes in the stock symbol and returns the point change after hours. If no data is available or if the stock has not been initialized then None is returned 

  - getPercentageChangeAfterHours(Symbol) - takes in the stock symbol and returns the percentage change after hours. If no data is available or if the stock has not been initialized then None is returned 

  - getPreviousClose(Symbol) - takes in the stock symbol and returns the previous close price. If no data is available or if the stock has not been initialized then None is returned 

  - getOpen(Symbol) - takes in the stock symbol and returns the open price. If no data is available or if the stock has not been initialized then None is returned 

  - getDayRange(Symbol) - takes in the stock symbol and returns the day's high and low as an array. If no data is available or if the stock has not been initialized then None is returned 

  - getDayLow(Symbol) - takes in the stock symbol and returns the day's low. If no data is available or if the stock has not been initialized then None is returned 

  - getDayHigh(Symbol) - takes in the stock symbol and returns the day's high. If no data is available or if the stock has not been initialized then None is returned 

  - get52WeekRange(Symbol) - takes in the stock symbol and returns the 52 week's high and low as an array. If no data is available or if the stock has not been initialized then None is returned 

  - get52WeekLow(Symbol) - takes in the stock symbol and returns the 52 week's low. If no data is available or if the stock has not been initialized then None is returned 

  - get52WeekHigh(Symbol) - takes in the stock symbol and returns the 52 week's high. If no data is available or if the stock has not been initialized then None is returned

  - getVolume(Symbol) - takes in the stock symbol and returns the volume. If no data is available or if the stock has not been initialized then None is returned

  - getAverageVolume(Symbol) - takes in the stock symbol and returns the average volume. If no data is available or if the stock has not been initialized then None is returned


  - getMarketCap(Symbol) - takes in the stock symbol and returns the market cap. If no data is available or if the stock has not been initialized then None is returned

  - getHistoricalDataAll(symbol) - takes in the stock symbol and returns all historical data in a dict with keys being "open", "low", "close", "high" holding the historical data in an array from most recent to least recent. If no data is available or if the stock has not been initialized then None is returned

  - getHistoricalDataRangeTradingDays(symbol, num1, num2) - takes in the stock symbol and a range of days and returns the historical data in a dict with keys being "open", "low", "close", "high" holding the historical data in an array from most recent to least recent. If no data is available or if the stock has not been initialized then None is returned

  - getHistoricalDataPastXTradingDays(symbol, num1) - takes in the stock symbol and the past number of days and returns the historical data in a dict with keys being "open", "low", "close", "high" holding the historical data in an array from most recent to least recent. If no data is available or if the stock has not been initialized then None is returned

  - getHistoricalDataPast5TradingDays(symbol) - takes in the stock symbol returns the historical data of the past five days in a dict with keys being "open", "low", "close", "high" holding the historical data in an array from most recent to least recent. If no data is available or if the stock has not been initialized then None is returned

  - getHistoricalDataPast30TradingDays(symbol) - takes in the stock symbol returns the historical data of the past thirty days in a dict with keys being "open", "low", "close", "high" holding the historical data in an array from most recent to least recent. If no data is available or if the stock has not been initialized then None is returned

  - getHistoricalDataRangeOfDates(symbol, date1, date2) - takes in the stock symbol and a range of dates in "YYYY-MM-DD" format and returns the historical data in a dict with keys being "open", "low", "close", "high" holding the historical data in an array from most recent to least recent. If no data is available or if the stock has not been initialized then None is returned
