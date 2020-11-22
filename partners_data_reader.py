# Należy przygotować klasę partner_data_reader (może mieć postać iteratora Python), której
# – konstruktor powinien mieć w swych parametrach identyfikator kampanii/partnera/podzbioru (partner_id) objętego
#   odczytem danych z pliku,
# – metoda next_day() powinna skutkować odczytaniem z odpowiedniego pliku (jednego z utworzonych wcześniej z użyciem
#   partner_data_splitter) danych o kolejnym dniu kampanii.
import pickle
from datetime import timedelta


class PartnersDataReader:
    def __init__(self, partner_id, directory):
        self.partner_id = partner_id
        self.directory = directory
        with open(f'{self.directory}/{self.partner_id}.pickle', "rb") as file:
            self.partner_data = pickle.load(file)
        self.dates = [date for date, _ in self.partner_data]
        self.__current_date = self.dates[0] - timedelta(days=1)

    def __iter__(self):
        return self

    def __next__(self):
        next_day = self.__current_date + timedelta(days=1)
        if next_day > self.dates[-1]:
            raise StopIteration
        self.__current_date = next_day
        return self.partner_data.get_group(self.__current_date)


if __name__ == '__main__':
    partners_data_reader = PartnersDataReader(partner_id='743B1EE3A39E06D855A72B3B66D501D0', directory='out')
    for data in partners_data_reader:
        print(data)
