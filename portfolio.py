import asset_repartition
import asset
import numpy as np
import asset_covariances
import pickle


class Portfolio:

    def __init__(self, list_asset_repartition):
        self.correlation_map = pickle.load(open('./covariancesHashMap', 'rb'))
        self.list_asset_repartition = list_asset_repartition
        self.returns = self.calculate_returns()
        self.volatility = self.calculate_volatility()
        self.risk_free_rate = 0.01
        self.sharpe = self.calculate_sharpe()

        # print('returns: {}'.format(self.returns))
        # print('volatility: {}'.format(self.volatility))
        #print('Sharpe: {}'.format(self.sharpe))

    def calculate_returns(self):
        result = 0
        for asset_repartition in self.list_asset_repartition:
            asset = asset_repartition.asset
            weight = asset_repartition.weight
            result += asset.annual_returns * weight


        return result

    def calculate_volatility(self):
        volatility = 0

        for i in range(0, len(self.list_asset_repartition)):
            for j in range(0, len(self.list_asset_repartition)):
                asset_repartition1 = self.list_asset_repartition[i]
                asset_repartition2 = self.list_asset_repartition[j]

                correlation = self.correlation_map[asset_repartition1.asset.id][asset_repartition2.asset.id]
                volatility += asset_repartition1.weight * asset_repartition2.weight * correlation * asset_repartition1.asset.annual_volatility * asset_repartition2.asset.annual_volatility

        volatility = np.sqrt(volatility)
        return volatility

    def calculate_sharpe(self):
        # print('self.returns :{}'.format(self.returns))
        # print('self.volatility :{}'.format(self.volatility))

        return (self.returns - self.risk_free_rate) / self.volatility
