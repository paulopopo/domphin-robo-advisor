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

exchange_rate_USD_EUR = 0.775430
total_portfolio_budget = 10000000
assert_equal_range = 0.3


class PortfolioTest(unittest.TestCase):
    list_assets = asset_selecter.get_list_asset()
    asset_hash_map = assetList.fetch_and_serialize_all_assets()
    nb_simulations = 1

    # Construct nb_simulations portfolios
    list_portfolio = create_random_portfolios(list_assets, nb_simulations)
    # Fix portfolio
    fix_portfolio = create_one_portfolio()

    def test_portfolio_sharp(self):
        print("TEST with random generated portfolio")
        for p in self.list_portfolio:
            self.put_portfolio(p)
            self.test_val_vs_api_val(p.sharpe, p.volatility, p.returns, False)

    def test_fix_portfolio(self):
        print("TEST with fix portfolio")
        # for p in self.list_portfolio:
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

    def test_val_vs_api_val(self, p_sharpe, p_volatility, p_returns, is_fix):
        # p_sharpe = self.p.sharpe


        url = endPoint + '/ratio/invoke'
        body = {
            'ratio': [
                ratio_map['sharpe'],
                ratio_map['annual_volatility'],
                ratio_map['annual_returns'],
                ratio_map['returns'],
            ],
            'asset': [portfolio_id],
            'start_date': start_date,
            'end_date': end_date
        }

        res = requests.post(url, auth=HTTPBasicAuth(login, password), verify=False,
                            data=json.dumps(body))

        data = json.loads(res.content.decode('utf-8'))
        api_sharpe = float(data[portfolio_id][ratio_map['sharpe']]['value'].replace(',', '.'))
        api_annual_volatility = float(data[portfolio_id][ratio_map['annual_volatility']]['value'].replace(',', '.'))
        api_annual_returns = float(data[portfolio_id][ratio_map['annual_returns']]['value'].replace(',', '.'))
        api_returns = float(data[portfolio_id][ratio_map['returns']]['value'].replace(',', '.'))

        if (is_fix):
            print("TEST FIX portfolio: api_sharpe = {0} | our sharpe = {1}".format(api_sharpe, p_sharpe))
            print("TEST FIX portfolio: api_annual_volatility = {0} | our volatility = {1}".format(api_annual_volatility, p_volatility))
            print("TEST FIX portfolio: api_annual_returns = {0} | our returns = {1}".format(api_annual_returns, p_returns))
            print("TEST FIX portfolio: api_returns = {0} | our returns = {1}".format(api_returns, p_returns))
        else:
            print("TEST random portfolio: api_sharpe = {0} | our sharpe = {1}".format(api_sharpe, p_sharpe))
            print("TEST random portfolio: api_annual_volatility = {0} | our volatility = {1}".format(api_annual_volatility, p_volatility))
            print("TEST random portfolio: api_annual_returns = {0} | our returns = {1}".format(api_annual_returns, p_returns))
            print("TEST random portfolio: api_returns = {0} | our returns = {1}".format(api_returns, p_returns))

        self.assertAlmostEqual(api_sharpe, p_sharpe, delta=assert_equal_range)
        self.assertAlmostEqual(api_annual_volatility, p_volatility, delta=assert_equal_range)
        self.assertAlmostEqual(api_annual_returns, p_returns, delta=assert_equal_range)
        self.assertAlmostEqual(api_returns, p_returns, delta=assert_equal_range)


unittest.main()
