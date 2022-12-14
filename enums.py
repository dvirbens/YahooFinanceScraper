from enum import Enum


# class syntax
class NumberOfStocks(Enum):
    FIVE = 5
    TEN = 10
    FIFTEEN = 15
    TWENTY = 20
    TWENTY_FIVE = 25
    FIFTY = 50

    @staticmethod
    def list():
        return list(map(lambda c: str(c.value), NumberOfStocks))