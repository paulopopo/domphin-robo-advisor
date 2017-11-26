import pickle
import numpy as np
import asset
import math
import pandas


def main():
    asset_hash_map = pickle.load(open('./assetHashMap.bin', 'rb'))
    hash_map_covariances = build_hash_map_correlations(asset_hash_map)
    pickle.dump(hash_map_covariances, open('./covariancesHashMap', 'wb'))


def build_hash_map_correlations(asset_hash_map):
    """
    Build a HashMap that will contains the correlation between each combinaison of asset
    :param asset_hash_map: The asset index by their ID
    :return: a hash_map[315][26] = correlation between asset_id=315 and asset_id=26
    """

    covariances_hash_map = {}
    # Keep track of the progression
    count = 0

    # Loop between all combinations
    for asset_id1 in asset_hash_map:
        for asset_id2 in asset_hash_map:

            count += 1

            # Compute correlation between the 2 assets
            correlation = calculate_correlation(asset_hash_map[asset_id1], asset_hash_map[asset_id2])

            # Index the result
            if asset_id1 not in covariances_hash_map:
                covariances_hash_map[asset_id1] = {}
            covariances_hash_map[asset_id1][asset_id2] = correlation
            print('Correlation[{}][{}] : {} -- Couple n: {}'.format(asset_id1, asset_id2, correlation, count))

    return covariances_hash_map


def calculate_covariance(asset1_commun_daily_returns, asset2_commun_daily_returns):
    covariance = np.cov(asset1_commun_daily_returns, asset2_commun_daily_returns, bias=True)[0][1]
    return covariance


def calculate_variance(asset_commun_daily_returns):
    return np.var(asset_commun_daily_returns)


def get_common_daily_returns(asset1, asset2):
    """
    Because both assets may not have the same number of quotes, it is necessary to take the common one

    :param asset1: Python object that represent the first asset
    :param asset2: Python object that represent the second asset
    :return: (df_daily_returns_asset_1, df_daily_returns_asset_2)
    """

    # Restrictive asset is the asset with the less quotes
    restrictive_asset = asset1
    not_restrictive_asset = asset2
    quotes_asset_1 = []
    quotes_asset_2 = []
    keys = []

    if len(asset2.hash_map_quotes) < len(asset1.hash_map_quotes):
        restrictive_asset = asset2
        not_restrictive_asset = asset1

    # Get the common quotes between the 2 assets
    for key in restrictive_asset.hash_map_quotes:
        if key not in not_restrictive_asset.hash_map_quotes:
            continue
        keys.append(key)

    for key in sorted(keys):
        closing_quote_asset_2 = asset2.hash_map_quotes[key][1]
        closing_quote_asset_1 = asset1.hash_map_quotes[key][1]
        quotes_asset_2.append(closing_quote_asset_2)
        quotes_asset_1.append(closing_quote_asset_1)

    # Transform the quotes into dataframe
    df1 = pandas.Series(quotes_asset_1)
    df2 = pandas.Series(quotes_asset_2)

    # Calculate the daily returns
    # Since the 0 is NaN, remove the 0index with [1:}
    asset1_commun_daily_returns = df1.pct_change()[1:]
    asset2_commun_daily_returns = df2.pct_change()[1:]

    return asset1_commun_daily_returns, asset2_commun_daily_returns


def calculate_covariance_of_two_objects(asset1, asset2):
    asset1_common_daily_returns, asset2_common_daily_returns = get_common_daily_returns(asset1, asset2)
    return calculate_covariance(asset1_common_daily_returns, asset2_common_daily_returns)


def calculate_correlation(asset1, asset2):
    """
    Compute the correlation between asset1 and asset2
    :param asset1: Python object that represent the first asset
    :param asset2: Python object that represent the second asset
    :return: float correlation -1 < x < 1
    """
    # Get the common quotes, then get the daily returns of each asset
    asset1_common_daily_returns, asset2_common_daily_returns = get_common_daily_returns(asset1, asset2)

    # Person correlation formula
    cov = calculate_covariance(asset1_common_daily_returns, asset2_common_daily_returns)
    vara = calculate_variance(asset1_common_daily_returns)
    varb = calculate_variance(asset2_common_daily_returns)
    return cov / (np.sqrt(vara) * np.sqrt(varb))

if __name__ == '__main__':
    main()