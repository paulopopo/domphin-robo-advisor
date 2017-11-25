import asset
import pickle
import converter

# Initial budget is 10M
initial_budget = 10000000
asset_hash_map = pickle.load(open('./assetHashMap.bin', 'rb'))


class AssetRepartition:

    def __init__(self, asset_id, weight):
        self.asset_id = asset_id
        self.quantity, self.weight = self.adjust_weight(weight)

    def adjust_weight(self, weight):
        """
        Because we need to upload quantity of each stock, the idea is to have the right quantity and then
        translate it back to weights.

        :param weight: random_weight
        :return: adjusted_weight (float)
        """

        initial_price_of_stock = converter.convert_currency_value(value=self.get_initial_stock_price(),
                                                                  initial_currency=asset_hash_map[self.asset_id].currency,
                                                                  final_currency='EUR')
        quantity_computed = self.compute_quantity_of_bought_stocks(initial_price_of_stock, weight)
        adjusted_weight = (initial_price_of_stock * quantity_computed) / initial_budget

        print('--')
        print('AssetRepartition')
        print('Assset id: {}'.format(self.asset_id))
        print('--')

        print('initial value: {}{}'.format(self.get_initial_stock_price(), asset_hash_map[self.asset_id].currency))
        print('final value:{}{}'.format(initial_price_of_stock, '€'))

        print('random weight assigned: {}'.format(weight))
        print('initial_price_of_stock: {}'.format(initial_price_of_stock))
        print('quantity computed: {}'.format(quantity_computed))
        print('adjusted weight: {}'.format(adjusted_weight))
        print('--')

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
        return int((weight * initial_budget) / (initial_price_of_stock))
