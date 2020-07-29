#a simple example of the api

from YahooFinanceAPI import StockAPI as api
import matplotlib.pyplot as plt  

api.setDebugMode(True)
api.initializStockData("BAC")

data = api.getHistoricalDataPast30TradingDays("BAC")
closeData = data["close"]
closeData.reverse()

plt.plot(closeData)
plt.show()