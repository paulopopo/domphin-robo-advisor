import pandas
import math
import converter

class Asset:
    def __init__(self, asset_id, currency, label, price_asset_when_creating_portfolio_in_curr, raw_json):
        self.id = asset_id
        self.label = label
        self.currency = currency
        self.hash_map_quotes = 0
        self.closing_quotes = 0
        self.opening_quotes = 0
        self.daily_returns = 0
        self.monthly_returns = 0

        self.price_asset_when_creating_portfolio_in_curr = price_asset_when_creating_portfolio_in_curr
        self.price_asset_when_creating_portfolio_in_euros = \
            converter.convert_currency_value(price_asset_when_creating_portfolio_in_curr, self.currency, 'EUR')

        if raw_json is not None:
            self.hash_map_quotes = self.build_hash_map_quotes(raw_json)
            self.opening_quotes, self.closing_quotes, self.daily_returns = self.calculate_quotes()

        self.annual_returns = 0
        self.returns = 0
        self.annual_volatility = 0
        self.sharp = 0

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def calculate_quotes(self):
        opening_quotes = []
        closing_quotes = []
        daily_returns = []

        sorted_key = sorted(self.hash_map_quotes)
        for key in sorted_key:
            opening_quotes.append(self.hash_map_quotes[key][0])
            closing_quotes.append(self.hash_map_quotes[key][1])
            daily_returns.append(self.hash_map_quotes[key][2])
        return opening_quotes, closing_quotes, daily_returns

    def get_quotes_index_by_month(self):
        sorted_key = sorted(self.hash_map_quotes)
        quotes_index_by_month = {}
        for key in sorted_key:
            month = key[0:7]
            if month not in quotes_index_by_month:
                quotes_index_by_month[month] = []

        for key in sorted_key:
            month = key[0:7]
            quote = self.hash_map_quotes[key]
            quotes_index_by_month[month].append(quote)

        return quotes_index_by_month

    def compute_monthly_returns_from_daily_returns(self):
        pass

    @staticmethod
    def build_hash_map_quotes(quotes):
        price_date_map = {}

        for q in quotes:
            date = q['date']
            close = q['close']
            opening = q['open']
            daily_return = q['return']
            price_date_map[date] = opening, close, daily_return

        return price_date_map

