import time
import threading
import pandas as pd
import streamlit as st
# from PV_Smoothing_Filter import Low_Pass_Filter
# from PV_Smoothing_Filter import FIR_Filter
from datetime import datetime
from pyModbusTCP.client import ModbusClient
import numpy as np
from Delta import read_conversion
from Delta import write_conversion

#address
address_PCS_Status = 4097
address_Charge_Power = 4103
address_Active_Power = 1816
#how many datas load
quantity = 1

#connect
connect = ModbusClient(host="192.168.1.136",port=502, auto_open=True, auto_close=True)


#check if connect
PCS_status = connect.read_holding_registers(address_PCS_Status,1)
print("PCS status: ", int(PCS_status[0]))

def turn_on_PCS():
    connect.write_single_register(4097, 1)
    PCS_status = connect.read_holding_registers(4097, 1)
    time.sleep(5)
    print("PCS status: ", int(PCS_status[0]))


# turn off PCS
def turn_off_PCS():
    connect.write_single_register(4103, 0)
    demand_power = connect.read_holding_registers(4103, 1)
    connect.write_single_register(4097, 0)
    PCS_status = connect.read_holding_registers(4097, 1)
    print("PCS status: ", int(PCS_status[0]))

def demand_0():
    connect.write_single_register(4103, 0)
    time.sleep(0.5)
    demand_power = connect.read_holding_registers(4103, 1)[0]


    


demand_0()


