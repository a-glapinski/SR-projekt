from product_list_optimizer import ProductListOptimizer


class PerPartnerSimulator:
    def __init__(self, partner_id):
        self.partner_id = partner_id
        self.optimizer = ProductListOptimizer(self.partner_id)

    def next_day(self, partner_data):
        self.optimizer.next_day(partner_data)
