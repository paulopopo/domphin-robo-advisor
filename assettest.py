import unittest
import json, requests, pickle, string
from requests.auth import HTTPBasicAuth


endPoint = 'https://dolphin.jump-technology.com:3389/api/v1'
login = 'epita_user_9'
password = 'dolphin16116'


class AssetTest(unittest.TestCase):

    assetMap = pickle.load(open('./assetHashMap.bin', 'rb'))


    def test_sharp_assetid_315(self):
        url = endPoint + '/ratio/invoke'
        body = {
            'ratio' : [17,18,20],
            'asset':[61],
            'startDate':'2012-01-01',
            'endDate':'2013-01-01'
        }

        print(json.dumps(body))
        res = requests.post(url, auth=HTTPBasicAuth(login, password), verify=False,
                           data=json.dumps(body))

        print("===")
        data = json.loads(res.content.decode('utf-8'))
        print(data)
        print("===")
        result_sharp_from_api =  float (data["61"]["20"]["value"].replace(',', '.'))
        self.assertEqual(result_sharp_from_api, self.assetMap[315].get_sharp())




unittest.main()