# Przygotować – z użyciem Pandas (opcja rekomendowana, ale w przypadku niektórych komputerów być może zbyt „wymagająca”
# pod względem objętości RAM) i/lub Dask i/lub Koalas-wstępną implementację tzw. skryptu partners_data_spliter.py
# realizującego następujące funkcje:
# – podział kompletnego „surowego” zbioru CPS na podzbiory (grupy) dla poszczególnych kampanii/partnerów,
# – posortowanie wierszy każdego z podzbiorów wg dat wyznaczonych ze znaczników czasowych
#   (w „surowym” zbiorze są tylko znaczniki czasowe, które warto zastąpić datami),
# – zapisanie każdego z podzbiorów w oddzielnym pliku CSV (najlepiej o nazwie zawierającej partner_id)
import pickle

import pandas as pd


class PartnersDataSplitter:
    def __init__(self):
        self.raw_data_frame = None
        self.splitted_data_frames = None

    def load_raw_data(self, nrows=None):
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
        self.raw_data_frame = pd.read_csv('criteo/CriteoSearchData', delimiter='\t', header=None,
                                          names=header_info.split(','), dtype=dtypes, nrows=nrows)

    def group_data_by_partners_and_dates(self, nrows=None):
        self.load_raw_data(nrows)
        df = self.raw_data_frame
        df['date'] = pd.to_datetime(df['click_timestamp'], unit='s').dt.date
        partner_id_groups = df.groupby('partner_id')
        self.splitted_data_frames = {partner_id: partner_data_frame.groupby('date') for partner_id, partner_data_frame
                                     in partner_id_groups}

    def save_groups_to_pickle(self):
        for partner_id, partner_id_date_df_groups in self.splitted_data_frames.items():
            with open(f'out/{partner_id}.pickle', "wb") as file:
                pickle.dump(partner_id_date_df_groups, file)


if __name__ == '__main__':
    data_splitter = PartnersDataSplitter()
    data_splitter.group_data_by_partners_and_dates(10_000)
    data_splitter.save_groups_to_pickle()
