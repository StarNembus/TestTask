import datetime as dt

class Record:
    def __init__(self, desc, amount, balance):
        self.date = dt.datetime.now()
        self.desc = desc
        if amount >= 0:
            self.deposit = amount
        else:
            self.deposit = ''
        if amount < 0:
            self.withdraw = amount
        else:
            self.withdraw = ''
        self.balance = balance

