import time
import pandas as pd
from datetime import datetime
from pyModbusTCP.client import ModbusClient
import numpy as np
import threading

import plotly.express as px
from Dual_axis import Dual_Axis
import Delta
from EdReg import EdReg


connect = ModbusClient(host="127.0.0.1",port=502, auto_open=True, auto_close=True)
mode_flag = 0 # 0:台電無命令 1:有

#　Check PCS and Turn ON
def initailly_checking():
    PCS_Status = Delta.PCS_mode("read", 1)
    if (PCS_Status == 0):
        condition = True
        Delta.PCS_mode("write", 1)
        time.sleep(5)
        PCS_Status = Delta.PCS_mode("read", 1)
    elif (PCS_Status == 2):
        print("PCS Fault")
        condition = False
    elif (PCS_Status == 1):
        condition = True
        pass
    print("PCS狀態: ", PCS_Status)
    return condition
    
PCS_condition = initailly_checking()

'''threading''' # 台電命令
dispatch = 0 
def tpc_command():
    global dispatch
    global mode_flag
    dispatch = input("TPC command: \n")
    if dispatch == '':
        dispatch = 0
    else:
        mode_flag = 1
    print("TPC command:", dispatch)
    dispatch = float(dispatch)
    return dispatch

def run_thread():
    t1 = threading.Thread(target = tpc_command)
    t1.start()

run_thread()


# grid frequency list
grid_frequency_list = pd.read_excel("grid_frequency_EdReg.xlsx")["frequency"].tolist()
count = 0
def data_grid_frequency(): # take out the next element of ("grid_frequency.xlsx")["frequency"]
    global count
    # count += 1
    count = (count+1) % len(grid_frequency_list) # 頻率重複循環
    return grid_frequency_list[count]

# # 初始化4列名稱，下一行中這五個欄位為 "初始值"
# initial_data={
#     'Time' : [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
#     'Grid_frequency' : [60],
#     'Demand_power' : [0],
#     'Active_power' : [0]
# }
# main_dataframe = pd.DataFrame(initial_data, index=[0]) #轉為表格形式的資料結構，放入新的表格中，作為未來更新的主表格


''' execute every seconds '''
class execute_once(EdReg):
    def __init__(self, total_capacity):
        self.emergency = 0 # f<59.5
        self.total_capacity = total_capacity # 得標容量
        initial_data={
            'Time' : [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'Grid_frequency' : [60],
            'Demand_power' : [0],
            'Active_power' : [0]
        }
        self.main_dataframe = pd.DataFrame(initial_data, index=[0])
        super().scheduled_list()

    def execute(self):
        global mode_flag
        global dispatch
        # time
        self.current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # grab a frequency data
        self.grid_frequency = data_grid_frequency()

        ''' calculate demand power '''
        # if emergency (f<59.5) --> run dReg0.5 900 sec
        if (self.grid_frequency <= 59.5):
            self.emergency = 1

        
        if (self.emergency == 0): 
            if (mode_flag != 0): # 台電命令模式 300 秒
                self.demand_power = super().dReg_05(self.grid_frequency) + dispatch
                print(mode_flag)
                mode_flag += 1
                if (mode_flag >= 10): # 300
                    print(mode_flag)
                    mode_flag = 0
                    dispatch = 0
                    run_thread()
            else:
                switch_mode = super().energy_transfer()[3]
                if (switch_mode == 0): # 僅 dReg0.5 模式
                    self.demand_power = super().dReg_05(self.grid_frequency)
                elif (switch_mode == 1): # 排程模式
                    super().updown_load()
                    super().dReg_05(self.grid_frequency)
                    self.demand_power = super().total_power()  

            # if (mode_flag == 0): # dReg0.5模式
            #     self.demand_power = super().dReg_05(self.grid_frequency)
            # elif (mode_flag == 1): # 排程模式
            #     ''' 繼承EdReg'''
            #     super().energy_transfer()
            #     super().updown_load()
            #     super().dReg_05(self.grid_frequency)
            #     self.demand_power = super().total_power()  
            # elif (mode_flag == 2): # 台電命令模式
            #     self.demand_power = super().dReg_05(self.grid_frequency) + dispatch
            # else:
            #     pass
            
        elif (self.emergency != 0): 
            if (self.emergency < 90): # 900
                self.emergency += 1
            elif (self.emergency >= 90): # 900
                self.emergency = 0
            self.demand_power = super().dReg_05(self.grid_frequency)

        # PCS 命令
        if (self.demand_power >= self.total_capacity): 
            self.demand_power = self.total_capacity
        elif (self.demand_power <= -1*self.total_capacity):
            self.demand_power = -1*self.total_capacity
        Delta.power_demand("write", self.demand_power)
        # wait for PCS to reaction
        time.sleep(0.5)

    
    def new_data_collection(self):
        self.current_time
        self.grid_frequency
        self.demand_power
        self.active_power = Delta.active_power()
            # self.SBSPM = quality_index(self.grid_frequency, (self.active_power/self.total_capacity) ) # (頻率, 功率百分比)

        # show in Terminal
        print("Grid frequency: ", self.grid_frequency, "Hz")
        print("Actaul output power: ", self.active_power,"kW")
            # print("SBSPM: ", self.SBSPM, "%")
        print()

        # collect values from all elements
        get_data = {
        'Time': [self.current_time],
        'Grid_frequency':[self.grid_frequency],
        'Demand_power':[self.demand_power],
        'Active_power':[self.active_power],
            # 'SBSPM': [self.SBSPM]
        }
        # make get_data to DataFrame format
        get_data_toframe = pd.DataFrame(get_data, index=[0])
        # data update to main_dataframe
        self.main_dataframe = pd.concat([self.main_dataframe, get_data_toframe], axis=0)
        # put main_dataframe to excel
        today = datetime.today().strftime('%Y-%m-%d')
        self.main_dataframe.to_csv(today+"test.csv", index = False)
        return self.main_dataframe


dual_axis = Dual_Axis()
Execute = execute_once(10)

drawing = 0
while PCS_condition:
    print()
    print("台電調度指令:", dispatch)

    start = time.time()

    Execute.execute()
    main_dataframe = Execute.new_data_collection()

    end = time.time()

    drawing += 1
    if (drawing >= 4):
        dual_axis.plot(main_dataframe['Grid_frequency'].to_list(), main_dataframe['Demand_power'].to_list(), main_dataframe['Active_power'].to_list(),
                        'r-','b-','g-',"grid_frequency",'Demand_power','Active_power',None ,(59.4,60.6), (-12.5,12.5), (-10,10))
        dual_axis.draw(0.1)
        drawing = 0
    else:
        pass
    execution_time = end - start
    print("程式執行時間: ", execution_time, "秒")
    time.sleep(0.3)
# test
# test with fetch feature

