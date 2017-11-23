import unittest
import json, requests, pickle, string
from requests.auth import HTTPBasicAuth


endPoint = 'https://dolphin.jump-technology.com:3389/api/v1'
login = 'epita_user_9'
password = 'dolphin16116'


class AssetTest(unittest.TestCase):

    assetMap = pickle.load(open('./assetHashMap.bin', 'rb'))

    def test_annual_volatility_assetid_315(self):
        url = endPoint + '/ratio/invoke'
        body = {
            'ratio' : [17,18,20, 21],
            'asset':[315],
            'startDate':'2012-01-01',
            'endDate':'2017-06-30'
        }

        res = requests.post(url, auth=HTTPBasicAuth(login, password), verify=False,
                           data=json.dumps(body))

        data = json.loads(res.content.decode('utf-8'))
        result_sharp_from_api = float (data["315"]["18"]["value"].replace(',', '.'))
        self.assetMap[315].calculate_quotes()
        self.assertEqual(result_sharp_from_api, self.assetMap[315].annual_volatility)


unittest.main()