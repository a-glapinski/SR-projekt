from product_list_optimizer import ProductListOptimizer


class PerPartnerSimulator:
    def __init__(self, partner_id, partner_avg_click_cost):
        self.partner_id = partner_id
        self.partner_avg_click_cost = partner_avg_click_cost
        self.optimizer = ProductListOptimizer(self.partner_id)
        self.previous_day_excluded_products = []
        self.next_day_excluded_products = []

    def next_day(self, one_day_partner_data):
        self.next_day_excluded_products = self.optimizer.next_day(one_day_partner_data)
        if not self.previous_day_excluded_products:
            self.previous_day_excluded_products = self.next_day_excluded_products

        self.next_day_excluded_products = self.optimizer.next_day(one_day_partner_data)



        self.previous_day_excluded_products = self.next_day_excluded_products
        # TODO Roznica pomiedzy przychodami i kosztami (22%)

    def __calculate_per_day_profit(self, partner_data):
        pass
