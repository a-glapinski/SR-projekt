import json
from collections import defaultdict

from simulator_core import SimulatorCore


class SimulationExecutor:
    def __init__(self, partner_ids, partners_data_directory, number_of_days, logs_directory):
        self.partner_ids = partner_ids
        self.data_directory = partners_data_directory
        self.number_of_days = number_of_days
        self.logs_directory = logs_directory
        self.simulator_core = SimulatorCore(self.partner_ids, self.data_directory)

    def execute_simulation(self):
        all_days_simulation_data = {}
        for i in range(self.number_of_days):
            date, one_day_simulation_data = self.simulator_core.next_day()
            all_days_simulation_data[date] = one_day_simulation_data

        processed_partners_data = defaultdict(lambda: {'days': []})
        for date, one_day_simulation_data in all_days_simulation_data.items():
            for partner_id, one_day_partner_simulation_data in one_day_simulation_data.items():
                processed_partners_data[partner_id]['days'].append(
                    one_day_partner_simulation_data[1].to_dict_with_date(date))

        for partner_id, data in processed_partners_data.items():
            with open(f'{self.logs_directory}/{partner_id}.json', 'w') as outfile:
                json.dump(data, outfile, indent=2)


if __name__ == '__main__':
    partners = ['C0F515F0A2D0A5D9F854008BA76EB537', '04A66CE7327C6E21493DA6F3B9AACC75']
    simulation_executor = SimulationExecutor(partners, 'out', 90, 'logs')
    simulation_executor.execute_simulation()

# def plot(per_day_profit_gains):
#     plt.plot(range(1, len(per_day_profit_gains) + 1), per_day_profit_gains)
#     plt.xlabel('Days of simulation')
#     plt.ylabel('Profit gain')
#     plt.grid()
#     plt.show()
