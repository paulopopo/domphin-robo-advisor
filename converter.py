import pickle
import requests
import os
from requests.auth import HTTPBasicAuth

endPoint = 'https://dolphin.jump-technology.com:3389/api/v1'
login = 'epita_user_9'
password = 'dolphin16116'

if os.path.exists('./currencies_converter.bin'):
    currencies_rate = pickle.load( open('./currencies_converter.bin', 'rb'))


def main():
    currencies = ['EUR', 'USD', 'GBP', 'GBp', 'JPY', 'NOK', 'SEK']
    hash_map_currencies = {}

    for c in currencies:
        for c2 in currencies:
            url = endPoint + '/currency/rate/{}/to/{}'.format(c, c2)
            res = requests.get(url, auth=HTTPBasicAuth(login, password), verify=False)
            data = float(res.content.decode('utf-8'))

            if c not in hash_map_currencies:
                hash_map_currencies[c] = {}
            hash_map_currencies[c][c2] = data
            print('{} to {} ! {}'.format(c, c2, data))

    print(hash_map_currencies)
    pickle.dump(hash_map_currencies, open('./currencies_converter.bin', 'wb'))


def convert_currency_value(value, initial_currency, final_currency):
    print(currencies_rate[initial_currency][final_currency])
    print(value)
    return value * currencies_rate[initial_currency][final_currency]


if __name__ == '__main__':
    main()