import pickle
import numpy as np


def get_list_asset():
    asset_hash_map = pickle.load(open('./assetHashMap.bin', 'rb'))

    # For now, get 20 random assets
    assets = []

    while len(assets) < 20:
        for asset_id in asset_hash_map:
            if len(assets) < 20 and asset_hash_map[asset_id] not in assets and asset_hash_map[asset_id].annual_returns > 0.30:
                assets.append(asset_hash_map[asset_id])
            elif len(assets) >= 20 :
                return assets
