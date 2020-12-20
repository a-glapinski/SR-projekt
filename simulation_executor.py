import json
from collections import defaultdict

import yaml

from simulator_core import SimulatorCore


class SimulationExecutor:
    def __init__(self, config):
        self.data_directory = config['simulation']['partners_data_input_directory']
        self.logs_directory = config['simulation']['partners_logs_output_directory']
        self.partner_ids = config['simulation']['partners_to_involve_in_simulation']
        self.number_of_days = config['simulation']['number_of_simulation_steps']
        self.simulator_core = SimulatorCore(self.partner_ids, self.data_directory,
                                            npm_in_percents=config['simulation']['npm_in_percents'],
                                            optimizer_config=config['simulation']['optimizer'])

    def execute_simulation(self):
        all_days_simulation_data = {}
        for _ in range(self.number_of_days):
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
    with open('config.yaml', 'r') as config_file:
        yaml_config = yaml.safe_load(config_file)
    simulation_executor = SimulationExecutor(yaml_config)
    simulation_executor.execute_simulation()

# def plot(per_day_profit_gains):
#     plt.plot(range(1, len(per_day_profit_gains) + 1), per_day_profit_gains)
#     plt.xlabel('Days of simulation')
#     plt.ylabel('Profit gain')
#     plt.grid()
#     plt.show()
