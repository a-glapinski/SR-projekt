import random

from sortedcontainers import SortedSet


class ProductListOptimizer:
    def __init__(self, partner_id, partner_avg_click_cost):
        self.partner_id = partner_id
        self.partner_avg_click_cost = partner_avg_click_cost
        self.products_seen_so_far = SortedSet()

    def next_day(self, one_day_partner_data):
        self.__update_products_seen_so_far(one_day_partner_data)
        return self.__get_excluded_products_pseudo_randomly()

    def __get_excluded_products_pseudo_randomly(self, how_many_ratio=20, random_seed=12):
        set_of_potentially_excluded_products = self.products_seen_so_far
        how_many_products = round(len(set_of_potentially_excluded_products) / how_many_ratio)
        random.seed(random_seed)
        excluded_products = random.sample(set_of_potentially_excluded_products, how_many_products)
        return sorted(excluded_products)

    def __update_products_seen_so_far(self, one_day_partner_data):
        products_ids = one_day_partner_data['product_id']
        self.products_seen_so_far |= products_ids
