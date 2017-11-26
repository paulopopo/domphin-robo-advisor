import pickle
import numpy as np

asset_hash_map = pickle.load(open('./assetHashMap.bin', 'rb'))


def get_list_asset():

    # For now, get 20 random assets
    assets = []

    while len(assets) < 20:
        for asset_id in asset_hash_map:
            if len(assets) < 20 and asset_hash_map[asset_id] not in assets and asset_hash_map[asset_id].sharp > 1.2:
                assets.append(asset_hash_map[asset_id])
            elif len(assets) >= 20 :
                return assets


def get_20_no_random_asset():
    # For now, get 20 random assets
    assets = []

    while len(assets) < 20:
        for asset_id in asset_hash_map:
            if len(assets) < 20 and asset_hash_map[asset_id] not in assets and asset_hash_map[asset_id].currency == "EUR":
                assets.append(asset_hash_map[asset_id])
            elif len(assets) >= 20 :
                return assets


def get_2_no_random_asset():
    # For now, get 20 random assets
    assets = []

    while len(assets) < 2:
        for asset_id in asset_hash_map:
            if len(assets) < 2 and asset_hash_map[asset_id] not in assets and asset_hash_map[asset_id].currency == "EUR":
                assets.append(asset_hash_map[asset_id])
            elif len(assets) >= 2:
                return assets


def get_1_no_random_asset():
    # For now, get 20 random assets
    assets = []

    while len(assets) < 1:
        for asset_id in asset_hash_map:
            if len(assets) < 1 and asset_hash_map[asset_id] not in assets and asset_hash_map[asset_id].currency == "EUR":
                assets.append(asset_hash_map[asset_id])
            elif len(assets) >= 1:
                return assets
