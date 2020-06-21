from YahooFinanceAPI import YahooFinanceAPI as api

api.setDebugMode(True)
api.initializStockData("AAL")
api.getStockPriceAtClose("AAL")
# api.getStockPriceAfterHours("AAL")
api.getPercentageChangeAtClose("AAL")
api.getPointChangeAtClose("AAL")
api.getPreviousClose('AAL')