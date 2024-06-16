import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class WrongConvert:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести {quote} в {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать значение {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/6359df55ab784e581b545d34/latest/{quote_ticker}')
        data = json.loads(r.content)
        if 'conversion_rates' not in data:
            raise ConvertionException('Ошибка при получении курсов валют.')

        rates = data['conversion_rates']
        if base_ticker not in rates:
            raise ConvertionException(f'Не удалось получить курс обмена для {base_ticker}.')

        rate = rates[base_ticker]
        total_base = rate * amount

        return total_base