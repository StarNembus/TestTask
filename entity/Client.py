from entity.Account import Account


class Client:
    def __init__(self, name):
        self.name = name
        self.account = Account()