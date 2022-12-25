from YahooFinance import YahooFinance
from enums import NumberOfStocks
from YahooFinanceGUI import AppGui
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys


def main():
    yf = YahooFinance()
    app = QApplication(sys.argv)
    window = AppGui(yf)
    window.add_items_to_combobox()
    app.exec_()


if __name__ == '__main__':
    main()
