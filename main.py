import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

my_api_key = os.getenv('API_KEY')


class RequestCreate:

    def __init__(self, api_key, currency, amount, base_currency='USD'):
        self.__api_key = api_key
        self.currency = currency
        self.amount = amount
        self.base_currency = base_currency
        self.response = None

    def send_request(self):
        response = requests.get(f'https://v6.exchangerate-api.com/v6/{self.__api_key}/latest/{self.base_currency}')
        if response.status_code == 200:
            self.response = json.loads(response.text)
        else:
            print(f"Error Code: {response.status_code}, something wrong")

    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, new_api):
        self.__api_key = new_api

    @staticmethod
    def calculate_exchanged_money(amount, currency_value):
        return round(amount * currency_value, 3)

    def print_all_currency(self):
        response = requests.get(f'https://v6.exchangerate-api.com/v6/{self.__api_key}/latest/USD')
        if response.status_code == 200:
            self.response = json.loads(response.text)
            print("All possible currencies: ")
            for index, key in enumerate(self.response['conversion_rates']):
                print(f'{index} - {key}')
        else:
            print(f"Error Code: {response.status_code}, something wrong")

    def __str__(self):
        if self.response is None:
            return f"Use method 'send_request', to get exchanged amount of money to chosen currency"
        else:
            converted_amount = self.calculate_exchanged_money(self.amount,
                                                              self.response['conversion_rates'][self.currency])
            return f"In currency {self.currency}, amount of your money will be {converted_amount}"


request_create = RequestCreate(my_api_key, "UAH", 500)
request_create.send_request()
request_create.print_all_currency()
print(request_create)

