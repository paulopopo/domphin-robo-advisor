from random import randrange, uniform

import asset_selecter
import numpy as np
import portfolio
import asset_repartition


def main():
    # Get the 20 assets that will compose our portfolio
    list_assets = asset_selecter.get_list_asset()
    nb_simulations = 10

    # Construct nb_simulations portfolios
    list_portfolio = create_random_portfolios(list_assets, nb_simulations)


def create_random_portfolios(list_assets, nb_simulations):
    """
    Create a list of nb_simulations portfolios
    :param list_assets: The list of assets that compose the portfolios
    :param nb_simulations: Number of random portfolios to generate
    :return: a list a portfolio objects
    """
    list_portfolios = []

    # Create nb_simulations random portfolios
    for i in range(0, nb_simulations):
        list_assets_repartition = []
        weights = generate_random_weights(nb_assets=len(list_assets))

        # Assign each asset with its repartition
        for j in range(0, len(list_assets)):
            tmp_asset_repartition = asset_repartition.AssetRepartition(asset=list_assets[j], weight=weights[j])
            list_assets_repartition.append(tmp_asset_repartition)

        # Create a portfolio with the assets given + random weights (0.01 <= x <= 0.1)
        tmp_portfolio = portfolio.Portfolio(list_asset_repartition=list_assets_repartition)
        list_portfolios.append(tmp_portfolio)
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

    weights /= np.sum(weights)
    return weights


if __name__ == '__main__':
    main()

