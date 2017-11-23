import requests, json
import pickle
from asset import Asset
from requests.auth import HTTPBasicAuth
import os.path

endPoint = 'https://dolphin.jump-technology.com:3389/api/v1'
login = 'epita_user_9'
password = 'dolphin16116'


def fetchAllAssets():
    if os.path.exists('./assetHashMap.bin'):
        return  pickle.load(open('./assetHashMap.bin', 'rb'))

    url = endPoint + '/asset?columns=ASSET_DATABASE_ID&columns=TYPE&columns=CURRENCY&columns=LABEL'
    assetsMap = {}
    tuppleList = []
    print(url)
    res = requests.get(url, auth=HTTPBasicAuth(login, password), verify=False)
    data = json.loads(res.content.decode('utf-8'))
    for elt in data:
        if elt['TYPE']['value'] != 'STOCK':
            continue
        id = int(elt['ASSET_DATABASE_ID']['value'])
        currency = elt['CURRENCY']['value']
        label = elt['LABEL']['value']

        assetsMap[id] = Asset(id, currency, label,loadQuotes(id))
        print(assetsMap)
        pickle.dump(assetsMap, open('./assetHashMap.bin', 'wb'))
        return

def loadQuotes(id):
    # Asset.loadQuotes(self)
    url = endPoint + '/asset/{0}/quote?start_date={1}&end_date={2}'.format(id, '2012-01-01', '2017-06-30')
    print(url)
    res = requests.get(url, auth=HTTPBasicAuth(login, password), verify=False)
    data = json.loads(res.content.decode('utf-8'))
    return data

