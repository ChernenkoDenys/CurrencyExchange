import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

my_api_key = os.getenv('API_KEY')
base_url = os.getenv('BASE_URL', 'https://v6.exchangerate-api.com/v6')


class RequestCreate:

    def __init__(self, api_key, currency, amount, base_currency='USD'):
        self.__api_key = api_key
        self.currency = currency
        self.amount = amount
        self.base_currency = base_currency
        self.response = None

    def send_request(self):
        try:
            url = f'{base_url}/{self.__api_key}/latest/{self.base_currency}'
            response = requests.get(url)
            response.raise_for_status()
            self.response = json.loads(response.text)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except json.JSONDecodeError as json_err:
            print(f"JSON decode error: {json_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    @property
    def api_key(self):
        return self.__api_key

    @staticmethod
    def calculate_exchanged_money(amount, currency_value):
        return round(amount * currency_value, 3)

    def print_all_currency(self):
        try:
            url = f'{base_url}/{self.__api_key}/latest/USD'
            response = requests.get(url)
            response.raise_for_status()
            self.response = response.json()
            print("All possible currencies: ")
            for index, key in enumerate(self.response['conversion_rates']):
                print(f'{index} - {key}')
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except json.JSONDecodeError as json_err:
            print(f"JSON decode error: {json_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

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

