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


__stocks__ = dict()
__debugMode = False

#general scraper to get the url
def scraper(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "lxml")
    return soup

#sets the debug mode
def setDebugMode(mode):
    __debugMode = mode

def message(text):
    if(__debugMode):
        print(text)

#takes in a stock symbol and stores the data. Use this every time you want to refresh
def initializStockData(sym):
    xml = -1
    xmlHistorical = -1
    try:
        url = "https://finance.yahoo.com/quote/" + sym
        xml = scraper(url)
        
        url = "https://finance.yahoo.com/quote/"+sym+"/history?period1=1&period2=2000000000&interval=1d&filter=history&frequency=1d"
        xmlHistorical = scraper(url)
        message("Success initializing: " + sym)

    except:
        message("Error initializing: " + sym)
        return None
    stock = Stock(xml, xmlHistorical, sym)

    __initStockData__(stock)

    __stocks__[sym] = stock

    writeToJson(sym)

    return True

def __initStockData__(stock):
    __initStockPriceAtClose__(stock)
    __initStockPriceAfterHours__(stock)
    __initChangeAtClose__(stock)
    __initChangeAfterHours__(stock)
    __initPreviousClose__(stock)
    __initOpen__(stock)
    __initDayRange__(stock)
    __init52WeekRange__(stock)
    __initVolume__(stock)
    __initAverageVolume__(stock)
    __initMarketCap__(stock)
    __initHistoricalDataAll__(stock)


def writeToJson(sym):
    stock = getInitializedStock(sym)
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
        message("error trying to read data from " + sym + "_data.json")
        return None

    __stocks__[sym] = stock

    return True

def __initStockPriceAtClose__(stock):
    try:
        xml = stock.xml.find_all("span", {"data-reactid": "50"})
        stock.priceAtClose = float(xml[0].string.strip().replace(",",""))
    except:
        message(stock.symbol + " close price data not currently available")

def __initStockPriceAfterHours__(stock):
    try:
        xml = stock.xml.find_all("span", {"data-reactid": "55"})
        stock.priceAfterHours = float(xml[0].string.strip().replace(",",""))
    except:
        message(stock.symbol + " after hours data not currently available")

def __initChangeAtClose__(stock):
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
        message(stock.symbol + " change at close data not currently available")

def __initChangeAfterHours__(stock):
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
        message(stock.symbol + " change after hours data not currently available")

def __initPreviousClose__(stock):
    try:
        xml = stock.xml.find_all("span", {"data-reactid": "98"})
        previousClose = float(xml[0].string.strip().replace(",",""))
        stock.previousClose = previousClose
    except:
        message(stock.symbol + " previous close data not currently available")

def __initOpen__(stock):
    try:
        xml = stock.xml.find_all("span", {"data-reactid" : "103"})
        openPrice = float(xml[0].string.strip().replace(",",""))
        stock.openPrice = openPrice
    except:
        message(stock.symbol + " open price data not currently available")

def __initDayRange__(stock):
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
        message(stock.symbol + " day range data not currently available")

def __init52WeekRange__(stock):
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
        message("52 week range data not currently available")

def __initVolume__(stock):
    volume = stock.getDataElement("126", "volume data not currently available")
    if(volume is None):
        return None
    stock.volume = float(volume)

def __initAverageVolume__(stock):
    averageVolume = stock.getDataElement("131", "average volume data not currently available")
    if(averageVolume is None):
        return None
    stock.averageVolume = float(averageVolume)

def __initMarketCap__(stock):
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

def __initHistoricalDataAll__(stock):
    # try:
    xml = stock.xmlHistorical
    temp = str(xml)
    i = temp.find("HistoricalPriceStore")
    stringData = ""
    data = []
    while(temp[i] != "["):
        i += 1
    while(temp[i] != "]"):
        stringData = ""
        while(temp[i] != "{"):
            i += 1
        while(temp[i] != "}"):
            stringData += temp[i]
            i += 1
        while(temp[i] == "}"):
            stringData += temp[i]
            i += 1
        # print(stringData)
        try:
            day = ast.literal_eval(stringData)
            data.append(day)
        except:
            message("error adding: " + stringData + " to historical data")
    ohcl = {}
    # print(stringData)
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
        stock = __stocks__[sym]
        return stock
    except:
        message("Error trying to access: " + sym + ". Try initializing the stock first")
        return None

#gets the stock price from a list of stocks
def getStockPriceAtClose(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    price = stock.priceAtClose
    if(price is None):
        return None            
    message(sym + " Price of at close: " + str(price))
    return price
    
#gets the stock price after hours
def getStockPriceAfterHours(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    price = stock.priceAfterHours
    if(price is None):
        return None
    message(sym + " Price after hours: " + str(price))
    return price

#gets the change at close and returns the point and percentage change
def getChangeAtClose(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    amountPoints = stock.pointChangeAtClose
    amountPercentage = stock.percentageChangeAtClose
    if(amountPoints is None or amountPercentage is None):
        return None
    return [float(amountPoints), float(amountPercentage)]

#gets the point change at close
def getPointChangeAtClose(sym):
    change = getChangeAtClose(sym)
    if(change is None):
        return None
    message(sym + " point change at close: " + str(change[0]))
    return change[0]

#gets the percentage change at close
def getPercentageChangeAtClose(sym):
    change = getChangeAtClose(sym)
    if(change is None):
        return None
    message( sym + " percentage change at close: " + str(change[1]) + "%")
    return change[1]

#gets the change after hours and returns the point and percentage change
def getChangeAfterHours(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    amountPoints = stock.pointChangeAfterHours
    amountPercentage = stock.percentageChangeAfterHours
    if(amountPoints is None or amountPercentage is None):
        return None
    return [float(amountPoints), float(amountPercentage)]

#gets the point change at close
def getPointChangeAfterHours(sym):
    change = getChangeAfterHours(sym)
    if(change is None):
        return None
    message(sym + " point change after hours: " + str(change[0]))
    return change[0]

#gets the percentage change at close
def getPercentageChangeAfterHours(sym):
    change = getChangeAfterHours(sym)
    if(change is None):
        return None
    message( sym + " percentage change after hours: " + str(change[1]) + "%")
    return change[1]

#gets the previous close 
def getPreviousClose(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    previousClose = stock.previousClose
    if(previousClose is None):
        return None
    message(sym + " previous close: " + str(previousClose))
    return previousClose

#gets the opening price
def getOpen(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    openPrice = stock.openPrice
    if(openPrice is None):
        return None
    message(sym + " open: " + str(openPrice))
    return openPrice

#gets the day's range
def  getDayRange(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    dayRange = stock.dayRange
    if(dayRange is None):
        return None
    return dayRange

#gets the day's low
def getDayLow(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    if(stock.dayRange is None):
        getDayRange(sym)
        stock = getInitializedStock(sym)
        if(stock is None or stock.dayRange is None):
            return None
    message(sym + " day low: " + str(stock.dayRange[0]))  
    return stock.dayRange[0]

#gets the day's high
def getDayHigh(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    if(stock.dayRange is None):
        getDayRange(sym)
        stock = getInitializedStock(sym)
        if(stock is None or stock.dayRange is None):
            return None
    message(sym + " day high: " + str(stock.dayRange[1]))  
    return stock.dayRange[1]

#gets the 52 week range
def get52WeekRange(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    yearRange = stock.yearRange
    if(yearRange is None):
        return None
    return yearRange

#gets the 52 week low
def get52WeekLow(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    if(stock.yearRange is None):
        get52WeekRange(sym)
        stock = getInitializedStock(sym)
        if(stock is None or stock.yearRange is None):
            return None
    message(sym + " 52 week low: " + str(stock.yearRange[0]))  
    return stock.yearRange[0]

#gets the 52 week high
def get52WeekHigh(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    if(stock.yearRange is None):
        get52WeekRange(sym)
        stock = getInitializedStock(sym)
        if(stock is None or stock.yearRange is None):
            return None
    message(sym + " 52 week high: " + str(stock.yearRange[1]))  
    return stock.yearRange[1]

#gets the volume for a stock symbol
def getVolume(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    volume = stock.volume
    if(volume is None):
        return None
    message(sym + " volume: " + str(volume))
    return volume

def getAverageVolume(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    averageVolume = stock.averageVolume
    if(averageVolume is None):
        return None
    message(sym + " average volume: " + str(averageVolume))
    return averageVolume

def getMarketCap(sym):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    marketCap = stock.marketCap
    if(marketCap is None):
        return None
    message(sym + " market cap: " + str(marketCap))
    return marketCap

#returns the historical data in a dict with keys: "open", "low", "high", "close"
#each key holds data from most recent to least recent
def getHistoricalDataAll(sym):
    stock = getInitializedStock(sym)
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
    stock = getInitializedStock(sym)
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
    return getHistoricalDataRangeTradingDays(sym, 0, num)

#returns the OHCL data of the past 5 trading days from most recent to least recent
def getHistoricalDataPast5TradingDays(sym):
    return getHistoricalDataPastXTradingDays(sym, 5)

#return the OHCL data of the past 30 trading days from most recent to least recent
def getHistoricalDataPast30TradingDays(sym):
    return getHistoricalDataPastXTradingDays(sym, 30)

#takes in two dates of strings in 'YYYY-MM-DD' format and returns the historical data in that range
def getHistoricalDataRangeOfDates(sym, date1, date2):
    stock = getInitializedStock(sym)
    if(stock is None):
        return None
    dates = stock.OHCL["date"]
    print(dates)
    try:
        d1 = dates.index(date1)
        d2 = dates.index(date2)
    except:
        message("error trying to access data from dates given")
        return None
    return getHistoricalDataRangeTradingDays(sym, d1, d2)

    


    



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
            message(message)
            return None    






