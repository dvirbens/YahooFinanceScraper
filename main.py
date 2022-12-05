from YahooFinance import YahooFinance





stocks=YahooFinance.get_all_most_active_stocks()
stocks_info=[]
cnt=0
for stock in stocks:
    stocks_info.append(YahooFinance.get_stock_info(stock))
    print(cnt)
    cnt+=1

print(stocks)
x = 2
