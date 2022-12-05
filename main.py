import requests
from bs4 import BeautifulSoup

def getData(stockCode):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
    url = 'https://finance.yahoo.com/quote/{stockCode}'
    r = requests.get(url, headers = headers)
    #print(r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    #print(soup.title.text)
    stock = {
    'StockName': soup.find('h1',{'class': 'D(ib) Fz(18px)'}).text,
    'CurrPrice': soup.find('td', {'data-test':'OPEN-value'}).text,
    'TargetEST': soup.find('td', {'data-test':'ONE_YEAR_TARGET_PRICE-value'}).text,
    'Profit': float(soup.find('td', {'data-test':'ONE_YEAR_TARGET_PRICE-value'}).text) -
              float(soup.find('td', {'data-test':'OPEN-value'}).text)
    }
    return stock

url = 'https://finance.yahoo.com/quote/AAPL'
r = requests.get(url)
print(r.status_code)
soup = BeautifulSoup(r.text, 'html.parser')
print(soup.title.text)
stock = {
'StockName': soup.find('h1',{'class': 'D(ib) Fz(18px)'}).text,
'CurrPrice': soup.find('td', {'data-test':'OPEN-value'}).text,
'TargetEST': soup.find('td', {'data-test':'ONE_YEAR_TARGET_PRICE-value'}).text,
'Profit': float(soup.find('td', {'data-test':'ONE_YEAR_TARGET_PRICE-value'}).text) -
          float(soup.find('td', {'data-test':'OPEN-value'}).text)
}
print(stock)