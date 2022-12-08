from bs4 import BeautifulSoup
import requests as req
import pandas as pd
import xlwt
from enums import NumberOfStocks


class YahooFinance:
    """
    class of yahoo finance data scraping
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

    @classmethod
    def get_stock_info(cls, stock_name: str) -> dict:
        """

        :return: dictionary of stock information
                example:
                {
                   "stock_name":"Tesla, Inc. (TSLA)",
                   "current_price":"175.03",
                   "estimated_price":"263.65",
                   "earning_per_share":"3.19",
                   "profit":88.61,
                   "profit_in_percentage":"50.6%",
                   "earning_average_estimate":"4.11",
                   "earning_average_estimate_percentage":"28.8%",
                   "market_cap":"615.32B"
                }
        """

        url = f'https://finance.yahoo.com/quote/{stock_name}'
        url_ana = f'https://finance.yahoo.com/quote/{stock_name}/analysis?p={stock_name}'
        url_mem = f'https://finance.yahoo.com/quote/{stock_name}/key-statistics?p={stock_name}'
        url_profile = f'https://finance.yahoo.com/quote/{stock_name}/profile?p={stock_name}'

        r = req.get(url, headers=cls.headers)
        r_ana = req.get(url_ana, headers=cls.headers)
        r_mem = req.get(url_mem, headers=cls.headers)
        r_profile = req.get(url_profile, headers=cls.headers)

        soup = BeautifulSoup(r.text, 'html.parser')
        soup_ana = BeautifulSoup(r_ana.text, 'html.parser')
        soup_mem = BeautifulSoup(r_mem.text, 'html.parser')
        soup_profile = BeautifulSoup(r_profile.text, 'html.parser')

        profit = ""
        profit_percentage = 0
        target_estimate = soup.find('td', {'data-test': 'ONE_YEAR_TARGET_PRICE-value'}).text

        if target_estimate == 'N/A':
            profit = -1
            profit_percentage = -1
        else:
            last_open_value = float(soup.find('td', {'data-test': 'OPEN-value'}).text)
            profit = float(target_estimate) - last_open_value
            profit_percentage = profit / last_open_value * 100

        esp = soup.find('td', {'data-test': 'EPS_RATIO-value'}).text

        if esp == 'N/A':
            avg_earning_in_percentage = -1
        else:
            esp = float(esp)
            avg_earning = float(soup_ana.find_all('td', {'class': "Ta(end)"})[6].text)
            avg_earning_in_percentage = ((avg_earning - esp) / esp) * 100

        try:
            earning_average_estimate = soup_ana.find_all('td', {'class': "Ta(end)"})[6].text
        except Exception as e:
            earning_average_estimate = "N/A"

        stock = {
            'stock_name': soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text,
            #'industry':soup_profile.find('span',{'class':'Fw(600)'}),
            'current_price': soup.find('td', {'data-test': 'OPEN-value'}).text,
            'estimated_price': soup.find('td', {'data-test': 'ONE_YEAR_TARGET_PRICE-value'}).text,
            'forward_dividend': soup.find('td', {'data-test': 'DIVIDEND_AND_YIELD-value'}).text,
            'earning_per_share': soup.find('td', {'data-test': 'EPS_RATIO-value'}).text,
            'profit': round(profit, 2),
            'profit_in_percentage': f'{round(profit_percentage, 1)}%',
            'earning_average_estimate': earning_average_estimate,
            'earning_average_estimate_percentage': round(avg_earning_in_percentage, 1),
            'market_cap': soup_mem.find('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text
        }
        return stock

    @classmethod
    def get_all_most_active_stocks(cls, number_of_stoks_to_get: NumberOfStocks) -> list:
        """

        :return: list of number_of_stocks_to_get most active stocks symbol
                Example:['TSLA', 'AMZN', 'AAPL', ....]
        """
        stocks = []
        url = f"https://finance.yahoo.com/most-active?offset=0&count={number_of_stoks_to_get.value}"
        requests_stocks = req.get(url=url, headers=cls.headers)
        target_class = 'simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor) '
        soup = BeautifulSoup(requests_stocks.text, 'html.parser')
        results = soup.findAll('table')[0].findAll('tr')
        del results[0]
        for result in results:
            name = result.find('a')
            stocks.append(name.text)

        return stocks

    @classmethod
    def stocks_info_to_excel_file(cls, stocks_info: list) -> any:
        """

        :return:
        """
        wb = xlwt.Workbook()
        cls._create_stocks_info_sheet(stocks_info=stocks_info, work_book=wb)
        cls._create_estimated_profit_sheet(stocks_info=stocks_info, work_book=wb)
        cls._create_average_earning_estimation_sheet(stocks_info=stocks_info, work_book=wb)
        cls._create_divident_sheet(stocks_info=stocks_info, work_book=wb)
        wb.save("most_active_stocks_info.xls")

    @staticmethod
    def _create_stocks_info_sheet(stocks_info, work_book):
        """

        :param stocks_info: list of dicts with stocks information
        :param work_book:
        :return:
        """
        sheet = work_book.add_sheet("most_active_stocks_info")
        style = xlwt.easyxf('font: bold 1')
        sheet.write(0, 0, "Stock Name", style)
        sheet.write(0, 1, "Current Price", style)
        sheet.write(0, 2, "Target EST", style)
        sheet.write(0, 3, "Profit", style)
        sheet.write(0, 4, "Profit in Percentage", style)
        sheet.write(0, 5, "avgEstimate", style)
        sheet.write(0, 6, "marketCap", style)
        exel_row = 1
        for stock in stocks_info:
            sheet.write(exel_row, 0, stock['stock_name'])
            sheet.write(exel_row, 1, stock['current_price'])
            sheet.write(exel_row, 2, stock['estimated_price'])
            sheet.write(exel_row, 3, stock['profit'])
            sheet.write(exel_row, 4, stock['profit_in_percentage'])
            sheet.write(exel_row, 5, stock['earning_average_estimate'])
            sheet.write(exel_row, 6, stock['market_cap'])
            exel_row += 1

    @staticmethod
    def _create_average_earning_estimation_sheet(stocks_info: list, work_book):
        """

        :param stocks_info: list of dicts with stocks information
        :param work_book:
        :return:
        """
        stocks_info_sorted = sorted(stocks_info, key=lambda d: d['earning_average_estimate_percentage'], reverse=True)
        sheet = work_book.add_sheet("Top earning per share stocks")
        style = xlwt.easyxf('font: bold 1')
        sheet.write(0, 0, "Stock Name", style)
        sheet.write(0, 1, "Earning Per Share ", style)
        sheet.write(0, 2, "Earning per share analyst estimation", style)
        sheet.write(0, 3, "Earning growth in percentage", style)
        exel_row = 1
        for stock in stocks_info_sorted:
            sheet.write(exel_row, 0, stock['stock_name'])
            sheet.write(exel_row, 1, stock['earning_per_share'])
            sheet.write(exel_row, 2, stock['earning_average_estimate'])
            earning = stock['earning_average_estimate_percentage']
            sheet.write(exel_row, 3, f'{earning}%')
            exel_row += 1

    @staticmethod
    def _create_estimated_profit_sheet(stocks_info: list, work_book):
        """

        :param stocks_info: list of dicts with stocks information
        :param work_book:
        :return:
        """
        stocks_info_sorted = sorted(stocks_info, key=lambda d: d['profit_in_percentage'], reverse=True)
        sheet = work_book.add_sheet("Top estimated profitable stocks")
        style = xlwt.easyxf('font: bold 1')
        sheet.write(0, 0, "Stock Name", style)
        sheet.write(0, 1, "Current Price", style)
        sheet.write(0, 2, "Analysts stock price estimation", style)
        sheet.write(0, 3, "Profit", style)
        sheet.write(0, 4, "Profit in Percentage", style)
        exel_row = 1
        for stock in stocks_info_sorted:
            sheet.write(exel_row, 0, stock['stock_name'])
            sheet.write(exel_row, 1, stock['current_price'])
            sheet.write(exel_row, 2, stock['estimated_price'])
            sheet.write(exel_row, 3, stock['profit'])
            sheet.write(exel_row, 4, stock['profit_in_percentage'])
            exel_row += 1

    @staticmethod
    def _create_divident_sheet(stocks_info: list, work_book):
        """

        :param stocks_info: list of dicts with stocks information
        :param work_book:
        :return:
        """
        stocks_info_sorted = sorted(stocks_info, key=lambda d: d['profit_in_percentage'], reverse=True)
        sheet = work_book.add_sheet("Top divident shared")
        style = xlwt.easyxf('font: bold 1')
        sheet.write(0, 0, "Stock Name", style)
        sheet.write(0, 1, "Divident", style)
        exel_row = 1
        for stock in stocks_info_sorted:
            sheet.write(exel_row, 0, stock['stock_name'])
            sheet.write(exel_row, 1, stock['forward_dividend'])
            exel_row += 1
