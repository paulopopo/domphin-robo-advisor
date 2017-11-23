import assetList
from asset import Asset
import pickle


def main():
    asset_hash_map = assetList.fetch_and_serialize_all_assets()
    print(asset_hash_map)

if __name__ == "__main__":
    main()
