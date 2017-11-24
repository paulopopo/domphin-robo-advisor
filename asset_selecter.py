import pickle


def get_list_asset():
    asset_hash_map = pickle.load(open('./assetHashMap.bin', 'rb'))

    # For now, get 20 random assets
    assets = []

    for asset_id in asset_hash_map:
        if len(assets) < 20:
            assets.append(asset_hash_map[asset_id])
        else:
            return assets
