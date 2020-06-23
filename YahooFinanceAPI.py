#Nick Latham
#6/21/2020
#An API for Yahoo Finance

import urllib3
from bs4 import BeautifulSoup
import lxml
import html5lib

class YahooFinanceAPI:

    stocks = dict()
    debugMode = True

    #general scraper to get the url
    def scraper(url):
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, "lxml")
        return soup

    #sets the debug mode
    def setDebugMode(mode):
        YahooFinanceAPI.debugMode = mode

    def message(text):
        if(YahooFinanceAPI.debugMode):
            print(text)

    #takes in a stock symbol and stores the data. Use this every time you want to refresh
    def initializStockData(sym):
        xml = -1
        try:
            url = "https://finance.yahoo.com/quote/" + sym
            xml = YahooFinanceAPI.scraper(url)
            YahooFinanceAPI.message("Success initializing: " + sym)
        except:
            YahooFinanceAPI.message("Error initializing: " + sym)
            return None
        stock = Stock(xml, sym)
        YahooFinanceAPI.stocks[sym] = stock

    #returns the initialized stock
    def getInitializedStock(sym):
        try:
            stock = YahooFinanceAPI.stocks[sym]
            return stock
        except:
            YahooFinanceAPI.message("Error trying to access: " + sym + ". Try initializing the stock first")
            return None
    
    #gets the stock price from a list of stocks
    def getStockPriceAtClose(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        price = stock.priceAtClose
        if(price is None):
            try:
                xml = stock.xml.find_all("span", {"data-reactid": "50"})
                stock.priceAtClose = float(xml[0].string.strip().replace(",",""))
                price = stock.priceAtClose
            except:
                YahooFinanceAPI.message("close price data not currently available")
                return None
        YahooFinanceAPI.message(sym + " Price of at close: " + str(price))
        return price
        
    #gets the stock price after hours
    def getStockPriceAfterHours(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        price = stock.priceAfterHours
        if(price is None):
            try:
                xml = stock.xml.find_all("span", {"data-reactid": "55"})
                stock.priceAfterHours = float(xml[0].string.strip().replace(",",""))
                price = stock.priceAfterHours
            except:
                YahooFinanceAPI.message("After hours data not currently available")
                return None
        YahooFinanceAPI.message(sym + " Price after hours: " + str(price))
        return price

    #gets the change at close and returns the point and percentage change
    def getChangeAtClose(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        amountPoints = stock.pointChangeAtClose
        amountPercentage = stock.percentageChangeAtClose
        if(amountPoints is None or amountPercentage is None):
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
                YahooFinanceAPI.message("change at close data not currently available")
                return None
        return [float(amountPoints), float(amountPercentage)]

    #gets the point change at close
    def getPointChangeAtClose(sym):
        change = YahooFinanceAPI.getChangeAtClose(sym)
        if(change is None):
            return None
        YahooFinanceAPI.message(sym + " point change at close: " + str(change[0]))
        return change[0]

    #gets the percentage change at close
    def getPercentageChangeAtClose(sym):
        change = YahooFinanceAPI.getChangeAtClose(sym)
        if(change is None):
            return None
        YahooFinanceAPI.message( sym + " percentage change at close: " + str(change[1]) + "%")
        return change[1]

    #gets the change after hours and returns the point and percentage change
    def getChangeAfterHours(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        amountPoints = stock.pointChangeAfterHours
        amountPercentage = stock.percentageChangeAfterHours
        if(amountPoints is None or amountPercentage is None):
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
                YahooFinanceAPI.message("change after hours data not currently available")
                return None
        return [float(amountPoints), float(amountPercentage)]

    #gets the point change at close
    def getPointChangeAfterHours(sym):
        change = YahooFinanceAPI.getChangeAfterHours(sym)
        if(change is None):
            return None
        YahooFinanceAPI.message(sym + " point change after hours: " + str(change[0]))
        return change[0]

    #gets the percentage change at close
    def getPercentageChangeAfterHours(sym):
        change = YahooFinanceAPI.getChangeAfterHours(sym)
        if(change is None):
            return None
        YahooFinanceAPI.message( sym + " percentage change after hours: " + str(change[1]) + "%")
        return change[1]

    #gets the previous close 
    def getPreviousClose(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        previousClose = stock.previousClose
        if(previousClose is None):
            try:
                xml = stock.xml.find_all("span", {"data-reactid": "98"})
                previousClose = float(xml[0].string.strip().replace(",",""))
                stock.previousClose = previousClose
            except:
                YahooFinanceAPI.message("previous close data not currently available")
                return None
        YahooFinanceAPI.message(sym + " previous close: " + str(previousClose))
        return previousClose

    #gets the opening price
    def getOpen(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        openPrice = stock.openPrice
        if(openPrice is None):
            try:
                xml = stock.xml.find_all("span", {"data-reactid" : "103"})
                openPrice = float(xml[0].string.strip().replace(",",""))
                stock.openPrice = openPrice
            except:
                YahooFinanceAPI.message("Open price data not currently available")
                return None
        YahooFinanceAPI.message(sym + " open: " + str(openPrice))
        return openPrice

    #gets the day's range
    def  getDayRange(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        dayRange = stock.dayRange
        if(dayRange is None):
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
                YahooFinanceAPI.message("day range data not currently available")
                return None
        return dayRange

    #gets the day's low
    def getDayLow(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        if(stock.dayRange is None):
            YahooFinanceAPI.getDayRange(sym)
            stock = YahooFinanceAPI.getInitializedStock(sym)
            if(stock is None or stock.dayRange is None):
                return None
        YahooFinanceAPI.message(sym + " day low: " + str(stock.dayRange[0]))  
        return stock.dayRange[0]

    #gets the day's high
    def getDayHigh(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        if(stock.dayRange is None):
            YahooFinanceAPI.getDayRange(sym)
            stock = YahooFinanceAPI.getInitializedStock(sym)
            if(stock is None or stock.dayRange is None):
                return None
        YahooFinanceAPI.message(sym + " day high: " + str(stock.dayRange[1]))  
        return stock.dayRange[1]

    #gets the 52 week range
    def get52WeekRange(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        yearRange = stock.yearRange
        if(yearRange is None):
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
                YahooFinanceAPI.message("52 week range data not currently available")
                return None
        return yearRange

    #gets the 52 week low
    def get52WeekLow(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        if(stock.yearRange is None):
            YahooFinanceAPI.get52WeekRange(sym)
            stock = YahooFinanceAPI.getInitializedStock(sym)
            if(stock is None or stock.yearRange is None):
                return None
        YahooFinanceAPI.message(sym + " 52 week low: " + str(stock.yearRange[0]))  
        return stock.yearRange[0]

    #gets the 52 week high
    def get52WeekHigh(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        if(stock.yearRange is None):
            YahooFinanceAPI.get52WeekRange(sym)
            stock = YahooFinanceAPI.getInitializedStock(sym)
            if(stock is None or stock.yearRange is None):
                return None
        YahooFinanceAPI.message(sym + " 52 week high: " + str(stock.yearRange[1]))  
        return stock.yearRange[1]

    #gets the volume for a stock symbol
    def getVolume(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        volume = stock.volume
        if(volume is None):
            volume = stock.getDataElement("126", "volume data not currently available")
            if(volume is None):
                return None
            stock.volume = float(volume)
        YahooFinanceAPI.message(sym + " volume: " + str(volume))
        return volume


class Stock:
    symbol = None
    xml = None
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


    def __init__(self, xml, symbol):
        self.xml = xml
        self.symbol = symbol

    def __str__(self):
        return self.sym

    def getDataElement(self, id, message):
        try:
            xml = self.xml.find_all("span", {"data-reactid" : str(id)})
            return xml[0].string.strip().replace(",","")
        except:
            YahooFinanceAPI.message(message)
            return None    






