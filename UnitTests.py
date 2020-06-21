from YahooFinanceAPI import YahooFinanceAPI as api

api.setDebugMode(True)
api.initializStockData("AAL")
api.getStockPriceAtClose("AAL")
# api.getStockPriceAfterHours("AAL")
api.getPercentageChangeAtClose("AAL")
api.getPointChangeAtClose("AAL")
api.getPreviousClose('AAL')
api.getOpen("AAL")
api.getDayLow("AAL")
api.getDayHigh("AAL")
api.get52WeekLow("AAL")
api.get52WeekHigh("AAL")
