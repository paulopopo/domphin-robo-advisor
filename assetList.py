import requests, json
from asset import Asset
from requests.auth import HTTPBasicAuth


endPoint = 'https://dolphin.jump-technology.com:3389/api/v1'
login = 'epita_user_9'
password = 'dolphin16116'

allAssetId = []

def getAllAssetId() :
    url = endPoint + '/asset?columns=ASSET_DATABASE_ID'
    print(url)
    res = requests.get(url, auth=HTTPBasicAuth(login, password) , verify=False)
    data = json.loads(res.content.decode('utf-8'))
    for elt in data :
        allAssetId.append(elt['ASSET_DATABASE_ID']['value'])
    print(allAssetId)