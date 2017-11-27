import asset
import pickle
import converter

# Initial budget is 10M
initial_budget = 10000000
asset_hash_map = pickle.load(open('./assetHashMap.bin', 'rb'))


class AssetRepartition:

    def __init__(self, asset_id, weight):
        self.asset_id = asset_id
        self.initial_value = self.get_initial_value()
        self.quantity, self.weight = self.adjust_weight(weight)
        self.value = self.calculate_nav()

    def get_initial_value(self):
        return asset_hash_map[self.asset_id].price_asset_when_creating_portfolio_in_euros

    def adjust_weight(self, weight):
        """
        Because we need to upload quantity of each stock, the idea is to have the right quantity and then
        translate it back to weights.

        :param weight: random_weight
        :return: adjusted_weight (float)
        """

        quantity_computed = self.compute_quantity_of_bought_stocks(self.initial_value, weight)
        adjusted_weight = (self.initial_value * quantity_computed) / initial_budget

        return quantity_computed, adjusted_weight

    def get_initial_stock_price(self):
        return asset_hash_map[self.asset_id].opening_quotes[0]

    @staticmethod
    def compute_quantity_of_bought_stocks(initial_price_of_stock, weight):
        """
        Translate the initial weight to a quantity of stocks
        :param initial_price_of_stock: The first closing price of a stock
        :param weight: random_weight assigned
        :return: the number of stocks purchased - int()
        """
        return int((weight * initial_budget) / (initial_price_of_stock)) - 10

    def calculate_nav(self):
        return self.quantity * self.initial_value
