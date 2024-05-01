import pandas as pd
from datetime import datetime
import time

from Dual_axis import Dual_Axis

class Waveform():
    def __init__(self):
        today_date = datetime.today().strftime('%Y-%m-%d')
        self.file = f"{today_date}test.csv"
        print(self.file)

    def main_list(self): 
        self.grid_frequency_list = pd.read_csv(self.file)["Grid_frequency"].to_list()
        self.demand_power_list = pd.read_csv(self.file)["Demand_power"].to_list()
        self.active_power_list = pd.read_csv(self.file)["Active_power"].to_list()
    
    def show(self):
        dual_axis = Dual_Axis()
        dual_axis.plot(self.grid_frequency_list, self.demand_power_list, self.active_power_list,
                    'r-','b-','g-',"grid_frequency",'Demand_power','Active_power',None ,(59.4,60.6), (-12.5,12.5), (-10,10))
        dual_axis.draw(60)
        
    
if __name__ == "__main__":
    waveform = Waveform()
    start = time.time()
    waveform.main_list()
    waveform.show()
    end = time.time()
    print(end-start)