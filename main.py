import assetList
from asset import Asset
import pickle
import pandas
import numpy as np

def main():
    asset_hash_map = assetList.fetch_and_serialize_all_assets()
    print(asset_hash_map[3].annual_returns)


    # for id in asset_hash_map:
    #     tmp_asset = asset_hash_map[id]
    #     tmp_asset.daily_returns = tmp_asset.calculate_returns()
    #     asset_hash_map[id] = tmp_asset


if __name__ == "__main__":
    main()
