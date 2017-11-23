class Asset:
    def __init__(self, asset_id, currency, label, raw_json):
        self.id = asset_id
        self.label = label
        self.mean = 0
        self.currency = currency
        self.hash_map_quotes = self.build_hash_map_quotes(raw_json)

        self.annual_returns = 0
        self.returns = 0
        self.annual_volatility = 0
        self.sharp = 0

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def calculate_quotes(self):
        quotes_value = []
        sorted_key = sorted(self.hash_map_quotes)
        for key in sorted_key:
            quotes_value.append(self.hash_map_quotes[key])
        return quotes_value

    @staticmethod
    def build_hash_map_quotes(quotes):
        price_date_map = {}

        for q in quotes:
            date = q['date']
            close = q['close']
            price_date_map[date] = close

        return price_date_map

