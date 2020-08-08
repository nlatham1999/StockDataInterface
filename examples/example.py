#a simple example of the api

from StockDataInterface import StockDataInterface as api
import matplotlib.pyplot as plt  

api.setDebugMode(True)
api.initializStockData("AAPL")

data = api.getHistoricalDataPast30TradingDays("AAPL")
closeData = data["close"]
closeData.reverse()

plt.plot(closeData)
plt.show()