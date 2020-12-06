import random

from sortedcontainers import SortedSet


class ProductListOptimizer:
    def __init__(self, partner_id):
        self.partner_id = partner_id
        self.today_products = None

    def next_day(self, one_day_partner_data):
        self.__set_products_seen_today(one_day_partner_data)
        return self.__get_excluded_products_pseudo_randomly()

    def __get_excluded_products_pseudo_randomly(self, how_many_ratio=3.1, random_seed=12):
        set_of_potentially_excluded_products = self.today_products
        how_many_products = round(len(set_of_potentially_excluded_products) / how_many_ratio)
        random.seed(random_seed)
        excluded_products = random.sample(set_of_potentially_excluded_products, how_many_products)
        return excluded_products

    def __set_products_seen_today(self, one_day_partner_data):
        products_list = one_day_partner_data['product_id'].to_list()
        self.today_products = SortedSet(products_list)
