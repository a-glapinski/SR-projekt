import json

import matplotlib.pyplot as plt
import numpy as np


class PartnerSimulationPlotter:
    def __init__(self, partner_id):
        self.partner_id = partner_id
        with open(f'logs/{self.partner_id}_factors.json', 'r') as json_file:
            partner_data = json.load(json_file)
            self.partner_data = partner_data['days']

    def plot_per_day_profit_gains(self):
        line = plt.plot(range(1, len(self.partner_data) + 1), [day['profitGain'] for day in self.partner_data],
                        label=self.partner_id)
        plt.xlabel('Days of simulation')
        plt.ylabel('Profit gain [EUR]')
        plt.grid()
        plt.legend(handles=line, loc='lower right')
        plt.show()

    def plot_accumulated_profit_gain(self):
        sums = np.cumsum([day['profitGain'] for day in self.partner_data], dtype=float)
        line = plt.plot(range(1, len(sums) + 1), sums, label=self.partner_id)
        plt.xlabel('Days of simulation')
        plt.ylabel('Accumulated profit gain [EUR]')
        plt.grid()
        plt.legend(handles=line, loc='upper right')
        plt.show()

    def plot_accumulated_profit_gain_ratio(self):
        pass

    def plot_sustained_profit(self):
        pass

    def plot_accumulated_sustained_profit(self):
        pass


if __name__ == '__main__':
    partner = 'C0F515F0A2D0A5D9F854008BA76EB537'
    plotter = PartnerSimulationPlotter(partner)
    plotter.plot_per_day_profit_gains()
    plotter.plot_accumulated_profit_gain()
    plotter.plot_sustained_profit()
