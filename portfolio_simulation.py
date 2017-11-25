from random import randrange, uniform

import asset_selecter
import numpy as np
import portfolio
import asset_repartition
import matplotlib.pyplot as plt


def main():
    # Get the 20 assets that will compose our portfolio
    list_assets = asset_selecter.get_list_asset()
    nb_simulations = 20000

    # Construct nb_simulations portfolios
    list_portfolio = create_random_portfolios(list_assets, nb_simulations)
    x = []
    y = []
    z = 0

    for portfolio in list_portfolio:
        x.append(portfolio.volatility)
        y.append(portfolio.returns)

    plt.plot(x, y, 'ro')
    plt.axis([0, 0.65, 0, 0.42])
    plt.show()


def create_random_portfolios(list_assets, nb_simulations):
    """
    Create a list of nb_simulations portfolios
    :param list_assets: The list of assets that compose the portfolios
    :param nb_simulations: Number of random portfolios to generate
    :return: a list a portfolio objects
    """
    z = 0
    list_portfolios = []

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
        list_portfolios.append(tmp_portfolio)

        z += 1
        if z % 100 == 0:
            print(tmp_portfolio.sharpe)
    return list_portfolios


def generate_random_weights(nb_assets):
    """
    Generate nb_assets random values between [0.01 <= x <= 0.1]
    :param nb_assets: number of random weights to generate
    :return: list of random floats
    """
    weights = []
    for i in range(0, nb_assets):
        weights.append(uniform(0.01, 0.1))

    #weights /= np.sum(weights)
    weights = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,]
    return weights


if __name__ == '__main__':
    main()

