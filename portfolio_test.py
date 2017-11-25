import unittest
import json, requests, pickle, string
from requests.auth import HTTPBasicAuth

from random import randrange, uniform

import asset_selecter
import numpy as np
import portfolio
import asset_repartition
import matplotlib.pyplot as plt

from portfolio_simulation import create_random_portfolios

endPoint = 'https://dolphin.jump-technology.com:3389/api/v1'
login = 'epita_user_9'
password = 'dolphin16116'
start_date = '2012-01-01'
end_date = '2017-06-30'
ratio_map = {'annual_volatility': '18', 'sharpe': '20', 'annual_returns': '17', 'returns': '21', 'correlation': '19'}
portfolio_id = '571'

assert_equal_range = 0.3


class PortfolioTest(unittest.TestCase):
    list_assets = asset_selecter.get_list_asset()
    nb_simulations = 1

    # Construct nb_simulations portfolios
    list_portfolio = create_random_portfolios(list_assets, nb_simulations)
    x = []
    y = []
    z = 0

    def test_portfolio_sharp(self):
        for p in self.list_portfolio:
            print("p")
            self.put_portfolio(p)
            self.test_portfolio_sharpe_val_vs_api_share_val(p.sharpe)

    @staticmethod
    def put_portfolio(p):
        # /!\ IT QUANTITY AND NOT WEIGHT
        list_asset_repartition = p.list_asset_repartition
        asset_id_list = []

        quantity_list = []
        for elt in list_asset_repartition:
            asset_id_list.append(elt.asset_id)

            # /!\ must be some quantity and not weight
            quantity_list.append(elt.weight)

        asset_list = [{"asset": {"asset": a, "quantity": q}} for a, q in zip(asset_id_list, quantity_list)]
        body = {
            "label": "PORTFOLIO_USER9",
            "currency": {
                "code": "EUR"
            },
            "type": "front",
            "values": {
                "2017-01-30": asset_list
            }
        }

        # print (json.dumps(body))
        url = endPoint + '/portfolio/{0}/dyn_amount_compo'.format(portfolio_id)
        requests.put(url, auth=HTTPBasicAuth(login, password), verify=False, data=json.dumps(body))

    def test_portfolio_sharpe_val_vs_api_share_val(self, portfolio_sharpe):

        print('portfolio_sharpe')
        print(portfolio_sharpe)

        url = endPoint + '/ratio/invoke'
        body = {
            'ratio': [
                ratio_map['sharpe']
            ],
            'asset': [portfolio_id],
            'startDate': start_date,
            'endDate': end_date
        }

        res = requests.post(url, auth=HTTPBasicAuth(login, password), verify=False,
                            data=json.dumps(body))

        data = json.loads(res.content.decode('utf-8'))
        api_sharpe = float(data[portfolio_id][ratio_map['sharpe']]['value'].replace(',', '.'))

        print('asses')
        print(api_sharpe)
        self.assertAlmostEqual(api_sharpe, portfolio_sharpe, delta=3.3)


unittest.main()
