import unittest
import json, requests, pickle, string
from requests.auth import HTTPBasicAuth

from random import randrange, uniform

import asset_selecter
import numpy as np
import portfolio
import asset_repartition
import matplotlib.pyplot as plt

import assetList
from asset import Asset

from portfolio_simulation import create_random_portfolios

endPoint = 'https://dolphin.jump-technology.com:3389/api/v1'
login = 'epita_user_9'
password = 'dolphin16116'
start_date = '2012-01-01'
end_date = '2017-06-30'
ratio_map = {'annual_volatility': '18', 'sharpe': '20', 'annual_returns': '17', 'returns': '21', 'correlation': '19'}
portfolio_id = '571'

exchange_rate_USD_EUR = 0.775430
total_portfolio_budget = 10000000
assert_equal_range = 0.3


class PortfolioTest(unittest.TestCase):
    list_assets = asset_selecter.get_list_asset()
    asset_hash_map = assetList.fetch_and_serialize_all_assets()
    nb_simulations = 1

    # Construct nb_simulations portfolios
    list_portfolio = create_random_portfolios(list_assets, nb_simulations)
    p = list_portfolio[0]

    def test_portfolio_sharp(self):
        # for p in self.list_portfolio:
        p = self.list_portfolio[0]
        self.put_portfolio(p)
        self.test_sharpe_val_vs_api_share_val()

    def put_portfolio(self, p):
        # /!\ IT QUANTITY AND NOT WEIGHT
        list_asset_repartition = p.list_asset_repartition

        asset_id_list = []

        quantity_list = []
        for elt in list_asset_repartition:
            asset_id_list.append(elt.asset_id)
            # /!\ convert weight into quantity
            qte = self.convert_weight_to_quantity(elt.asset_id, elt.weight)
            quantity_list.append(qte)

        asset_list = [{"asset": {"asset": a, "quantity": q}} for a, q in zip(asset_id_list, quantity_list)]
        body = {
            "label": "PORTFOLIO_USER9",
            "currency": {
                "code": "EUR"
            },
            "type": "front",
            "values": {
                start_date : asset_list
            }
        }
        # print (json.dumps(body))
        url = endPoint + '/portfolio/{0}/dyn_amount_compo'.format(portfolio_id)
        requests.put(url, auth=HTTPBasicAuth(login, password), verify=False,
                     data=json.dumps(body))

    def convert_weight_to_quantity(self, id, weight):

        asset = self.asset_hash_map[id]
        budget = total_portfolio_budget * weight
        # Get last  closing price
        firstquote_date= sorted(asset.hash_map_quotes.keys())[0]
        price = asset.hash_map_quotes[firstquote_date]
        if asset.currency == 'USD':
            price = price * exchange_rate_USD_EUR
        return budget / price

    def test_sharpe_val_vs_api_share_val(self):
        p_sharpe = self.p.sharpe

        url = endPoint + '/ratio/invoke'
        body = {
            'ratio': [
                ratio_map['sharpe']
            ],
            'asset': [portfolio_id],
            'start_date': start_date,
            'end_date': end_date
        }

        res = requests.post(url, auth=HTTPBasicAuth(login, password), verify=False,
                            data=json.dumps(body))

        data = json.loads(res.content.decode('utf-8'))
        api_sharpe = float(data[portfolio_id][ratio_map['sharpe']]['value'].replace(',', '.'))

        self.assertAlmostEqual(api_sharpe, p_sharpe, delta=assert_equal_range)


unittest.main()
