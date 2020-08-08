#Nick Latham
#6/21/2020
#An API for Yahoo Finance

import urllib3
from bs4 import BeautifulSoup
import lxml
import html5lib
import ast
import json
from datetime import datetime, timedelta

def testFuntion():
    print("test")

class StockDataInterface:

    stocks = dict()
    __debugMode = False

    #general scraper to get the url
    def scraper(url):
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, "lxml")
        return soup

    #sets the debug mode
    def setDebugMode(mode):
        StockDataInterface.__debugMode = mode

    def message(text):
        if(StockDataInterface.__debugMode):
            print(text)

    #takes in a stock symbol and stores the data. Use this every time you want to refresh
    def initializStockData(sym):
        xml = -1
        xmlHistorical = -1
        try:
            url = "https://finance.yahoo.com/quote/" + sym
            xml = StockDataInterface.scraper(url)
            
            url = "https://finance.yahoo.com/quote/"+sym+"/history?period1=1&period2=2000000000&interval=1d&filter=history&frequency=1d"
            xmlHistorical = StockDataInterface.scraper(url)
            StockDataInterface.message("Success initializing: " + sym)

        except:
            StockDataInterface.message("Error initializing: " + sym)
            return None
        stock = Stock(xml, xmlHistorical, sym)

        StockDataInterface.__initStockData(stock)

        StockDataInterface.stocks[sym] = stock

        StockDataInterface.writeToJson(sym)

        return True

    def __initStockData(stock):
        StockDataInterface.__initStockPriceAtClose(stock)
        StockDataInterface.__initStockPriceAfterHours(stock)
        StockDataInterface.__initChangeAtClose(stock)
        StockDataInterface.__initChangeAfterHours(stock)
        StockDataInterface.__initPreviousClose(stock)
        StockDataInterface.__initOpen(stock)
        StockDataInterface.__initDayRange(stock)
        StockDataInterface.__init52WeekRange(stock)
        StockDataInterface.__initVolume(stock)
        StockDataInterface.__initAverageVolume(stock)
        StockDataInterface.__initMarketCap(stock)
        StockDataInterface.__initHistoricalDataAll(stock)


    def writeToJson(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        file = open( sym + "_data.json", "w")
        data = {}
        data["symbol"] = stock.symbol
        data["price at close"] = stock.priceAtClose
        data["point change at close"] = stock.pointChangeAtClose
        data["percentage change at close"] = stock.percentageChangeAtClose
        data["price after hours"] = stock.priceAfterHours
        data["percentage change after hours"] = stock.percentageChangeAfterHours
        data["point change after hours"] = stock.pointChangeAfterHours
        data["previous close"] = stock.previousClose
        data["open price"] = stock.openPrice
        data["day range"] = stock.dayRange
        data["volume"] = stock.volume
        data["average volume"] = stock.averageVolume
        data["market cap"] = stock.marketCap
        data["52 week low"] = stock.yearRange[0]
        data["52 week high"] = stock.yearRange[1]
        data["historical data"] = stock.OHCL

        json.dump(data, file, indent=4) 

    def initializStockDataFromJson(sym):

        stock = Stock("", "", sym)

        try:
            fileName = sym + "_data.json"
            file = open(fileName, "r")
            data = json.load(file)
            stock.priceAtClose = data["symbol"]
            stock.priceAfterHours = data["price at close"]
            stock.pointChangeAtClose = data["point change at close"]
            stock.percentageChangeAtClose = data["percentage change at close"]
            stock.percentageChangeAfterHours = data["percentage change after hours"]
            stock.pointChangeAfterHours = data["point change after hours"]
            stock.previousClose = data["previous close"]
            stock.openPrice = data["open price"]
            stock.dayRange = data["day range"]
            stock.volume = data["volume"]
            stock.averageVolume = data["average volume"]
            stock.marketCap = data["market cap"]
            stock.yearRange = [data["52 week low"], data["52 week high"]]
            stock.OHCL = data["historical data"]
        except:
            StockDataInterface.message("error trying to read data from " + sym + "_data.json")
            return None

        StockDataInterface.stocks[sym] = stock

        return True

    def __initStockPriceAtClose(stock):
        try:
            xml = stock.xml.find_all("span", {"data-reactid": "50"})
            stock.priceAtClose = float(xml[0].string.strip().replace(",",""))
        except:
            StockDataInterface.message(stock.symbol + " close price data not currently available")

    def __initStockPriceAfterHours(stock):
        try:
            xml = stock.xml.find_all("span", {"data-reactid": "55"})
            stock.priceAfterHours = float(xml[0].string.strip().replace(",",""))
        except:
            StockDataInterface.message(stock.symbol + " after hours data not currently available")

    def __initChangeAtClose(stock):
        try:
            xml = stock.xml.find_all("span", {"data-reactid": "51"})
            temp = xml[0].string.strip().replace(",","")
            amountPoints = ""
            amountPercentage = ""
            i = 0
            while(i < len(temp) and temp[i] != '('):
                amountPoints += temp[i]
                i += 1
            i += 1
            while(i < len(temp) and temp[i] != '%'):
                amountPercentage += temp[i] 
                i += 1
            stock.pointChangeAtClose = float(amountPoints)
            stock.percentageChangeAtClose = float(amountPercentage)
        except:
            StockDataInterface.message(stock.symbol + " change at close data not currently available")

    def __initChangeAfterHours(stock):
        try:
            xml = stock.xml.find_all("span", {"data-reactid": "58"})
            temp = xml[0].string.strip().replace(",","")
            amountPoints = ""
            amountPercentage = ""
            i = 0
            while(i < len(temp) and temp[i] != '('):
                amountPoints += temp[i]
                i += 1
            i += 1
            while(i < len(temp) and temp[i] != '%'):
                amountPercentage += temp[i] 
                i += 1
            stock.pointChangeAfterHours = float(amountPoints)
            stock.percentageChangeAfterHours = float(amountPercentage)
        except:
            StockDataInterface.message(stock.symbol + " change after hours data not currently available")

    def __initPreviousClose(stock):
        try:
            xml = stock.xml.find_all("span", {"data-reactid": "98"})
            previousClose = float(xml[0].string.strip().replace(",",""))
            stock.previousClose = previousClose
        except:
            StockDataInterface.message(stock.symbol + " previous close data not currently available")

    def __initOpen(stock):
        try:
            xml = stock.xml.find_all("span", {"data-reactid" : "103"})
            openPrice = float(xml[0].string.strip().replace(",",""))
            stock.openPrice = openPrice
        except:
            StockDataInterface.message(stock.symbol + " open price data not currently available")

    def __initDayRange(stock):
        high = ""
        low = ""
        try:
            xml = stock.xml.find_all("td", {"data-reactid" : "117"})
            temp = xml[0].string.strip().replace(",","")
            i = 0
            while(i < len(temp) and temp[i] != " "):
                low += temp[i]
                i += 1
            i += 3
            while(i < len(temp)):
                high += temp[i]
                i+= 1
            dayRange = [float(low), float(high)]
            stock.dayRange = dayRange
        except:
            StockDataInterface.message(stock.symbol + " day range data not currently available")

    def __init52WeekRange(stock):
        high = ""
        low = ""
        try:
            xml = stock.xml.find_all("td", {"data-reactid" : "121"})
            temp = xml[0].string.strip().replace(",","")
            i = 0
            while(i < len(temp) and temp[i] != " "):
                low += temp[i]
                i += 1
            i += 3
            while(i < len(temp)):
                high += temp[i]
                i+= 1
            yearRange = [float(low), float(high)]
            stock.yearRange = yearRange
        except:
            StockDataInterface.message("52 week range data not currently available")

    def __initVolume(stock):
        volume = stock.getDataElement("126", "volume data not currently available")
        if(volume is None):
            return None
        stock.volume = float(volume)

    def __initAverageVolume(stock):
        averageVolume = stock.getDataElement("131", "average volume data not currently available")
        if(averageVolume is None):
            return None
        stock.averageVolume = float(averageVolume)

    def __initMarketCap(stock):
        temp = stock.getDataElement("139", "market cap data not currently available")
        if(temp is None):
            return None
        marketCap = ""
        for i in temp:
            if(i.isdigit() or i == "."):
                marketCap += i
        marketCap = float(marketCap)
        if(temp[len(temp) - 1] == "T"):
            marketCap *= 1000000000000
        elif(temp[len(temp) - 1] == "B"):
            marketCap *= 1000000000
        elif(temp[len(temp) - 1] == "M"):
            marketCap *= 1000000
        stock.marketCap = marketCap

    def __initHistoricalDataAll(stock):
        # try:
        xml = stock.xmlHistorical
        temp = str(xml)
        i = temp.find("HistoricalPriceStore")
        stringData = ""
        while(temp[i] != "["):
            i += 1
        while(temp[i] != "]"):
            stringData += temp[i]
            i += 1
        stringData += "]"
        ohcl = {}
        data = ast.literal_eval(stringData)
        openD = []
        high = []
        low = []
        close = []
        adjClose = []
        volume = []
        date = []
        firstDay = datetime(1970, 1, 1)
        for x in data:
            try:
                # day = [float(x["open"]), float(x["high"]), float(x['close']), float(x["low"])]
                dateInt = int(int(x["date"]) / 86400)
                dateString = (firstDay + timedelta(days=dateInt)).date().isoformat()
                openD.append(float(x["open"]))
                high.append(float(x["high"]))
                low.append(float(x["low"]))
                close.append(float(x["close"]))
                volume.append(float(x["volume"]))
                adjClose.append(float(x["adjclose"]))
                date.append(dateString)
            except:
                day = ""
        ohcl["open"] = openD
        ohcl["high"] = high
        ohcl["low"] = low
        ohcl["close"] = close
        ohcl["volume"] = volume
        ohcl["adjclose"] = adjClose
        ohcl["date"] = date
        # except:
        #     YahooFinanceAPI.message("error trying to access OHCL data")
        #     return None
        stock.OHCL = ohcl

    #returns the initialized stock
    def getInitializedStock(sym):
        try:
            stock = StockDataInterface.stocks[sym]
            return stock
        except:
            StockDataInterface.message("Error trying to access: " + sym + ". Try initializing the stock first")
            return None
    
    #gets the stock price from a list of stocks
    def getStockPriceAtClose(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        price = stock.priceAtClose
        if(price is None):
            return None            
        StockDataInterface.message(sym + " Price of at close: " + str(price))
        return price
        
    #gets the stock price after hours
    def getStockPriceAfterHours(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        price = stock.priceAfterHours
        if(price is None):
            return None
        StockDataInterface.message(sym + " Price after hours: " + str(price))
        return price

    #gets the change at close and returns the point and percentage change
    def getChangeAtClose(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        amountPoints = stock.pointChangeAtClose
        amountPercentage = stock.percentageChangeAtClose
        if(amountPoints is None or amountPercentage is None):
            return None
        return [float(amountPoints), float(amountPercentage)]

    #gets the point change at close
    def getPointChangeAtClose(sym):
        change = StockDataInterface.getChangeAtClose(sym)
        if(change is None):
            return None
        StockDataInterface.message(sym + " point change at close: " + str(change[0]))
        return change[0]

    #gets the percentage change at close
    def getPercentageChangeAtClose(sym):
        change = StockDataInterface.getChangeAtClose(sym)
        if(change is None):
            return None
        StockDataInterface.message( sym + " percentage change at close: " + str(change[1]) + "%")
        return change[1]

    #gets the change after hours and returns the point and percentage change
    def getChangeAfterHours(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        amountPoints = stock.pointChangeAfterHours
        amountPercentage = stock.percentageChangeAfterHours
        if(amountPoints is None or amountPercentage is None):
            return None
        return [float(amountPoints), float(amountPercentage)]

    #gets the point change at close
    def getPointChangeAfterHours(sym):
        change = StockDataInterface.getChangeAfterHours(sym)
        if(change is None):
            return None
        StockDataInterface.message(sym + " point change after hours: " + str(change[0]))
        return change[0]

    #gets the percentage change at close
    def getPercentageChangeAfterHours(sym):
        change = StockDataInterface.getChangeAfterHours(sym)
        if(change is None):
            return None
        StockDataInterface.message( sym + " percentage change after hours: " + str(change[1]) + "%")
        return change[1]

    #gets the previous close 
    def getPreviousClose(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        previousClose = stock.previousClose
        if(previousClose is None):
            return None
        StockDataInterface.message(sym + " previous close: " + str(previousClose))
        return previousClose

    #gets the opening price
    def getOpen(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        openPrice = stock.openPrice
        if(openPrice is None):
            return None
        StockDataInterface.message(sym + " open: " + str(openPrice))
        return openPrice

    #gets the day's range
    def  getDayRange(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        dayRange = stock.dayRange
        if(dayRange is None):
            return None
        return dayRange

    #gets the day's low
    def getDayLow(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        if(stock.dayRange is None):
            StockDataInterface.getDayRange(sym)
            stock = StockDataInterface.getInitializedStock(sym)
            if(stock is None or stock.dayRange is None):
                return None
        StockDataInterface.message(sym + " day low: " + str(stock.dayRange[0]))  
        return stock.dayRange[0]

    #gets the day's high
    def getDayHigh(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        if(stock.dayRange is None):
            StockDataInterface.getDayRange(sym)
            stock = StockDataInterface.getInitializedStock(sym)
            if(stock is None or stock.dayRange is None):
                return None
        StockDataInterface.message(sym + " day high: " + str(stock.dayRange[1]))  
        return stock.dayRange[1]

    #gets the 52 week range
    def get52WeekRange(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        yearRange = stock.yearRange
        if(yearRange is None):
            return None
        return yearRange

    #gets the 52 week low
    def get52WeekLow(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        if(stock.yearRange is None):
            StockDataInterface.get52WeekRange(sym)
            stock = StockDataInterface.getInitializedStock(sym)
            if(stock is None or stock.yearRange is None):
                return None
        StockDataInterface.message(sym + " 52 week low: " + str(stock.yearRange[0]))  
        return stock.yearRange[0]

    #gets the 52 week high
    def get52WeekHigh(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        if(stock.yearRange is None):
            StockDataInterface.get52WeekRange(sym)
            stock = StockDataInterface.getInitializedStock(sym)
            if(stock is None or stock.yearRange is None):
                return None
        StockDataInterface.message(sym + " 52 week high: " + str(stock.yearRange[1]))  
        return stock.yearRange[1]

    #gets the volume for a stock symbol
    def getVolume(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        volume = stock.volume
        if(volume is None):
            return None
        StockDataInterface.message(sym + " volume: " + str(volume))
        return volume

    def getAverageVolume(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        averageVolume = stock.averageVolume
        if(averageVolume is None):
            return None
        StockDataInterface.message(sym + " average volume: " + str(averageVolume))
        return averageVolume

    def getMarketCap(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        marketCap = stock.marketCap
        if(marketCap is None):
            return None
        StockDataInterface.message(sym + " market cap: " + str(marketCap))
        return marketCap

    #returns the historical data in a dict with keys: "open", "low", "high", "close"
    #each key holds data from most recent to least recent
    def getHistoricalDataAll(sym):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        ohcl = stock.OHCL
        return ohcl

    #returns the historical data in OHCL format from a range of trading days
    #num1 holds the start of how many days ago and num2 holds the end
    #e.g. num1 = 100 and num2 = 20 returns the data from 20 days ago to 100 days ago
    #returns data from most recent to least recent
    def getHistoricalDataRangeTradingDays(sym, num1, num2):
        if(num2 < num1):
            t = num2
            num2 = num1
            num1 = t
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        ohcl = stock.OHCL
        if(ohcl is None):
            return None 
        data = {}
        try:
            data["open"] = ohcl["open"][num1 : num2]
            data["close"] = ohcl["close"][num1 : num2]
            data["low"] = ohcl["low"][num1 : num2]
            data["high"] = ohcl["high"][num1 : num2]
            return data
        except:
            return None


    #returns the historical data in OHCL format from an x number of trading days from most recent to least recent
    def getHistoricalDataPastXTradingDays(sym, num):
        return StockDataInterface.getHistoricalDataRangeTradingDays(sym, 0, num)

    #returns the OHCL data of the past 5 trading days from most recent to least recent
    def getHistoricalDataPast5TradingDays(sym):
        return StockDataInterface.getHistoricalDataPastXTradingDays(sym, 5)

    #return the OHCL data of the past 30 trading days from most recent to least recent
    def getHistoricalDataPast30TradingDays(sym):
        return StockDataInterface.getHistoricalDataPastXTradingDays(sym, 30)

    #takes in two dates of strings in 'YYYY-MM-DD' format and returns the historical data in that range
    def getHistoricalDataRangeOfDates(sym, date1, date2):
        stock = StockDataInterface.getInitializedStock(sym)
        if(stock is None):
            return None
        dates = stock.OHCL["date"]
        print(dates)
        try:
            d1 = dates.index(date1)
            d2 = dates.index(date2)
        except:
            StockDataInterface.message("error trying to access data from dates given")
            return None
        return StockDataInterface.getHistoricalDataRangeTradingDays(sym, d1, d2)

    


    



class Stock:
    symbol = None
    xml = None
    xmlHistorical = None
    priceAtClose = None
    priceAfterHours = None
    pointChangeAtClose = None
    percentageChangeAtClose = None
    pointChangeAfterHours = None
    percentageChangeAfterHours = None
    previousClose = None
    openPrice = None
    dayRange = None
    yearRange = None
    volume = None
    averageVolume = None
    marketCap = None
    OHCL = None


    def __init__(self, xml, xmlHistorical, symbol):
        self.xml = xml
        self.xmlHistorical = xmlHistorical
        self.symbol = symbol

    def __str__(self):
        return self.sym

    def getDataElement(self, id, message):
        try:
            xml = self.xml.find_all("span", {"data-reactid" : str(id)})
            return xml[0].string.strip().replace(",","")
        except:
            StockDataInterface.message(message)
            return None    






