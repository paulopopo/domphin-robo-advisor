import pickle
import numpy as np
import asset

def main():
    asset_hash_map = pickle.load(open('./assetHashMap.bin', 'rb'))
    # asset1 = asset.Asset(10, "USD", "ASSET1", None)
    # asset2 = asset.Asset(11, "USD", "ASSET2", None)
    #
    # asset1.returns_list = [-0.0517, 0.1587, 0.2477, -0.0215, -0.1749, 0.0333, 0.0439, -0.1377, -0.0429, 0.1525, -0.1323, -0.1324]
    # asset2.returns_list = [-0.0557, 0.0112, 0.0272, 0.0158, 0.0007, 0.0143, 0.0922, -0.0658, -0.0254, 0.0488, -0.0468, -0.0791]
    #
    # asset_hash_map = {10: asset1, 11: asset2}

    hash_map_covariances = build_hash_map_correlations(asset_hash_map)
    pickle.dump(hash_map_covariances, open('./covariancesHashMap', 'wb'))


def build_hash_map_correlations(asset_hash_map):
    covariances_hash_map = {}
    for asset_id1 in asset_hash_map:
        for asset_id2 in asset_hash_map:
            if asset_id1 == asset_id2:
                continue
            correlation = calculate_correlation(asset_hash_map[asset_id1], asset_hash_map[asset_id2])
            if asset_id1 not in covariances_hash_map:
                covariances_hash_map[asset_id1] = {}
            covariances_hash_map[asset_id1][asset_id2] = correlation
            print(correlation)
    print(covariances_hash_map)
    return covariances_hash_map


def calculate_covariance(asset1, asset2):
    print('len asset1.returns_list: {}\n'
          'len asset2.returns_list: {}'.format(len(asset1.returns_list),
                                               len(asset2.returns_list)))
    print('asset: {}\nasset: {}'.format(asset1.id, asset2.id))
    if len(asset1.returns_list) != len(asset2.returns_list):
        return 0
    covariance = np.cov(asset1.returns_list, asset2.returns_list, bias=True)[0][1]
    return covariance


def calculate_variance(asset):
    return np.var(asset.returns_list)


def calculate_correlation(asset1, asset2):
    import math
    return calculate_covariance(asset1, asset2) / (math.sqrt(calculate_variance(asset1)) * math.sqrt(calculate_variance(asset2)))

if __name__ == '__main__':
    main()