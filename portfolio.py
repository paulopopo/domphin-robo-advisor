import asset_repartition
import asset
import numpy as np
import asset_covariances


class Portfolio:

    def __init__(self, list_asset_repartition):
        self.list_asset_repartition = list_asset_repartition
        print('--')
        self.returns = self.calculate_returns()
        self.volatility = self.calculate_volatility()
        print('--')

    def calculate_returns(self):
        result = 0

        for asset_repartition in self.list_asset_repartition:
            asset = asset_repartition.asset
            weight = asset_repartition.weight
            result += asset.annual_returns * weight
        print('Returns computed: {}'.format(result))
        return result

    def calculate_volatility(self):
        volatility = 0
        for i in range(0, len(self.list_asset_repartition)):
            for j in range(0, len(self.list_asset_repartition)):
                asset_repartition1 = self.list_asset_repartition[i]
                asset_repartition2 = self.list_asset_repartition[j]
                volatility += asset_repartition1.weight * asset_repartition2.weight \
                              * asset_covariances.calculate_covariance_of_two_objects(asset_repartition1.asset,
                                                                                      asset_repartition2.asset)
        print('Volatility computed: {}'.format(volatility))
        return volatility
