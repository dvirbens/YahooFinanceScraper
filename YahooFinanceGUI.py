import time

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5 import uic
from enums import NumberOfStocks
import time


class AppGui(QMainWindow):

    def __init__(self, stocks, yf):
        super(AppGui, self).__init__()
        uic.loadUi("app_gui.ui", self)
        self.stocks = stocks
        self.stocks_info = []
        self.startButton.clicked.connect(self.button_clicked)
        self.yf = yf
        self.show()

    def add_items_to_combobox(self):
        self.NumberOfStocksCB.addItems(NumberOfStocks.list())

    def button_clicked(self):
        self.startButton.setEnabled(False)
        self.NumberOfStocksCB.setEnabled(False)
        self.worker = ThreadClass(self.stocks, self.yf, app=self)
        self.worker.start()
        self.worker.update_progres_bar.connect(self.evt_update_progressbar)
        self.worker.update_stocks_info.connect(self.evt_update_stocks_info)
        self.worker.finished.connect(self.evt_done_getting_stocks_info)

    def evt_update_stocks_info(self, val):
        self.stocks_info = val

    def evt_update_progressbar(self, val):
        self.progressBar.setValue(val)

    def evt_done_getting_stocks_info(self):
        self.progress_msg.setText('Done')
        self.startButton.setEnabled(True)
        self.NumberOfStocksCB.setEnabled(True)


class ThreadClass(QtCore.QThread):
    update_progres_bar = QtCore.pyqtSignal(int)
    update_stocks_info = QtCore.pyqtSignal(list)

    def __init__(self, stocks, yf, app):
        super(ThreadClass, self).__init__()
        self.stocks = stocks
        self.yf = yf
        self.app = app

    def run(self):
        stocks_info = []
        cnt = 1
        for stock in self.stocks:
            stocks_info.append(self.yf.get_stock_info(stock))
            print(f'{cnt} {stock}')
            progres = (cnt / len(self.stocks)) * 100
            self.update_progres_bar.emit(progres)
            cnt += 1
        self.update_stocks_info.emit(stocks_info)
        self.update_table(stocks_info)

    def update_table(self, stocks_info):
        row = 0
        self.app.tableWidget.setRowCount(len(stocks_info))
        for stock in stocks_info:
            self.app.tableWidget.setItem(row, 0, QTableWidgetItem(stock["stock_name"]))
            self.app.tableWidget.setItem(row, 1, QTableWidgetItem(stock["current_price"]))
            row = row + 1
