from pyModbusTCP.client import ModbusClient
import numpy as np

connect = ModbusClient(host="127.0.0.1",port=502, auto_open=True, auto_close=True)

# 將tcp收到的值轉為int16型態
def read_conversion(position):
    actual_value = connect.read_holding_registers(position, 1)
    converted_value = np.array(actual_value).astype('int16')
    return int(converted_value[0])

# 將寫入tcp的數值轉為uint16型態存入
def write_conversion(position, value):
    converted_value = np.array(value).astype('uint16')
    connect.write_single_register(position, converted_value)

# 讀取或寫入即時資料(PCS)
def PCS_mode(condition, value):
    if (condition == "read"):
        PCS_mode = read_conversion(4097)
        return PCS_mode
    elif (condition == "write"):
        PCS_mode = write_conversion(4097, value)

def power_demand(condition, value):
    if (condition == "read"):
        power_demand = read_conversion(4103)
        power_demand = power_demand/10
        return power_demand
    elif(condition == "write"):
        power_demand = write_conversion(4103, value*10)

def active_power():
    active_power = read_conversion(1816)
    return active_power/10 #單位(kW)



if __name__ == "__main__":
    value = read_conversion(4097)
    print(value)