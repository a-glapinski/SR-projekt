from datetime import timedelta
from functools import reduce

import matplotlib.pyplot as plt
from sortedcontainers import SortedSet

from partner_data_reader import PartnerDataReader
from per_partner_simulator import PerPartnerSimulator, PerDayProfitGainFactors


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
        next_day_partners_profit = {}
        for data_reader, simulator in zip(self.partner_data_readers, self.per_partner_simulators):
            partner_id = data_reader.partner_id
            if self.next_date == data_reader.next_date:
                try:
                    data_from_reader = data_reader.__next__()
                    next_day_partners_profit[partner_id] = simulator.next_day(data_from_reader)
                except StopIteration:
                    next_day_partners_profit[partner_id] = PerDayProfitGainFactors()
            else:
                next_day_partners_profit[partner_id] = PerDayProfitGainFactors()
        date = self.next_date
        self.next_date += timedelta(days=1)
        return date, next_day_partners_profit


# TODO better plotting mechanism
def plot(per_day_profit_gains):
    plt.plot(range(1, len(per_day_profit_gains) + 1), per_day_profit_gains)
    plt.xlabel('Days of simulation')
    plt.ylabel('Profit gain')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    # partners = ['743B1EE3A39E06D855A72B3B66D501D0', '2AAA4123BE41F050F159BD574800464F',
    #             'C0F515F0A2D0A5D9F854008BA76EB537']
    partners = ['C0F515F0A2D0A5D9F854008BA76EB537']
    simulator_core = SimulatorCore(partners, 'out')
    data = [simulator_core.next_day()[1] for i in range(40)]
    profit_gains = [p['C0F515F0A2D0A5D9F854008BA76EB537'].profit_gain for p in data]
    plot(profit_gains)
