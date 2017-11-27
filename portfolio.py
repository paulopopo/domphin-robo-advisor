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
        self.risk_free_rate = 0.005
        self.total_initial_asset_value = self.calculate_total_initial_asset_value()
        self.update_asset_nav()
        print('value portfolio: {}'.format(self.total_initial_asset_value))

        self.volatility = self.calculate_volatility()
        self.returns = self.calculate_returns()
        self.sharpe = self.calculate_sharpe()

    def calculate_returns(self):
        result = 0
        print('====')
        print('=calculate_returns=')

        for asset_repartition in self.list_asset_repartition:
            # print('asset id: {}'.format(asset_repartition.asset_id))
            # print('quantity: {}'.format(asset_repartition.quantity))
            asset = asset_hash_map[asset_repartition.asset_id]

            weight = asset_repartition.weight

            recalculate_nav_asset = (asset.price_asset_when_creating_portfolio_in_euros * asset_repartition.quantity) / self.total_initial_asset_value
            weight = recalculate_nav_asset

            result += asset.annual_returns * weight

            #print('recalculate_nav_asset: {}'.format(recalculate_nav_asset))
            # print('asset_repartition.weight: {}'.format(asset_repartition.weight))
            # print('asset.annual_returns: {}'.format(asset.annual_returns))
            # print('Multiplication: {}'.format(asset.annual_returns * weight))
        print('====')

        return result

    def calculate_initial_portfolio_value(self):
        initial_quote = 0
        for asset_repartition in self.list_asset_repartition:
            asset = asset_hash_map[asset_repartition.asset_id]
            initial_quote += (asset.opening_quotes[0] * asset_repartition.quantity)
        return initial_quote

    def calculate_final_portfolio_value(self):
        final_quote = 0
        for asset_repartition in self.list_asset_repartition:
            asset = asset_hash_map[asset_repartition.asset_id]
            final_quote += (asset.closing_quotes[len(asset.closing_quotes) - 1] * asset_repartition.quantity)
        return final_quote

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

    def calculate_total_initial_asset_value(self):
        result = 0
        for asset_repartition in self.list_asset_repartition:
            result += asset_repartition.value
        return result

    def update_asset_nav(self):
        for asset_repartition in self.list_asset_repartition:
            asset_repartition.weight = round(asset_repartition.value / self.total_initial_asset_value, 5)
