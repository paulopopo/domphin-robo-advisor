import requests, json
from requests.auth import HTTPBasicAuth


endPoint = 'https://dolphin.jump-technology.com:3389/api/v1'
login = 'epita_user_9'
password = 'dolphin16116'

class Asset :
    '''Represents any school member.'''

    average = 0
    volatility = 0
    priceDateMap = {}
    quotes = []

    def __init__(self, id):
        # Asset.__init__(self,id)
        self.id = id
        print('(Initialized Asset: {})'.format(self.id))
        self.loadQuotes()

    def loadQuotes(self):
        # Asset.loadQuotes(self)
        id = self.id
        url = endPoint + '/asset/{0}/quote?start_date={1}&end_date={2}'.format(id, '2012-01-01' , '2012-01-10')
        print(url)
        res = requests.get(url, auth=HTTPBasicAuth(login, password) , verify=False)
        data = json.loads(res.content.decode('utf-8'))
        self.buildQuotes(data)

    def buildQuotes(self, quotes):
        for q in quotes :
            date = q['date']
            close = q['close']
            self.priceDateMap[date] = close
        print(self.priceDateMap)