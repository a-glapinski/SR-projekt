import json

import matplotlib.pyplot as plt
import numpy as np


class PartnerSimulationPlotter:
    def __init__(self, partner_id):
        self.partner_id = partner_id
        with open(f'logs/{self.partner_id}_factors.json', 'r') as json_file:
            partner_data = json.load(json_file)
            self.partner_data = partner_data['days']

    def plot_profit_gain(self):
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

    def plot_sustained_profit(self):
        line = plt.plot(range(1, len(self.partner_data) + 1), [day['sustainedProfit'] for day in self.partner_data],
                        label=self.partner_id)
        plt.xlabel('Days of simulation')
        plt.ylabel('Sustained profit [EUR]')
        plt.grid()
        plt.legend(handles=line, loc='lower right')
        plt.show()

    def plot_accumulated_sustained_profit(self):
        sums = np.cumsum([day['sustainedProfit'] for day in self.partner_data], dtype=float)
        line = plt.plot(range(1, len(sums) + 1), sums, label=self.partner_id)
        plt.xlabel('Days of simulation')
        plt.ylabel('Accumulated sustained profit [EUR]')
        plt.grid()
        plt.legend(handles=line, loc='lower right')
        plt.show()

    def plot_accumulated_profit_gain_ratio(self):
        profit_gain_sums = np.cumsum([day['profitGain'] for day in self.partner_data], dtype=float)
        sustained_profit_sums = np.cumsum([day['sustainedProfit'] for day in self.partner_data], dtype=float)
        ratios = profit_gain_sums / sustained_profit_sums
        line = plt.plot(range(1, len(ratios) + 1), ratios, label=self.partner_id)
        plt.xlabel('Days of simulation')
        plt.ylabel('Accumulated profit gain ratio [EUR/EUR]')
        plt.grid()
        plt.legend(handles=line, loc='upper right')
        plt.show()

    def plot_clicks_savings(self):
        line = plt.plot(range(1, len(self.partner_data) + 1), [day['clicksSavings'] for day in self.partner_data],
                        label=self.partner_id)
        plt.xlabel('Days of simulation')
        plt.ylabel('Clicks savings [EUR]')
        plt.grid()
        plt.legend(handles=line, loc='lower right')
        plt.show()

    def plot_sale_losses(self):
        line = plt.plot(range(1, len(self.partner_data) + 1), [day['saleLosses'] for day in self.partner_data],
                        label=self.partner_id)
        plt.xlabel('Days of simulation')
        plt.ylabel('Sale losses [EUR]')
        plt.grid()
        plt.legend(handles=line, loc='lower right')
        plt.show()

    def plot_profit_losses(self):
        line = plt.plot(range(1, len(self.partner_data) + 1), [day['profitLosses'] for day in self.partner_data],
                        label=self.partner_id)
        plt.xlabel('Days of simulation')
        plt.ylabel('Profit losses [EUR]')
        plt.grid()
        plt.legend(handles=line, loc='lower right')
        plt.show()


if __name__ == '__main__':
    partner = 'C0F515F0A2D0A5D9F854008BA76EB537'
    plotter = PartnerSimulationPlotter(partner)
    plotter.plot_profit_gain()
    plotter.plot_accumulated_profit_gain()
    plotter.plot_sustained_profit()
    plotter.plot_accumulated_sustained_profit()
    plotter.plot_accumulated_profit_gain_ratio()
    plotter.plot_clicks_savings()
    plotter.plot_sale_losses()
    plotter.plot_profit_losses()
