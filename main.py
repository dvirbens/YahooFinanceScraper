from YahooFinance import YahooFinance

stocks = YahooFinance.get_all_most_active_stocks()
stocks_info = []
cnt = 0

for stock in stocks:
    stocks_info.append(YahooFinance.get_stock_info(stock))
    print(cnt)
    cnt += 1

#sorted_list = sorted(stocks_info, key=lambda d: d['ProfitPercentage'], reverse=True)
print(stocks_info)
x=5