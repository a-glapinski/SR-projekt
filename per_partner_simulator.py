import dataclasses
import json
from dataclasses import dataclass

from product_list_optimizer import ProductListOptimizer


class PerPartnerSimulator:
    def __init__(self, partner_id, partner_avg_click_cost):
        self.partner_id = partner_id
        self.partner_avg_click_cost = partner_avg_click_cost
        self.optimizer = ProductListOptimizer(self.partner_id, partner_avg_click_cost)
        self.previous_day_excluded_products = []

    def next_day(self, one_day_partner_data):
        if one_day_partner_data is None:
            return PerDayProfitGainFactors()

        one_day_partner_data_only_excluded = one_day_partner_data.loc[
            one_day_partner_data['product_id'].isin(self.previous_day_excluded_products)]
        one_day_partner_data_without_excluded = one_day_partner_data.loc[
            -one_day_partner_data['product_id'].isin(self.previous_day_excluded_products)]

        per_day_profit_gain_factors = self.__calculate_per_day_profit_gain_factors(one_day_partner_data_only_excluded)

        self.previous_day_excluded_products = self.optimizer.next_day(one_day_partner_data_without_excluded)
        return per_day_profit_gain_factors

    def __calculate_per_day_profit_gain_factors(self, one_day_partner_data_only_excluded):
        total_clicks_savings = 0.0
        total_sale_losses = 0.0
        total_profit_losses = 0.0
        total_net_profit_gain = 0.0

        for excluded_product_id in self.previous_day_excluded_products:
            excluded_product_df = one_day_partner_data_only_excluded.loc[
                one_day_partner_data_only_excluded['product_id'] == excluded_product_id]
            excluded_product_total_sales = excluded_product_df['sales_amount_in_euro'].sum()
            excluded_product_total_clicks_count = len(excluded_product_df.index)

            excluded_product_clicks_savings = excluded_product_total_clicks_count * self.partner_avg_click_cost
            total_clicks_savings += excluded_product_clicks_savings

            excluded_product_sale_losses = excluded_product_total_sales
            total_sale_losses += excluded_product_sale_losses

            excluded_product_profit_losses = \
                excluded_product_total_sales - excluded_product_total_clicks_count * self.partner_avg_click_cost
            total_profit_losses += excluded_product_profit_losses

            excluded_product_net_profit_gain = \
                excluded_product_total_clicks_count * self.partner_avg_click_cost - excluded_product_total_sales * 0.22
            total_net_profit_gain += excluded_product_net_profit_gain

        return PerDayProfitGainFactors(clicks_savings=total_clicks_savings,
                                       sale_losses=total_sale_losses,
                                       profit_losses=total_profit_losses,
                                       profit_gain=total_net_profit_gain)


@dataclass
class PerDayProfitGainFactors:
    clicks_savings: float = 0.0
    sale_losses: float = 0.0
    profit_losses: float = 0.0
    profit_gain: float = 0.0

    def to_json(self):
        return json.dumps(dataclasses.asdict(self))
