# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import yfinance as yf

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    nvda=yf.Ticker("NVDA")
    hist=nvda.history(period="1mo")
    print(hist)





