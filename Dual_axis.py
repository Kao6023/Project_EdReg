from threading import Thread
from threading import Event
from pyModbusTCP.client import ModbusClient
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

            
class Dual_Axis:
    def __init__(self):
        self.color1 = 'r-'
        self.color2 = 'b-'
        self.color3 = 'g-'
        self.fig = plt.figure(figsize= (12,10), dpi = 80)
        self.ax1 = plt.subplot(111)
        self.ax2 = self.ax1.twinx()
        self.ax3 = self.ax1.twinx()
        
    def plot(self, list1, list2, list3, color1, color2, color3, 
             label1='list1', label2='list2', label3='list3', x_lim = None, y1_lim = None, y2_lim = None, y3_lim = None):
        self.ax1.plot(list1, color1, label=label1)
        self.ax2.plot(list2, color2, label=label2)
        self.ax3.plot(list3, color3, label=label3)
        # 數值範圍限制
        if (x_lim):
            self.ax1.set_xlim(x_lim)
        if (y1_lim):
            self.ax1.set_ylim(y1_lim)
        if (y2_lim):
            self.ax2.set_ylim(y2_lim)
        if (y3_lim):
            self.ax3.set_ylim(y2_lim)
    def draw(self,pause_time=1):
        self.fig.tight_layout()
        plt.draw()
        plt.pause(pause_time)

if __name__ == "__main__":
    while True:
        dataframe = pd.read_excel("test.xlsx")
        data1_list = dataframe['test_1'].values.tolist()
        data2_list = dataframe['test_2'].values.tolist()    
        dual_axis = Dual_Axis()
        dual_axis.plot(data1_list, data2_list,'r-','b-',label1='Data List 1', label2='Data List 2')
        dual_axis.draw()




    # while True:
    #     actural_load_list.append(np.average(test.load_array))
    #     act_list.append(test.Calculate())
    #     RealPower = c.read_holding_registers(2181,1)
    #     RealPower = np.array(RealPower, dtype="int16")
    #     load_list.append(RealPower[0])
    #     test.Predict(RealPower[0])

    #     dual_axis.plot(load_list,act_list, 'r-', 'g-', 'current_load', 'breaker')
    #     # ax1.plot(load_list,'r-')
    #     dual_axis.ax1.plot(actural_load_list,'b-',label='average_load')
    #     dual_axis.draw()
    #     # ax2.plot(act_list,'g-')
    #     # load_plot.set_ydata(load_list)
    #     # load_plot.set_xdata(time_list)
    #     # plt.draw()
    #     # plt.pause(1)