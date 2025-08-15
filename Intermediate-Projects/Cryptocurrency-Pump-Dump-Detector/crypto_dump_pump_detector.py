import numpy as np
from datetime import datetime

# Wherever I have written the path of my file, you have to replace it with your own file path.
with open(r"C:\Users\usar\Downloads\btc_hourly_ohlcv.csv",encoding="utf-8") as f: 
    headers = f.readline().strip().split(",")



data = np.genfromtxt(r"C:\Users\usar\Downloads\btc_hourly_ohlcv.csv",delimiter=",",dtype=None,encoding="utf-8",skip_header=1)
timestamps = np.array([row[0] for row in data],dtype="datetime64[s]")
print(timestamps[0])
volume = np.array([row[5] for row in data])
high = np.array([row[2] for row in data])
low = np.array([row[3] for row in data])
close = np.array([row[4] for row in data])
open_ = np.array([row[1] for row in data])
dates = np.array([np.datetime64(ts,"D") for ts in timestamps])

# Dataset start & end dates
# Dataset start & end dates
start_date = dates.min()
end_date = dates.max()

def volume_spike_detector():
    """Detect volume spikes based on past week's average volume."""

    from_date = input("From (YYYY-MM-DD): ")
    to_date = input("To (YYYY-MM-DD): ")

    try:
        # Convert to numpy.datetime64[D]
        check1 = np.datetime64(datetime.strptime(from_date, "%Y-%m-%d").date(), 'D')
        check2 = np.datetime64(datetime.strptime(to_date, "%Y-%m-%d").date(), 'D')
    except ValueError:
        print("❌ Invalid format! Please use YYYY-MM-DD format only.")
        return

    # Validate range
    if check1 < start_date or check2 > end_date:
        print(f"❌ Date range is outside dataset ({start_date} to {end_date}).")
        return

    # Filter volumes within the date range
    mask = (dates >= check1) & (dates <= check2)
    selected_volumes = volume[mask]

    if len(selected_volumes) == 0:
        print("No data for this date range.")
        return

    # Calculate average volume
    avg_volume = np.mean(selected_volumes)

    # Identify spikes (50% higher than average)
    spike_threshold = avg_volume * 1.5
    spikes = selected_volumes[selected_volumes > spike_threshold]

    # Output results
    print(f"📊 Average volume in range: {avg_volume:.2f}")
    print(f"📈 Spike threshold: {spike_threshold:.2f}")
    print(f"🚀 Number of spikes: {len(spikes)}")
    if len(spikes) > 0:
        print("Spike volumes:", spikes)
        

'''⚠️IN  PROGRESS''' 
# def price_range():
#     '''Check Price Range is normal or not'''
#     date = input("Date (YYYY-MM-DD):")
#     time = input("Time (HH:MM:SS): ")

#     try:
#         check1 = np.datetime64(datetime.strptime(date,"%Y-%m-%d").date(),"D")
#         check2 = np.datetime64(datetime.strptime(time,"%H:%M:%S").time(),"s")
#     except ValueError:
#         print("Invalid Time/Date format, correct format:\nFor date: YYYY-MM-DD\nFor time: HH:MM:SS")
#         return
    








    

    




    






    








