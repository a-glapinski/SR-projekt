from dataclasses import dataclass

from product_list_optimizer import ProductListOptimizer


class PerPartnerSimulator:
    def __init__(self, partner_id, partner_avg_click_cost):
        self.partner_id = partner_id
        self.partner_avg_click_cost = partner_avg_click_cost
        self.optimizer = ProductListOptimizer(self.partner_id)
        self.previous_day_excluded_products = []

    def next_day(self, one_day_partner_data):
        one_day_partner_data_only_excluded = one_day_partner_data.loc[
            one_day_partner_data['product_id'].isin(self.previous_day_excluded_products)]
        one_day_partner_data_without_excluded = one_day_partner_data.loc[
            -one_day_partner_data['product_id'].isin(self.previous_day_excluded_products)]
        return self.__calculate_per_day_profit(one_day_partner_data_only_excluded,
                                               one_day_partner_data_without_excluded)

    def __calculate_per_day_profit(self, one_day_partner_data_only_excluded,
                                   one_day_partner_data_without_excluded):
        if not self.previous_day_excluded_products:
            self.previous_day_excluded_products = self.optimizer.next_day(one_day_partner_data_without_excluded)
            return PerDayProfit()

        click_savings_for_each_product = []
        sale_losses_for_each_product = []
        profit_losses_for_each_product = []

        for excluded_product_id in self.previous_day_excluded_products:
            excluded_product_df = one_day_partner_data_only_excluded.loc[
                one_day_partner_data_only_excluded['product_id'] == excluded_product_id]
            # TODO Obliczanie click_savings, sale_losses, profit_losses, profit_gain

        # TODO Roznica pomiedzy przychodami i kosztami (22%)

        # NPG - per produkt i per dzień,
        # Click savings - oszczednosci na kliknieciach, slajd 76 - pierwsza czesc formuly
        # Sale losses - daily per excluded products; tylko liczymy jesli produkt wykluczony
        # Profit losses

        self.previous_day_excluded_products = self.optimizer.next_day(one_day_partner_data_without_excluded)
        return PerDayProfit(click_savings=11.0, sale_losses=12.0, profit_losses=13.0, profit_gain=5.0)


@dataclass
class PerDayProfit:
    click_savings: float = 0.0
    sale_losses: float = 0.0
    profit_losses: float = 0.0
    profit_gain: float = 0.0
