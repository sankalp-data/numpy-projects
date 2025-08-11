import numpy as np


with open(r"C:\Users\usar\Downloads\btc_hourly_ohlcv.csv",encoding="utf-8") as f:
    headers = f.readline().strip().split(",")



data = np.genfromtxt(r"C:\Users\usar\Downloads\btc_hourly_ohlcv.csv",delimiter=",",dtype=None,encoding="utf-8",skip_header=1)
# print(data)
# print(data[0])

def volume_spike_detector():
    '''Calculate average volume over past week.'''
    

    








