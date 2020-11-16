# Należy przygotować klasę partner_data_reader (może mieć postać iteratora Python), której
# – konstruktor powinien mieć w swych parametrach identyfikator kampanii/partnera/podzbioru (partner_id) objętego
#   odczytem danych z pliku,
# – metoda next_day() powinna skutkować odczytaniem z odpowiedniego pliku (jednego z utworzonych wcześniej z użyciem
#   partner_data_splitter) danych o kolejnym dniu kampanii.
from datetime import datetime
from datetime import timedelta

import pandas as pd


class PartnersDataReader:
    def __init__(self, partner_id, directory):
        self.partner_id = partner_id
        self.directory = directory
        self.partner_data = pd.read_csv(f'{self.directory}/{self.partner_id}.csv', delimiter='\t').groupby('date')
        self.dates = [datetime.strptime(date, '%Y-%m-%d') for date, _ in self.partner_data]
        self.current_date = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_date is None:
            self.current_date = self.dates[0]
        else:
            next_day = self.current_date + timedelta(days=1)
            if next_day > self.dates[-1]:
                raise StopIteration
            self.current_date = next_day
        return self.partner_data.get_group(self.current_date.strftime('%Y-%m-%d'))


if __name__ == '__main__':
    partners_data_reader = PartnersDataReader(partner_id='743B1EE3A39E06D855A72B3B66D501D0', directory='out')
    for data in partners_data_reader:
        print(data)
