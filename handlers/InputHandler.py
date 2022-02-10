import re

from entity.Account import Account
from entity.Client import Client

"""
Класс для обработки вводимых данных от пользователя
"""


class InputHandler:
    pattern_client = 'client="'
    pattern_amount = 'amount='
    pattern_desc = 'description="'
    pattern_since = 'since="'
    pattern_till = 'till="'

    patterns = [pattern_client, pattern_amount, pattern_desc, pattern_since, pattern_till]

    clients = []

    def __init__(self):
        self.command = ''

    # (1) основная работа программы (в бесконечном цикле будет запрашивать данные у клиента)
    def run(self):
        try:
            while True:
                self.client_input()
        except KeyboardInterrupt:
            print('WOW! Keyboard interrupt.')
        finally:
            print('Thanks for using.')

    # (2) запрос данных от клиента (результат - строка)
    def client_input(self):
        self.command = input('> ')
        self.line_parser(self.command)

    # (3) обработка данных от пользователя
    """
    Парсинг команд. Список команд:
    deposit - пополнение
    withdraw - снятие
    show_bank_statement - вывод справочной информации
    Атрибуты команд:
    --client - клиент в формате (Имя Фвмилия)
    --amount - сумма денежных средств (дробное число в долларах, 2 знак после запятой)
    --description - описание
    --since - начало периода (формат ГГГГ-ММ-ДД ЧЧ:мм:СС). Актуально только для команды show_bank_statement
    --till - конец периода (формат ГГГГ-ММ-ДД ЧЧ:мм:СС). Актуально только для команды show_bank_statement
    
    Примеры запросов:
    deposit --client="John Jones" --amount=100 --description="ATM Deposit"
    withdraw --client="John Jones" --amount=100 --description="ATM Withdrawal"
    show_bank_statement --client="John Jones" --since="2021-01-01 00:00:00" --till="2021-02-01 00:00:00"
    """

    def line_parser(self, client_line):
        # определяем основную команду
        command_and_attr = client_line.split('--')
        command = command_and_attr[0].strip()

        # обрезаем все пробелы
        for i in range(len(command_and_attr)):
            command_and_attr[i] = command_and_attr[i].strip()

        # проверяем количество аттрибутов
        if len(command_and_attr) != 4:
            print('Wrong quantity of attributes')
            return

        # проверяем валидность аттрибутов
        attrs_is_valid = InputHandler.check_attributes(command, command_and_attr[1:])
        if not attrs_is_valid:
            print('Wrong name of attributes')
            return
        # парсим имя
        name = InputHandler.parse_attr(command_and_attr[1])
        # находим клиента или создаем его
        client = InputHandler.check_account_name(name)

        if command == 'deposit':
            amount = int(InputHandler.parse_attr_amount(command_and_attr[2]))
            desc = InputHandler.parse_attr(command_and_attr[3])
            client.account.deposit(amount, desc)
        elif command == 'withdraw':
            amount = int(InputHandler.parse_attr_amount(command_and_attr[2])) * -1
            desc = InputHandler.parse_attr(command_and_attr[3])
            client.account.withdraw(amount, desc)
        elif command == 'show_bank_statement':
            since = InputHandler.parse_attr(command_and_attr[2])
            till = InputHandler.parse_attr(command_and_attr[3])
            client.account.show_bank_statement(since, till)
        else:
            print('Syntax error')


    def check_attributes(command, attibutes):
        if command == 'deposit' or command == 'withdraw':
            return attibutes[0].startswith(InputHandler.pattern_client) and \
                    attibutes[1].startswith(InputHandler.pattern_amount) and \
                   attibutes[2].startswith(InputHandler.pattern_desc)
        elif command == 'show_bank_statement':
            return attibutes[0].startswith(InputHandler.pattern_client) and \
                   attibutes[1].startswith(InputHandler.pattern_since) and \
                   attibutes[2].startswith(InputHandler.pattern_till)

    def parse_attr(attribute):
        idx_of_bound = [idx.start() for idx in re.finditer('\"', attribute)]
        return attribute[idx_of_bound[0] + 1:idx_of_bound[1]]

    def parse_attr_amount(attribute):
        idx = attribute.find('=')
        return int(attribute[idx + 1:])

    def check_account_name(name):
        for el in InputHandler.clients:
            if el.name == name:
                return el
        client = Client(name)
        InputHandler.clients.append(client)
        return client

