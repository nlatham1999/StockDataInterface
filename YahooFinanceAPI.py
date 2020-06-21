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
                stock.priceAtClose = float(xml[0].string.strip())
                price = stock.priceAtClose
            except:
                YahooFinanceAPI.message("close price data not currently available")
                return None
        YahooFinanceAPI.message(sym + "Price of at close: " + str(price))
        return price
        
    #Todo: get the proper id
    def getStockPriceAfterHours(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        price = stock.priceAfterHours
        if(price is None):
            try:
                xml = stock.xml.find_all("span", {"data-reactid": "40"})
                stock.priceAfterHours = float(xml[0].string.strip())
                price = stock.priceAfterHours
            except:
                YahooFinanceAPI.message("After hours data not currently available")
                return None
        YahooFinanceAPI.message("Price after hours: " + str(price))
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
                temp = xml[0].string.strip()
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

    #gets the previous close 
    def getPreviousClose(sym):
        stock = YahooFinanceAPI.getInitializedStock(sym)
        if(stock is None):
            return None
        previousClose = stock.previousClose
        if(previousClose is None):
            try:
                xml = stock.xml.find_all("span", {"data-reactid": "98"})
                previousClose = float(xml[0].string.strip())
                stock.previousClose = previousClose
            except:
                YahooFinanceAPI.message("previous close data not currently available")
                return None
        YahooFinanceAPI.message(sym + " Previous close for " + sym + ": " + str(previousClose))
        return previousClose
        

        


class Stock:
    symbol = None
    xml = None
    priceAtClose = None
    priceAfterHours = None
    pointChangeAtClose = None
    percentageChangeAtClose = None
    previousClose = None

    def __init__(self, xml, symbol):
        self.xml = xml
        self.symbol = symbol

    def __str__(self):
        return self.sym
    






