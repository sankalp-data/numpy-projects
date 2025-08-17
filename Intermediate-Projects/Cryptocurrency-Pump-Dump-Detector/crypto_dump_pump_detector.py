import numpy as np
from datetime import datetime
from pprint import pprint

# Wherever I have written the path of my file, you have to replace it with your own file path.
with open(r"C:\Users\usar\Downloads\btc_hourly_ohlcv.csv",encoding="utf-8") as f: 
    headers = f.readline().strip().split(",")



data = np.genfromtxt(r"C:\Users\usar\Downloads\btc_hourly_ohlcv.csv",delimiter=",",dtype=None,encoding="utf-8",skip_header=1)
timestamps = np.array([row[0] for row in data],dtype="datetime64[s]")
volume = np.array([row[5] for row in data])
high = np.array([row[2] for row in data])
low = np.array([row[3] for row in data])
close = np.array([row[4] for row in data])
open_ = np.array([row[1] for row in data])
dates = np.array([np.datetime64(ts,"D") for ts in timestamps])


# Dataset start & end dates
start_date = dates.min()
end_date = dates.max()


def volume_spike_detector():

    from_date = input("From (YYYY-MM-DD): ")
    to_date = input("To (YYYY-MM-DD): ")
    details = {}

    try:
        check1 = np.datetime64(datetime.strptime(from_date,"%Y-%m-%d").date(),"D")
        check2 = np.datetime64(datetime.strptime(to_date,"%Y-%m-%d").date(),"D")

    except ValueError:
        print("Invalid date format!\nCorrect format: YYYY-MM-DD")
        return 
    
    if check1<start_date or check2>end_date:
        print("Dates are out of range!")
        return
    
    mask = (check1<=dates) & (check2>=dates)
    selected_vol = volume[mask]


    details[f"Average Volume from {check1} to {check2}"] = float(np.mean(selected_vol))
    spike_threshold = 1.5*(np.mean(selected_vol))
    indices = np.where(selected_vol > spike_threshold)[0]
    details["Spike Points"] = timestamps[indices].astype(str).tolist()

    
    pprint(details)
    print(f"TOTAL SPIKES: {len(details['Spike Points'])}")


'''IN PROGRESS---'''
# def moving_average():
    
#     number_of_days = int(input("Moving Average of last days: "))




        
    


    

    

    

    
    
    


    


    








    

    




    






    








