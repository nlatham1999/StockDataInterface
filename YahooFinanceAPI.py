import urllib3
from bs4 import BeautifulSoup
import lxml
import html5lib

class YahooFinanceAPI:

    stocks = dict()

    #general scraper to get the url
    def scraper(self, url):
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, "lxml")
        return soup

    #takes in a stock symbol and stores the data. Use this every time you want to refresh
    def initializStockData(self, sym):
        try:
            url = "https://finance.yahoo.com/quote/" + sym
            xml = self.scraper(url)
            print("success")
        except:
            print("error")
        stock = Stock(xml, sym)
        self.stocks[sym] = stock
    
    #gets the stock price from a list of stocks
    def getStockPrice(self, sym):
        try:
            stock = self.stocks[sym]
            price = stock.price
            if(price == -1):
                xml = stock.xml.find_all("span", {"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"})
                stock.price = xml[0].string.strip()
                price = stock.price
            print(price)
            return price
        except:
            print("Error trying to access: " + sym + ". Try initializing the stock first")
        

class Stock:
    symbol = ""
    xml = ""
    price = -1

    def __init__(self, xml, symbol):
        self.xml = xml
        self.symbol = symbol

    def __str__(self):
        return self.sym
    






api = YahooFinanceAPI()
api.initializStockData("SPY")
api.getStockPrice("SPY")


