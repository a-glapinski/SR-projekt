import pickle

import pandas as pd


class PartnersDataSplitter:
    def __init__(self, click_cost_ratio, filepath, nrows=None, outdir='out'):
        self.raw_data_frame = None
        self.splitted_data_frames = None
        self.partners_avg_click_costs = None
        self.click_cost_ratio = click_cost_ratio
        self.filepath = filepath
        self.nrows = nrows
        self.outdir = outdir

    def load_raw_data(self):
        header_info = "sale,sales_amount_in_euro,time_delay_for_conversion,click_timestamp,nb_clicks_1week," \
                      "product_price,product_age_group,device_type,audience_id,product_gender,product_brand," \
                      "product_category_1,product_category_2,product_category_3,product_category_4," \
                      "product_category_5,product_category_6,product_category_7,product_country,product_id," \
                      "product_title,partner_id,user_id"
        dtypes = {'sale': 'int64', 'sales_amount_in_euro': 'float64', 'time_delay_for_conversion': 'int64',
                  'click_timestamp': 'int64', 'nb_clicks_1week': 'int64', 'product_price': 'float64',
                  'product_age_group': 'O', 'device_type': 'O', 'audience_id': 'O', 'product_gender': 'O',
                  'product_brand': 'O', 'product_category_1': 'O', 'product_category_2': 'O',
                  'product_category_3': 'O', 'product_category_4': 'O', 'product_category_5': 'O',
                  'product_category_6': 'O', 'product_category_7': 'O', 'product_country': 'O', 'product_id': 'O',
                  'product_title': 'O', 'partner_id': 'O', 'user_id': 'O'}
        self.raw_data_frame = pd.read_csv(self.filepath, delimiter='\t', header=None,
                                          names=header_info.split(','), dtype=dtypes, nrows=self.nrows)

    def group_data_by_partners_and_dates(self):
        self.load_raw_data()
        df = self.raw_data_frame

        df['sales_amount_in_euro'] = df['sales_amount_in_euro'].replace(-1.0, pd.NA)
        df['date'] = pd.to_datetime(df['click_timestamp'], unit='s').dt.date

        partner_id_groups = df.groupby('partner_id')

        self.__calculate_partners_avg_click_costs(partner_id_groups)
        self.splitted_data_frames = {partner_id: partner_data_frame.groupby('date') for partner_id, partner_data_frame
                                     in partner_id_groups}

    def save_groups_to_pickle(self):
        for partner_id, partner_id_date_df_groups in self.splitted_data_frames.items():
            with open(f'{self.outdir}/{partner_id}.pickle', "wb") as file:
                pair = (partner_id_date_df_groups, self.partners_avg_click_costs[partner_id])
                pickle.dump(pair, file)

    def __calculate_partners_avg_click_costs(self, partner_id_groups):
        total_partners_clicks_count = partner_id_groups.size()
        total_partners_sales = partner_id_groups['sales_amount_in_euro'].sum().apply(
            lambda total_sales: total_sales * self.click_cost_ratio)
        self.partners_avg_click_costs = total_partners_sales / total_partners_clicks_count


if __name__ == '__main__':
    data_splitter = PartnersDataSplitter(click_cost_ratio=0.12, filepath='criteo/CriteoSearchData')
    data_splitter.group_data_by_partners_and_dates()
    data_splitter.save_groups_to_pickle()
