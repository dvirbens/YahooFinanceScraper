import time

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5 import uic
from enums import NumberOfStocks
import time


class AppGui(QMainWindow):

    def __init__(self, yf):
        super(AppGui, self).__init__()
        uic.loadUi("app_gui.ui", self)
        self.stocks_info = []
        self.startButton.clicked.connect(self.button_clicked)
        self.yf = yf
        self.number_of_stocks = 5
        self.show()

    def add_items_to_combobox(self):
        self.NumberOfStocksCB.addItems(NumberOfStocks.list())

    def button_clicked(self):
        self.startButton.setEnabled(False)
        self.number_of_stocks = int(self.NumberOfStocksCB.currentText())
        self.NumberOfStocksCB.setEnabled(False)
        self.worker = ThreadClass(yf=self.yf, app=self, number_of_stocks=self.number_of_stocks)
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

    def __init__(self, yf, app, number_of_stocks):
        super(ThreadClass, self).__init__()
        self.yf = yf
        self.app = app
        self.number_of_stocks = number_of_stocks

    def run(self):
        stocks = self.yf.get_all_most_active_stocks(number_of_stoks_to_get=self.number_of_stocks)
        stocks_info = []
        cnt = 1
        for stock in stocks:
            stocks_info.append(self.yf.get_stock_info(stock))
            print(f'{cnt} {stock}')
            progres = (cnt / len(stocks)) * 100
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
