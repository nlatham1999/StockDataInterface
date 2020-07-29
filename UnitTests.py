from YahooFinanceAPI import StockAPI as api

def unitTest(t, message, file):
    if(t is None):
        file.write(message + "\n")
        return 0
    else:
        return 1

api.setDebugMode(False)

file = open("UnitTestOutput.txt", "w")
i = 0

i += unitTest(api.initializStockData("AAL"), "Failed trying to initialize AAL", file)
# i += unitTest(api.initializStockDataFromJson("AAL"), "failed trying to initialize data from Json file", file) 
i += unitTest(api.getStockPriceAtClose("AAL"), "Failed trying to get the closing price", file)
i += unitTest(api.getStockPriceAfterHours("AAL"), "Failed trying to get the after hours price", file)
i += unitTest(api.getPercentageChangeAtClose("AAL"), "Failed trying to get the percentage change at close", file)
i += unitTest(api.getPointChangeAtClose("AAL"), "Failed trying to get the point change at close", file)
i += unitTest(api.getPercentageChangeAfterHours("AAL"), "Failed trying to get the percentage change after hours", file)
i += unitTest(api.getPointChangeAfterHours("AAL"), "Failed trying to get the point change after hours", file)
i += unitTest(api.getPreviousClose('AAL'), "Failed trying to get the previous close", file)
i += unitTest(api.getOpen("AAL"), "Failed trying the get the open price", file)
i += unitTest(api.getDayLow("AAL"), "Failed trying to get the day low", file)
i += unitTest(api.getDayHigh("AAL"), "Failed trying to the day high", file)
i += unitTest(api.get52WeekLow("AAL"), "Failed trying to get the 52 week low", file)
i += unitTest(api.get52WeekHigh("AAL"), "Failed trying to get the 52 week high", file)
i += unitTest(api.getVolume("AAL"), "Failed trying to get the volume", file)
i += unitTest(api.getAverageVolume("AAL"), "Failed trying to get the average volume", file)
i += unitTest(api.getMarketCap("AAL"), "Failed trying to get the market cap", file)
i += unitTest(api.getHistoricalDataAll("AAL"), "Failed trying to get the historical data", file)
# i += unitTest(api.getHistoricalDataThisWeek("AAL"), "Failed trying to get the historical data for this week", file)
i += unitTest(api.getHistoricalDataPast5TradingDays("AAL"), "Failed trying to get past 5 days data", file)
i += unitTest(api.getHistoricalDataRangeOfDates("AAL", "2020-07-01", "2020-07-24"), "Failed trying to get range of dates data", file)

file.write(str(i)+ " tests passed without errors")

file.close()