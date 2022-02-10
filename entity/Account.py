from datetime import datetime

from entity.Record import Record


class Account:
    def __init__(self):
        self.records = []
        self.balance = 0

    def deposit(self, amount, description):
        self.balance += amount
        record = Record(description, amount, self.balance)
        self.records.append(record)
        print(f'Deposit operation was successful! {amount}$')

    def withdraw(self, amount, description):
        if self.balance >= amount * -1:
            self.balance += amount
            record = Record(description, amount, self.balance)
            self.records.append(record)
            print(f'Withdrawal operation was successful! {amount}$')
        else:
            print(f'Insufficient funds')

    def show_bank_statement(self, since, till):
        time_format = '%Y-%m-%d %H:%M:%S'
        for el in self.records:
            print(f'{el.date: {time_format}} '
                  f'| {"%+20s" % el.desc} '
                  f'| {("%10s" % "$" + str(el.withdraw)[1:]) if isinstance(el.withdraw, int) else "%10s" % ""} '
                  f'| {("%10s" % "$" + str(el.deposit)) if isinstance(el.deposit, int) else "%10s" % ""} '
                  f'| {"%10s" % "$" + str(el.balance)}')




