# Należy przygotować simulator_core, której
# – konstruktor powinien mieć w swych parametrach konfigurację podzbioru
#   kampanii/partnerów (podzbiór wartości partner_id) objętych daną symulacją i konfigurację podzbióru,
#   kampanii/partnerów (podzbiór wartości partner_id) objętych odczytem danych jako listę partners_to_read_data_from
#   instancji obiektów klasy PLO_partner_data_reader,
# – konstruktor powinien tworzyć listę instancji klasy per_partner_simulator – dla każdej kampanii (partnera)
#   objętej daną symulacją,
# – metoda next_day() powinna skutkować odczytaniem z partners_to_read_data_from danych
#   o kolejnym dniu równolegle symulowanych kampanii.
from datetime import timedelta
from functools import reduce

from sortedcontainers import SortedSet

from partner_data_reader import PartnerDataReader
from per_partner_simulator import PerPartnerSimulator


class SimulatorCore:
    def __init__(self, data_directory, partner_ids):
        self.data_directory = data_directory
        self.simulation_partner_ids = partner_ids
        self.partner_data_readers = [PartnerDataReader(partner_id, self.data_directory) for partner_id in
                                     self.simulation_partner_ids]
        self.per_partner_simulators = [PerPartnerSimulator(reader.partner_id, reader.partner_avg_click_click_cost)
                                       for reader in self.partner_data_readers]
        self.dates = SortedSet(reduce(list.__add__, [reader.dates for reader in self.partner_data_readers]))
        self.next_date = self.dates[0]

    def next_day(self):
        if self.next_date > self.dates[-1]:
            raise Exception('Next date exceeds last date!')
        next_day_partners_profit = {}
        for data_reader, simulator in zip(self.partner_data_readers, self.per_partner_simulators):
            partner_id = data_reader.partner_id
            if self.next_date == data_reader.next_date:
                try:
                    data_from_reader = data_reader.__next__()
                    next_day_partners_profit[partner_id] = simulator.next_day(data_from_reader)
                except StopIteration:
                    next_day_partners_profit[partner_id] = None
            else:
                next_day_partners_profit[partner_id] = None
        date = self.next_date
        self.next_date += timedelta(days=1)
        return date, next_day_partners_profit


if __name__ == '__main__':
    simulator_core = SimulatorCore('out', ['743B1EE3A39E06D855A72B3B66D501D0', '2AAA4123BE41F050F159BD574800464F'])
    print(simulator_core.dates)
    for i in range(30):
        data = simulator_core.next_day()
        print(data)
