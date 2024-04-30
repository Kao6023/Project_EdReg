import pandas as pd
from datetime import datetime
import time
import numpy as np
import math


class EdReg():
    def __init__(self, total_capacity):
        self.total_capacity = total_capacity # 得標容量
        self.ET_time = 0
        self.ET = 0
        self.emergency_counter = 0

    # 讀取excel資料轉成list形式。 Out:既定排程列表
    def scheduled_list(self): 
        self.energytransfer_list = pd.read_excel("schedule_EdReg.xlsx")["Energy_transfer(kW)"].to_list()
        self.time_list = pd.read_excel("schedule_EdReg.xlsx")["Time"].to_list()
        return self.energytransfer_list, self.time_list

    # 得到excel表內的既定排程功率(%)。 Out: 當下排程功率(前、現在、後)、排程時段
    def energy_transfer(self):
        now = datetime.now().time().replace(microsecond=0)
        for i in range(len(self.time_list)):
            if self.time_list[i] <= now < self.time_list[i+1] :
                self.ET_last = self.energytransfer_list[i-1] 
                self.ET_now = self.energytransfer_list[i] 
                self.ET_next = self.energytransfer_list[i+1] 
                self.ET_time = self.time_list[i] # 排程時段
                if i==0:
                    self.ET_last = 0
                print("Scheduled Period at: ", self.ET_time, " Energy transfer: ",self.energytransfer_list[i], "kW")
                print("Total power: ",self.total_capacity, "kW")

                break
            else:
                pass

        return self.ET_last, self.ET_now, self.ET_next

    # 根據排程功率，計算升降載率。 # Out: 當下的指定執行升降載量
    def updown_load(self):
        # 計算時間差
        now = datetime.now().time()
        print("Current time:", now)
        now = (now.minute * 60) + (now.second) # now --> 秒數
        schedule_period = (self.ET_time.minute * 60) + (self.ET_time.second) # self.ET_time --> 秒數
        duration = now - schedule_period # 時間差
        print("時間差(秒):", duration)
        
        # delta P，計算升降載率
        delta_P = (self.ET_now - self.ET_last) 
        if duration <300:
            Pn = ((duration * delta_P)/300 + self.ET_last)*1000 # ***(以W為單位)進行以下進位/
            if delta_P > 0: # delta P
                Pn = math.ceil(Pn) # 無條件進位
            elif delta_P < 0:
                Pn = math.floor(Pn) # 無條件捨去
            self.ET = Pn/1000 # ***(以kW為單位)
        else:
            self.ET = self.ET_now

        print("升降載率:", self.ET)


    # dReg0.5模式。 # In:頻率，Out:dReg指定執行功率、頻率
    def dReg_05(self, grid_frequency):
        if (grid_frequency <= 59.5):
            y = 1
            if (self.emergency_counter <= 300): # f<59.5
                self.emergency_counter += 1
            else:
                self.emergency_counter = 0
        elif (grid_frequency < 59.98):
            y = -2.083 * grid_frequency + 124.938
        elif (59.98 <= grid_frequency <= 60.02):
            y = 0
        elif (60.02 < grid_frequency < 60.5):
            y = -2.083 * grid_frequency + 125.022
        elif (grid_frequency >= 60.5):
            y = -1
        self.dReg_power = round((y * self.total_capacity), 3)

        return self.dReg_power # Power(kW)
    
    # Emergency f<59.5
    def emergency(self):
        for i in range(0, 300):
            y = 1
        return y

    # "Energy transfer power" + "dReg0.5 mode"。 # Out: 總輸出功率
    def total_power(self):
        Output_dReg = self.dReg_power # (kW)
        Output_ET = self.ET # (kW)
        Output_total = round((Output_dReg + Output_ET), 3) 
        if (Output_total >= 1*self.total_capacity ):
            Output_total = 1*self.total_capacity
        elif (Output_total <= -1*self.total_capacity ):
            Output_total = -1*self.total_capacity
        else:
            pass
        return Output_total # (kW) 小數點後三位


test = EdReg(10)
if __name__ == "__main__":
    while True:
        time.sleep(0.5)
        start = time.time()
        test.scheduled_list()
        test.energy_transfer()

        test.updown_load()
        end = time.time()
        print("程式執行時間: ", end - start)
        print()
