import requests
import json
import pickle
from asset import Asset
from requests.auth import HTTPBasicAuth
import os.path

endPoint = 'https://dolphin.jump-technology.com:3389/api/v1'
login = 'epita_user_9'
password = 'dolphin16116'
asset_hash_map_path = './assetHashMap.bin'
start_date = '2012-01-01'
end_date = '2017-06-30'
ratio_map = {'annual_volatility': '18', 'sharpe': '20', 'annual_returns': '17', 'returns': '21' }


def fetch_and_serialize_all_assets():

    # If the assets have already been fetched, return the result
    if os.path.exists(asset_hash_map_path):
        print('Already fetched. Deserialize the bin file.')
        return pickle.load(open(asset_hash_map_path, 'rb'))

    print('Not fetched. API CALL + Serialize.')
    url = endPoint + '/asset?columns=ASSET_DATABASE_ID&columns=TYPE&columns=CURRENCY&columns=LABEL'
    assets_map = {}

    res = requests.get(url, auth=HTTPBasicAuth(login, password), verify=False)
    data = json.loads(res.content.decode('utf-8'))

    for elt in data:

        # Fetch only STOCK
        if elt['TYPE']['value'] != 'STOCK':
            continue

        print('-')
        print('Fetching elt {}'.format(len(assets_map) + 1))

        asset_id = int(elt['ASSET_DATABASE_ID']['value'])
        currency = elt['CURRENCY']['value']
        label = elt['LABEL']['value']

        print('Loading quotes')
        tmp_asset = Asset(asset_id, currency, label, load_quotes(asset_id))
        print('Loading ratios')
        tmp_asset = load_ratios(asset=tmp_asset)
        print('-')
        assets_map[asset_id] = tmp_asset

    pickle.dump(assets_map, open(asset_hash_map_path, 'wb'))
    return assets_map


def load_quotes(asset_id):
    """
    Get the quotes of an asset

    :param asset_id:
    :return: Quotes of the asset, Json format
    """

    url = endPoint + '/asset/{0}/quote?start_date={1}&end_date={2}'.format(asset_id, start_date, end_date)
    res = requests.get(url, auth=HTTPBasicAuth(login, password), verify=False)
    data = json.loads(res.content.decode('utf-8'))
    return data


def load_ratios(asset):
    """
    Load volatility, rendement, rendements annualisé, sharp
    :param asset:
    :return: The object updated
    """

    # 18 = volatility
    url = endPoint + '/ratio/invoke'
    body = {
        'ratio': [
            ratio_map['annual_volatility'],
            ratio_map['returns'],
            ratio_map['annual_returns'],
            ratio_map['sharpe']
            ],
        'asset': [asset.id],
        'start_date': start_date,
        'end_date': end_date
    }

    res = requests.post(url, auth=HTTPBasicAuth(login, password), verify=False,
                        data=json.dumps(body))

    data = json.loads(res.content.decode('utf-8'))
    asset.sharp = float(data[str(asset.id)][ratio_map['sharpe']]['value'].replace(',', '.'))
    asset.annual_returns = float(data[str(asset.id)][ratio_map['annual_returns']]['value'].replace(',', '.'))
    asset.returns = float(data[str(asset.id)][ratio_map['returns']]["value"].replace(',', '.'))
    asset.annual_volatility = float(data[str(asset.id)][ratio_map['annual_volatility']]["value"].replace(',', '.'))

    return asset
