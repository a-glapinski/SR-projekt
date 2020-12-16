# Należy przygotować klasę partner_data_reader (może mieć postać iteratora Python), której
# – konstruktor powinien mieć w swych parametrach identyfikator kampanii/partnera/podzbioru (partner_id) objętego
#   odczytem danych z pliku,
# – metoda next_day() powinna skutkować odczytaniem z odpowiedniego pliku (jednego z utworzonych wcześniej z użyciem
#   partner_data_splitter) danych o kolejnym dniu kampanii.
import pickle
from datetime import timedelta


class PartnerDataReader:
    def __init__(self, partner_id, directory):
        self.partner_id = partner_id
        self.directory = directory
        with open(f'{self.directory}/{self.partner_id}.pickle', "rb") as file:
            self.partner_data, self.partner_avg_click_click_cost = pickle.load(file)
        self.dates = [date for date, _ in self.partner_data]
        self.next_date = self.dates[0]

    def __iter__(self):
        return self

    def __next__(self):
        if self.next_date > self.dates[-1]:
            raise StopIteration
        date = self.next_date
        self.next_date += timedelta(days=1)
        try:
            return self.partner_data.get_group(date)
        except KeyError:
            return None


if __name__ == '__main__':
    partner_data_reader = PartnerDataReader(partner_id='C0F515F0A2D0A5D9F854008BA76EB537', directory='out')
    print(partner_data_reader.partner_avg_click_click_cost)
    for data in partner_data_reader:
        print(data)
