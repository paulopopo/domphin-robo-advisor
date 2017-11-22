from assetList import fetchAllAssets
from asset import Asset


def main():
    message = "Hello jump API"
    # print(message)

    var = fetchAllAssets()
    print(var)

if __name__ == "__main__":
    # execute only if run as a script
    main()
