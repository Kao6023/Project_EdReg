import pandas as pd
from datetime import datetime
import time

from Dual_axis import Dual_Axis

class Waveform():
    def __init__(self):
        self.date = datetime.now()
    def maindata_list(self): 
        self.demand_power_list = pd.read_excel("schedule_EdReg.xlsx")["Energy_transfer(kW)"].to_list()
        self.time_list = pd.read_excel("schedule_EdReg.xlsx")["Time"].to_list()
        return self.energytransfer_list, self.time_list
    


if __name__ == '__name__':
    print(datetime.now())