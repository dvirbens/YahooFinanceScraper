from bs4 import BeautifulSoup
import requests as req
import pandas as pd


class YahooFinance:
    """
    class of yahoo finance data scraping
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

    @classmethod
    def get_stock_info(cls, stock_name: str) -> dict[str, any]:
        """

        :return:
        """

        url = f'https://finance.yahoo.com/quote/{stock_name}'
        url_ana = f'https://finance.yahoo.com/quote/{stock_name}/analysis?p={stock_name}'
        url_mem = f'https://finance.yahoo.com/quote/{stock_name}/key-statistics?p={stock_name}'
        
        r = req.get(url, headers=cls.headers)
        r_ana = req.get(url_ana, headers=cls.headers)
        r_mem = req.get(url_mem, headers=cls.headers)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        soup_ana = BeautifulSoup(r_ana.text, 'html.parser')
        soup_mem = BeautifulSoup(r_mem.text, 'html.parser')
        
        profit = ""
        profit_percentage = 0
        target_estimate = soup.find('td', {'data-test': 'ONE_YEAR_TARGET_PRICE-value'}).text

        if target_estimate == 'N/A':
            profit = -1
            profit_percentage = -1
        else:
            last_open_value = float(soup.find('td', {'data-test': 'OPEN-value'}).text)
            profit = float(target_estimate) - last_open_value
            profit_percentage = profit/last_open_value*100

        stock = {
            'StockName': soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text,
            'CurrPrice': soup.find('td', {'data-test': 'OPEN-value'}).text,
            'TargetEST': soup.find('td', {'data-test': 'ONE_YEAR_TARGET_PRICE-value'}).text,
            'Profit':  profit,
            'ProfitPercentage': profit_percentage,
            'avgEstimate': soup_ana.find_all('td', {'class': "Ta(end)"})[6].text,
            'marketCap': soup_mem.find('td', {'class': 'Fw(500) Ta(end) Pstart(10px) Miw(60px)'}).text
        }
        return stock


    @classmethod
    def get_all_most_active_stocks(cls) -> list:
        """

        :return:
        """
        stocks=[]
        url = "https://finance.yahoo.com/most-active?offset=0&count=5"
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
    def stocks_info_to_excel_file(stocks_info: list[dict[str, str, str, float, float, str, str]]) -> any:
        """

        :return:
        """
        data_file = pd.DataFrame.from_dict(stocks_info)
        data_file.to_excel('stocks_info.xlsx')
