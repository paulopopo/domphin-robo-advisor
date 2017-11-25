import asset_repartition
import asset
import numpy as np
import asset_covariances
import pickle

correlation_map = pickle.load(open('./covariancesHashMap', 'rb'))
asset_hash_map = pickle.load(open('./assetHashMap.bin', 'rb'))


class Portfolio:

    def __init__(self, list_asset_repartition):
        self.list_asset_repartition = list_asset_repartition
        self.returns = self.calculate_returns()
        self.volatility = self.calculate_volatility()
        self.risk_free_rate = 0.005
        self.sharpe = self.calculate_sharpe()

    def calculate_returns(self):
        result = 0
        weights = 0
        returns = 0

        for asset_repartition in self.list_asset_repartition:
            asset = asset_hash_map[asset_repartition.asset_id]
            weight = asset_repartition.weight
            result += asset.annual_returns * weight
            weights += weight
            returns += asset.annual_returns

        # print('mean asset return: {}'.format(returns / len(self.list_asset_repartition)))
        # print('weights portfolio: {}'.format(weights))
        # print('returns portfolio: {}'.format(result))

        return result

    def calculate_volatility(self):
        volatility = 0

        for i in range(0, len(self.list_asset_repartition)):
            for j in range(0, len(self.list_asset_repartition)):
                asset_repartition1 = self.list_asset_repartition[i]
                asset_repartition2 = self.list_asset_repartition[j]

                correlation = correlation_map[asset_repartition1.asset_id][asset_repartition2.asset_id]
                volatility += asset_repartition1.weight * asset_repartition2.weight * correlation * asset_hash_map[asset_repartition1.asset_id].annual_volatility * asset_hash_map[asset_repartition2.asset_id].annual_volatility

        volatility = np.sqrt(volatility)
        return volatility

    def calculate_sharpe(self):
        return (self.returns - self.risk_free_rate) / self.volatility
