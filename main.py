from YahooFinance import YahooFinance
from enums import NumberOfStocks
from YahooFinanceGUI import AppGui
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys


def main():
    yf = YahooFinance()
    stocks_number = NumberOfStocks.FIVE
    stocks = yf.get_all_most_active_stocks(number_of_stoks_to_get=stocks_number)
    print(stocks)
    app = QApplication(sys.argv)
    window = AppGui(stocks, yf)
    window.add_items_to_combobox()

    app.exec_()

    # yf.stocks_info_to_excel_file(stocks_info)


if __name__ == '__main__':
    main()
