import threading
import time


dispatch = 0

def tpc_command():
    global dispatch_counter
    global dispatch
    dispatch = input("TPC command: ")
    if dispatch == '':
        dispatch = 0
        print("TPC command: 0")
    else:
        print("TPC command:", dispatch)
    return dispatch
        
        



if __name__ == "__main__":
    t1 = threading.Thread(target = tpc_command)


    t1.start()
