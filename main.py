from YahooFinance import YahooFinance
from enums import NumberOfStocks



yf=YahooFinance()
stocks = yf.get_all_most_active_stocks(number_of_stoks_to_get=NumberOfStocks.FIVE)
stocks_info = []
cnt = 0

for stock in stocks:
    stocks_info.append(yf.get_stock_info(stock))
    print(f'{cnt} {stock}')
    cnt += 1

yf.stocks_info_to_excel_file(stocks_info)
x = 5
