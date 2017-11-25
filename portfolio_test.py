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
from portfolio_simulation import create_one_portfolio

endPoint = 'https://dolphin.jump-technology.com:3389/api/v1'
login = 'epita_user_9'
password = 'dolphin16116'
start_date = '2012-01-01'
end_date = '2017-06-30'
ratio_map = {'annual_volatility': '18', 'sharpe': '20', 'annual_returns': '17', 'returns': '21'}
portfolio_id = '571'
currency = "EUR"

class PortfolioTest(unittest.TestCase):
    list_assets = asset_selecter.get_list_asset()
    asset_hash_map = assetList.fetch_and_serialize_all_assets()
    nb_simulations = 1

    # Construct nb_simulations portfolios
    list_portfolio = create_random_portfolios(list_assets, nb_simulations)
    # Fix portfolio
    fix_portfolio = create_one_portfolio()

    def test_fix_portfolio(self):
        p = self.fix_portfolio
        self.put_portfolio(p)
        self.test_val_vs_api_val(p.sharpe, p.volatility, p.returns, True)

    def put_portfolio(self, p):
        list_asset_repartition = p.list_asset_repartition

        asset_id_list = []

        quantity_list = []
        for elt in list_asset_repartition:
            asset_id_list.append(elt.asset_id)
            quantity_list.append(elt.quantity)

        asset_list = [{"asset": {"asset": a, "quantity": q}} for a, q in zip(asset_id_list, quantity_list)]
        body = {
            "label": "PORTFOLIO_USER9",
            "currency": {
                "code": currency
            },
            "type": "front",
            "values": {
                start_date: asset_list
            }
        }
        # print (json.dumps(body))
        url = endPoint + '/portfolio/{0}/dyn_amount_compo'.format(portfolio_id)
        requests.put(url, auth=HTTPBasicAuth(login, password), verify=False,
                     data=json.dumps(body))

unittest.main()
