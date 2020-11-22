# Należy przygotować simulator_core, której
# – konstruktor powinien mieć w swych parametrach konfigurację podzbioru
#   kampanii/partnerów (podzbiór wartości partner_id) objętych daną symulacją i konfigurację podzbióru
#   kampanii/partnerów (podzbiór wartości partner_id) objętych odczytem danych jako listę partners_to_read_data_from
#   instancji obiektów klasy PLO_partner_data_reader,
# – konstruktor powinien tworzyć listę instancji klasy per_partner_simulator – dla każdej kampanii (partnera)
#   objętej daną symulacją,
# – metoda next_day() powinna skutkować odczytaniem z partners_to_read_data_from danych
#   o kolejnym dniu równolegle symulowanych kampanii.
from functools import reduce

from sortedcontainers import SortedSet

from partners_data_reader import PartnersDataReader
from per_partner_simulator import PerPartnerSimulator


class SimulatorCore:
    def __init__(self, partner_ids):
        self.simulation_partner_ids = partner_ids
        self.partner_data_readers = [PartnersDataReader(partner_id, 'out') for partner_id in
                                     self.simulation_partner_ids]
        self.per_partner_simulators = [PerPartnerSimulator(partner_id) for partner_id in self.simulation_partner_ids]
        self.dates = SortedSet(reduce(list.__add__, [data_reader.dates for data_reader in self.partner_data_readers]))

    def next_day(self):
        for date in self.dates:
            print(date)


if __name__ == '__main__':
    simulator_core = SimulatorCore(['743B1EE3A39E06D855A72B3B66D501D0', '2AAA4123BE41F050F159BD574800464F'])
    simulator_core.next_day()
