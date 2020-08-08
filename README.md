# Table of Contents


- [About](#About)
- [Installation](#Installation)
- [Examples](#Examples)
- [Dependencies](#Dependencies)
- [Documentation](#Documentation)

---

# About

A fast, easy API that retrieves stock data from Yahoo Finance.
Data can be initialized by scraping data from yahoo finance or by reading from a json file saved by a previous session.
Data collected includes current data as well as all historical data for a stock up to the past 50 years.
Unlike other APIs that collect data from Yahoo Finance this API has built in easy to use functions to filter collected data.

---

# Installation

```shell
$ pip install StockDataInterface
```

---

# Examples

below are a couple code samples, for a complete list of funtions available consult the [documentation](#Documentation) 

 ```python
 #Nick Latham
 #8/7/2020
 #print and plot the close data of Apple from the past year

from StockDataInterface import api 
import matplotlib.pyplot as plt #(pip install matplotlib)

#first initialize the stock
api.initializStockData("AAPL")

#get the historical data from the past year
data = api.getHistoricalDataRangeOfDates("AAPL", "2019-08-07", "2020-08-07")

#get the close data into an array using the 'close' key
#keys available are 'open', 'low', 'close', 'high', 'volume', 'adjclose', and 'date'
closeData = data['close']

#we need to reverse the array because historical data is returned from most recent to least recent
closeData.reverse()

#plot and show the graph
plt.plot(closeData)
plt.show()

 ```

 ```python
 #Nick Latham
 #8/7/2020
 #compare close prices from Delta and United Airlines from the past 30 trading days

from StockDataInterface import api 
import matplotlib.pyplot as plt

#initialize the data
api.initializStockData("DAL")
api.initializStockData("UAL")

#get the data from the past 30 trading days
dataDAL = api.getHistoricalDataPast30TradingDays("DAL")
dataUAL = api.getHistoricalDataPast30TradingDays("UAL")

#only get the close data
closeDataDAL = dataDAL['close']
closeDataUAL = dataUAL["close"]

#reverse the arrays since we get the data from most recent to least recent
closeDataDAL.reverse()
closeDataUAL.reverse()

#plot  and show the data
plt.plot(closeDataDAL)
plt.plot(closeDataUAL)
plt.show()
 ```

---

# Dependencies
urllib3, BeautifulSoup, lxml, html5lib, datetime

---

# Documentation

  - initializeStockData(symbol)  - takes in a stock symbol and collects the needed data to be processed. If the symbol is invalid or the connection refused then None is returned

  - initializeStockDataFromJson - initializes the stock data from a previously generated json doc. Returns None if no json doc is available.

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
