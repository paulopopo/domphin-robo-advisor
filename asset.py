import requests, json
from requests.auth import HTTPBasicAuth

endPoint = 'https://dolphin.jump-technology.com:3389/api/v1'
login = 'epita_user_9'
password = 'dolphin16116'


class Asset:
    def __init__(self, id, currency, label, rawJson):
        # Asset.__init__(self,id)
        self.id = id
        self.label = label
        self.mean = 0
        self.annual_volatility = 0
        self.currency = currency
        self.priceDateMap = self.buildQuotes(rawJson)

        print('(Initialized Asset: {})'.format(self.id))

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def get_sharp(self):
        return -0.097626066925

    @staticmethod
    def buildQuotes(quotes):
        priceDateMap = {}
        for q in quotes:
            date = q['date']
            close = q['close']
            priceDateMap[date] = close
        return priceDateMap
