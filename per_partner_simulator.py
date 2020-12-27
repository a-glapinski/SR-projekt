from dataclasses import dataclass

from sortedcontainers import SortedSet

from product_list_optimizer import ProductListOptimizer


class PerPartnerSimulator:
    def __init__(self, partner_id, partner_avg_click_cost, npm_in_percents, optimizer_config):
        self.partner_id = partner_id
        self.partner_avg_click_cost = partner_avg_click_cost
        self.npm = npm_in_percents / 100
        self.optimizer = ProductListOptimizer(self.partner_id, partner_avg_click_cost, optimizer_config)
        self.previous_day_excluded_products = []

    def next_day(self, one_day_partner_data):
        if one_day_partner_data is None:
            return PerDayProfitGainFactors(), \
                   PerDayProductsData(products_seen_so_far=list(self.optimizer.products_seen_so_far),
                                      products_to_exclude=self.previous_day_excluded_products,
                                      products_actually_excluded=[])

        one_day_partner_data_only_excluded = one_day_partner_data.loc[
            one_day_partner_data['product_id'].isin(self.previous_day_excluded_products)]
        one_day_partner_data_without_excluded = one_day_partner_data.loc[
            -one_day_partner_data['product_id'].isin(self.previous_day_excluded_products)]

        per_day_profit_gain_factors = self.__calculate_per_day_profit_gain_factors(one_day_partner_data_only_excluded)

        actually_excluded_products = SortedSet(one_day_partner_data_only_excluded['product_id'])
        per_day_products_data = PerDayProductsData(
            products_seen_so_far=list(self.optimizer.products_seen_so_far),
            products_to_exclude=self.previous_day_excluded_products,
            products_actually_excluded=list(actually_excluded_products))

        self.previous_day_excluded_products = self.optimizer.next_day(one_day_partner_data_without_excluded)
        return per_day_profit_gain_factors, per_day_products_data

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

            excluded_product_profit_losses = excluded_product_total_sales * self.npm
            total_profit_losses += excluded_product_profit_losses

            excluded_product_net_profit_gain = \
                excluded_product_total_clicks_count * self.partner_avg_click_cost \
                - excluded_product_total_sales * (0.12 + self.npm)
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

    def to_dict_with_date(self, date):
        return {
            'day': date.strftime('%Y-%m-%d'),
            'clicksSavings': self.clicks_savings,
            'saleLosses': self.sale_losses,
            'profitLosses': self.profit_losses,
            'profitGain': self.profit_gain
        }


@dataclass
class PerDayProductsData:
    products_seen_so_far: list
    products_to_exclude: list
    products_actually_excluded: list

    def to_dict_with_date(self, date):
        return {
            'day': date.strftime('%Y-%m-%d'),
            'productsSeenSoFar': self.products_seen_so_far,
            'productsToExclude': self.products_to_exclude,
            'productsActuallyExcluded': self.products_actually_excluded
        }
