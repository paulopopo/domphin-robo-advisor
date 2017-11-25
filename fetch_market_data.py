import assetList
from asset import Asset
import pickle
import pandas
import numpy as np


def main():
    print('Fetch_market_data')
    asset_hash_map = assetList.fetch_and_serialize_all_assets()

if __name__ == "__main__":
    main()
