from bs4 import BeautifulSoup
import requests as req


class YahooFinance:
    """
    class of yahoo finance data scraping
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

    @classmethod
    def get_stock_info(cls, stock_name: str) -> dict:
        """

        :return:
        """

        url = f'https://finance.yahoo.com/quote/{stock_name}'
        r = req.get(url, headers=cls.headers)
        # print(r.status_code)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.title.text)
        stock = {
            'StockName': soup.find('h1', {'class': 'D(ib) Fz(18px)'}).text,
            'CurrPrice': soup.find('td', {'data-test': 'OPEN-value'}).text,
            'TargetEST': soup.find('td', {'data-test': 'ONE_YEAR_TARGET_PRICE-value'}).text,
#            'Profit': float(soup.find('td', {'data-test': 'ONE_YEAR_TARGET_PRICE-value'}).text) -
#                      float(soup.find('td', {'data-test': 'OPEN-value'}).text)
        }
        return stock

    @classmethod
    def get_all_most_active_stocks(cls) -> list:
        """

        :return:
        """
        stocks=[]
        url = "https://finance.yahoo.com/most-active?offset=0&count=100"
        requests_stocks = req.get(url=url, headers=cls.headers)
        target_class = 'simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor) '
        soup = BeautifulSoup(requests_stocks.text, 'html.parser')
        results = soup.findAll('table')[0].findAll('tr')
        del results[0]
        for result in results:
            name = result.find('a')
            stocks.append(name.text)

        return stocks
