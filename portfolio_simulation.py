from random import randrange, uniform
import json, requests, pickle, string
from requests.auth import HTTPBasicAuth


import asset_selecter
import numpy as np
import portfolio
import asset_repartition
import matplotlib.pyplot as plt


endPoint = 'https://dolphin.jump-technology.com:3389/api/v1'
login = 'epita_user_9'
password = 'dolphin16116'
start_date = '2012-01-01'
end_date = '2017-06-30'
ratio_map = {'annual_volatility': '18', 'sharpe': '20', 'annual_returns': '17', 'returns': '21'}
portfolio_id = '571'
currency = "EUR"


def main():
    # Get the 20 assets that will compose our portfolio
    list_assets = asset_selecter.get_list_asset()
    nb_simulations = 200000

    # Construct nb_simulations portfolios
    list_portfolio = create_random_portfolios(list_assets, nb_simulations)
    x = []
    y = []
    sharpes = []

    for portfolio in list_portfolio:
        x.append(portfolio.volatility)
        y.append(portfolio.returns)
        sharpes.append(portfolio.sharpe)

    plt.scatter(x, y, c=sharpes, cmap='RdYlBu')

    # efficient_border = get_efficient_border_from_list_portfolios(list_portfolio)
    # x2 = []
    # y2 = []
    # for key in efficient_border:
    #     x2.append(key)
    #     y2.append(efficient_border[key].returns)

    # plt.plot(x2, y2, 'go')

    plt.colorbar()
    plt.show()


def create_random_portfolios(list_assets, nb_simulations):
    """
    Create a list of nb_simulations portfolios
    :param list_assets: The list of assets that compose the portfolios
    :param nb_simulations: Number of random portfolios to generate
    :return: a list a portfolio objects
    """
    list_portfolios = []
    best_sharp = 0
    best_portfolio = 0

    # Create nb_simulations random portfolios
    for i in range(0, nb_simulations):
        list_assets_repartition = []
        weights = generate_random_weights(nb_assets=len(list_assets))

        # Assign each asset with its repartition
        for j in range(0, len(list_assets)):
            tmp_asset_repartition = asset_repartition.AssetRepartition(asset_id=list_assets[j].id, weight=weights[j])
            list_assets_repartition.append(tmp_asset_repartition)

        # Create a portfolio with the assets given + random weights (0.01 <= x <= 0.1)
        tmp_portfolio = portfolio.Portfolio(list_asset_repartition=list_assets_repartition)

        if best_sharp < tmp_portfolio.sharpe:
            best_sharp = tmp_portfolio.sharpe
            best_portfolio = tmp_portfolio

        list_portfolios.append(tmp_portfolio)

    put_portfolio(best_portfolio)
    print('portfolio sharpe: {}'.format(best_portfolio.sharpe))
    for asset_repartitio in best_portfolio.list_asset_repartition:
        print('AssetRepartition:')
        print('asset_repartition.id: {}'.format(asset_repartitio.asset_id))
        print('self.value: {}'.format(asset_repartitio.value))
        print('NAV: {}'.format(asset_repartitio.value / best_portfolio.total_initial_asset_value))
    return list_portfolios


def create_one_portfolio():
    """
    Create a deterministic portfolio
    :return: a portfolio
    """
    list_assets = asset_selecter.get_2_no_random_asset()
    list_assets_repartition = []
    # weights = [0.15, 0.15, 0.039, 0.039, 0.039, 0.039, 0.039, 0.039, 0.039, 0.039,
    #            0.039, 0.039, 0.039, 0.039, 0.039, 0.039, 0.039, 0.039, 0.039, 0.039]

    weights = [0.3, 0.7]

    # Assign each asset with its repartition
    for j in range(0, len(list_assets)):
        tmp_asset_repartition = asset_repartition.AssetRepartition(asset_id=list_assets[j].id, weight=weights[j])
        list_assets_repartition.append(tmp_asset_repartition)

    result = portfolio.Portfolio(list_asset_repartition=list_assets_repartition)
    return result


def generate_random_weights(nb_assets):
    """
    Generate nb_assets random values between [0.01 <= x <= 0.1]
    :param nb_assets: number of random weights to generate
    :return: list of random floats
    """
    weights = []
    for i in range(0, nb_assets):
        weights.append(uniform(0.015, 0.09))

    weights /= np.sum(weights)
    return weights


def put_portfolio(p):
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
    r = requests.put(url, auth=HTTPBasicAuth(login, password), verify=False,
                     data=json.dumps(body))


# def get_efficient_border_from_list_portfolios(list_portfolios):
#     """
#     :param list_portfolios: list of portfolios constructed from the monte carlo simulation
#     :return: map of efficient portfolios
#     """
#     tmp_efficient_border = {}
#     efficient_border = {}
#
#     for portfolio in list_portfolios:
#         x = round(portfolio.volatility, 4)
#
#         # Bins of 0.001
#         if x not in tmp_efficient_border:
#             tmp_efficient_border[x] = portfolio
#
#         if tmp_efficient_border[x].returns < portfolio.returns:
#             tmp_efficient_border[x] = portfolio
#
#
#     # for key in tmp_efficient_border:
#
#
#     return tmp_efficient_border

if __name__ == '__main__':
    main()
