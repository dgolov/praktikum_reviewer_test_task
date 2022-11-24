import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Можно использовать значение аргумента по умолчанию, код будет более простой и читаемый
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Нужно обратить внимание, что название переменной начинается с заглавной буквы, такие названия мы используем
        # в именах класса, обычные переменные так называть не рекомендуется
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Можно упростить, например 0 <= x < 7
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Строка уберается, можно не переносить ее на две строчки в коде
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Тут не нужны скобки обратите внимание на return в блоке if
            return('Хватит есть!')


class CashCalculator(Calculator):
    # Upper Case в Python обычно используют для названия переменных констант, в данном случае это не константы
    # Плюс эти параметры можно передавать в функцию get_today_cash_remained, либо в __init__ и не объявлять тут
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Для лучшей читаемости можно написать в одну строчку и не обязательно присваивать USD_RATE=USD_RATE
    # см комментарий выше, код можно оптимизировать
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # currency_type лишняя переменная, вместо нее можно везде использовать currency (как вы сделали с usd)
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Лишний знак равенства (Он используется в операциях сравнения, а не присвоения)
            # Подумайте что должно быть вместо ==
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            # Тут так же не нужны скобки, все можно вернуть одной строкой в одну строчку
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        # Тут можно использовать not вмето == 0, либо перенести этот
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Есть возможность сократить вложенность кода убрав последний elif
        elif cash_remained < 0:
            # Сложно читается, не нужен перенос строки
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        # Это не нужно, метод по умолчанию будет доступен в классе родителе
        super().get_week_stats()
