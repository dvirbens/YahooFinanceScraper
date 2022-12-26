import time

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5 import uic
from enums import NumberOfStocks


class AppGui(QMainWindow):

    def __init__(self, yf):
        super(AppGui, self).__init__()
        uic.loadUi("app_gui.ui", self)
        self.stocks_info = []
        self.startButton.clicked.connect(self.start_button_clicked)
        self.ExportBtn.clicked.connect(self.export_data_to_excel)
        self.showInfoBtn.clicked.connect(self.evt_show_info_clicked)
        self.yf = yf
        self.number_of_stocks = 5
        self.show()

    def add_items_to_combobox(self):
        self.NumberOfStocksCB.addItems(NumberOfStocks.list())

    def start_button_clicked(self):
        self.startButton.setEnabled(False)
        self.number_of_stocks = int(self.NumberOfStocksCB.currentText())
        self.NumberOfStocksCB.setEnabled(False)
        self.worker = ThreadClass(yf=self.yf, app=self, number_of_stocks=self.number_of_stocks)
        # self.worker = ThreadClass(yf=self.yf, app=self, number_of_stocks=1)
        self.worker.start()
        self.worker.update_progres_bar.connect(self.evt_update_progressbar)
        self.worker.update_stocks_info.connect(self.evt_update_stocks_info)
        self.worker.finished.connect(self.evt_done_getting_stocks_info)

    def export_data_to_excel(self):
        self.yf.stocks_info_to_excel_file(stocks_info=self.stocks_info)

    def evt_update_stocks_info(self, val):
        self.stocks_info = val

    def evt_update_progressbar(self, val):
        self.progressBar.setValue(val)

    def evt_done_getting_stocks_info(self):
        self.progress_msg.setText('Done now you can select what information to show')
        self.startButton.setEnabled(True)
        self.NumberOfStocksCB.setEnabled(True)
        self.ExportBtn.setEnabled(True)
        self.informationSelectCB.setEnabled(True)
        self.showInfoBtn.setEnabled(True)

    def evt_show_info_clicked(self):
        what_to_show = self.informationSelectCB.currentText()
        print(what_to_show)
        if what_to_show == 'Show all stocks':
            self.show_all_at_table()
        elif what_to_show == 'Top estimated profitable stocks':
            self.show_top_est_profit()
        elif what_to_show == 'Top earning per share stocks':
            self.show_top_earning_per_share_table()
        elif what_to_show == 'Top dividend stocks':
            self.show_dividend_in_table()

    def show_all_at_table(self):
        self.tableWidget.setColumnCount(3)

        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Stock Name"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Price"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Industry"))
        row = 0
        self.tableWidget.setRowCount(len(self.stocks_info))
        for stock in self.stocks_info:
            self.tableWidget.setItem(row, 0, QTableWidgetItem(stock["stock_name"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(stock["current_price"]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(stock["industry"]))
            row = row + 1

    def show_top_est_profit(self):
        self.tableWidget.setColumnCount(5)
        stocks_info_sorted = sorted(self.stocks_info, key=lambda d: d['profit_in_percentage'], reverse=True)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Stock Name"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Current-Price"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Analysts stock price estimation"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Profit"))
        self.tableWidget.setHorizontalHeaderItem(4, QTableWidgetItem("Profit in Percentage"))
        self.tableWidget.setRowCount(len(stocks_info_sorted))
        row = 0
        for stock in stocks_info_sorted:
            profit = stock['profit']
            profit_percentage = f'{stock["profit_in_percentage"]}%'
            if profit == -1:
                profit = 'N/A'
                profit_percentage = 'N/A'
            self.tableWidget.setItem(row, 0, QTableWidgetItem(stock["stock_name"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(stock["current_price"]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(stock["estimated_price"]))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(profit)))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(profit_percentage))
            row += 1

    def show_top_earning_per_share_table(self):
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Stock Name"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Earning Per Share"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Earning per share analyst estimation"))
        self.tableWidget.setHorizontalHeaderItem(3, QTableWidgetItem("Earning growth in percentage"))
        stocks_info_sorted = sorted(self.stocks_info, key=lambda d: d['earning_average_estimate_percentage'],
                                    reverse=True)
        self.tableWidget.setRowCount(len(stocks_info_sorted))
        row = 0
        for stock in stocks_info_sorted:
            self.tableWidget.setItem(row, 0, QTableWidgetItem(stock["stock_name"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(stock['earning_per_share']))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(stock['earning_average_estimate']))
            earning = stock['earning_average_estimate_percentage']
            self.tableWidget.setItem(row, 3, QTableWidgetItem(f'{earning}%'))
            row += 1

    def show_dividend_in_table(self):
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("Stock Name"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Dividend"))
        row = 0
        self.tableWidget.setRowCount(len(self.stocks_info))
        for stock in self.stocks_info:
            dividend = stock['forward_dividend']
            self.tableWidget.setItem(row, 0, QTableWidgetItem(stock["stock_name"]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(stock['forward_dividend']))
            row += 1


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
