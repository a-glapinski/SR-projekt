from datetime import timedelta
from functools import reduce

from sortedcontainers import SortedSet

from partner_data_reader import PartnerDataReader
from per_partner_simulator import PerPartnerSimulator


class SimulatorCore:
    def __init__(self, partner_ids, data_directory):
        self.simulation_partner_ids = partner_ids
        self.data_directory = data_directory
        self.partner_data_readers = [PartnerDataReader(partner_id, self.data_directory) for partner_id in
                                     self.simulation_partner_ids]
        self.per_partner_simulators = [PerPartnerSimulator(reader.partner_id, reader.partner_avg_click_click_cost)
                                       for reader in self.partner_data_readers]
        self.dates = SortedSet(reduce(list.__add__, [reader.dates for reader in self.partner_data_readers]))
        self.next_date = self.dates[0]

    def next_day(self):
        next_day_partners_data = {}
        for data_reader, simulator in zip(self.partner_data_readers, self.per_partner_simulators):
            partner_id = data_reader.partner_id
            if self.next_date == data_reader.next_date:
                try:
                    data_from_reader = data_reader.__next__()
                    next_day_partners_data[partner_id] = simulator.next_day(one_day_partner_data=data_from_reader)
                except StopIteration:
                    next_day_partners_data[partner_id] = simulator.next_day(one_day_partner_data=None)
            else:
                next_day_partners_data[partner_id] = simulator.next_day(one_day_partner_data=None)
        date = self.next_date
        self.next_date += timedelta(days=1)
        return date, next_day_partners_data
