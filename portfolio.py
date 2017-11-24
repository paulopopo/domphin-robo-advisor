import asset_repartition
import asset
import numpy as np


class Portfolio:

    def __init__(self, list_asset_repartition):
        self.list_asset_repartition = list_asset_repartition
        self.returns = self.calculate_returns()
        self.volatility = self.calculate_volatility()

    def calculate_returns(self):
        result = 0
        returns = []
        for asset_repartition in self.list_asset_repartition:
            asset = asset_repartition.asset
            weight = asset_repartition.weight
            returns.append(asset.annual_returns)
            result += asset.annual_returns * weight
        return result

    def calculate_volatility(self):
        self.volatility = 1
        return 0
