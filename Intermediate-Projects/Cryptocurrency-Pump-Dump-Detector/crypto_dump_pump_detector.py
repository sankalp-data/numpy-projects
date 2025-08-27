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


def moving_average():
    try:
        days = int(input("Enter number of days for moving average: "))
    except ValueError:
        print("Invalid number!")
        return

    if days <= 0:
        print("Days must be greater than 0")
        return

    # moving average on CLOSE price
    window_size = days
    result = []

    # loop through dataset with sliding window
    for i in range(len(close) - window_size + 1):
        avg = np.mean(close[i:i+window_size])
        result.append((timestamps[i+window_size-1], float(avg)))

    # show last 10 values for quick view
    print(f"\nMoving Average ({days} days) calculated on Close Price:")
    for ts, val in result[-10:]:   # last 10 values
        print(str(ts), "->", val)

    print(f"\nTOTAL MOVING AVERAGE POINTS: {len(result)}")


def high_low_range():
    want = input("Enter 1 for one day analysis\nEnter 2 for multiple days analysis: ")
    if want not in ["1", "2"]:
        print("Please reply in 1 or 2")
        return

    if want == "1":
        date = input("Date (YYYY-MM-DD): ")
        try:
            check = np.datetime64(datetime.strptime(date, "%Y-%m-%d").date(), "D")
        except ValueError:
            print("Invalid Date Format!")
            return
        if check not in dates:
            print("Date is out of range.")
            return

        mask = dates == check
        selected_low = low[mask]
        selected_high = high[mask]

        print(f"Details of {check}\n"
              f"Low = {np.min(selected_low)}\n"
              f"High = {np.max(selected_high)}\n"
              f"Range = {np.max(selected_high) - np.min(selected_low):.2f}")

    elif want == "2":
        from_date = input("From (YYYY-MM-DD): ")
        to_date = input("To (YYYY-MM-DD): ")

        try:
            check1 = np.datetime64(datetime.strptime(from_date, "%Y-%m-%d").date(), "D")
            check2 = np.datetime64(datetime.strptime(to_date, "%Y-%m-%d").date(), "D")
        except ValueError:
            print("Invalid Date Format!")
            return

        if check1 < start_date or check2 > end_date:
            print("Dates are out of range!")
            return

        num_days = (check2 - check1).astype(int) + 1  # correct number of days

        for i in range(num_days):
            current_day = check1 + np.timedelta64(i, "D")
            mask_day = dates == current_day

            if not np.any(mask_day):  # skip if no data for that day
                continue

            day_low = low[mask_day]
            day_high = high[mask_day]

            print(f"Details of {current_day}\n"
                  f"Low = {np.min(day_low)}\n"
                  f"High = {np.max(day_high)}\n"
                  f"Range = {np.max(day_high) - np.min(day_low):.2f}")