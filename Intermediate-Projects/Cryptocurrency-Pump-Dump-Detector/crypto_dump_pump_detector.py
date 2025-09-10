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

def parse_date(from_date=None, to_date=None, date=None):
    '''Parse and validate dates provided by the user.

    Args:
        from_date (str, optional): Start date in format YYYY-MM-DD.
        to_date (str, optional): End date in format YYYY-MM-DD.
        date (str, optional): Single date in format YYYY-MM-DD.

    Returns:
        numpy.datetime64 or tuple:
            - If `from_date` and `to_date` are provided → returns (check1, check2)
            - If `date` is provided → returns check3

    Raises:
        ValueError: If the date format is invalid or dates are out of dataset range.'''
    if from_date and to_date:
        try:
            check1 = np.datetime64(datetime.strptime(from_date, "%Y-%m-%d").date(), "D")
            check2 = np.datetime64(datetime.strptime(to_date, "%Y-%m-%d").date(), "D")
        except ValueError:
            raise ValueError("Invalid date format! Correct format: YYYY-MM-DD")

        if (check1 < start_date) | (check2 > end_date) | (check1 > end_date) | (check2 < start_date):
            raise ValueError("Date(s) are out of range!")
        return check1,check2

    elif date:
        try:
            check3 = np.datetime64(datetime.strptime(date, "%Y-%m-%d").date(), "D")
        except ValueError:
            raise ValueError("Invalid date format! Correct format: YYYY-MM-DD")

        if check3 not in dates:
            raise ValueError("Date is out of range.")

        return check3

    else:
        raise ValueError("Must provide either (from_date & to_date) or (date).")

        

def volume_spike_detector():
    """
    Detect spikes in trading volume within a given date range.

    Prompts the user for a start and end date, calculates the average volume,
    and flags all timestamps where volume exceeds 1.5 times the average.

    Returns:
        None. Prints the details including:
            - Average volume for the period
            - List of spike timestamps
            - Total number of spikes
    """
    check1,check2 = parse_date(from_date=input("From Date (YYYY-MM-YY): "),to_date=input("To Date (YYYY-MM-DD):"))
    details = {} 
    mask = (check1<=dates) & (check2>=dates)
    selected_timestamps = timestamps[mask]
    selected_vol = volume[mask]
    details[f"Average Volume from {check1} to {check2}"] = float(np.mean(selected_vol))
    spike_threshold = 1.5*(np.mean(selected_vol))
    indices = np.where(selected_vol > spike_threshold)[0]
    details["Spike Points"] = selected_timestamps[indices].astype(str).tolist()    
    pprint(details)
    print(f"TOTAL SPIKES: {len(details['Spike Points'])}")



def moving_average():
    """
    Calculate and display the moving average of the close price.

    Prompts the user to input the number of days for the moving average window.
    Computes rolling averages on close prices and prints the last 10 results.

    Returns:
        None. Prints:
            - Last 10 moving average values with timestamps
            - Total number of calculated points
    """
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
    """
    Analyze the high-low price range for one or multiple days.

    Prompts the user:
        - Option 1: Enter a single date → shows low, high, and daily range.
        - Option 2: Enter a date range → shows low, high, and range for each day.

    Returns:
        None. Prints details for each day analyzed.
    """
    want = input("Enter 1 for one day analysis\nEnter 2 for multiple days analysis: ")
    if want not in ["1", "2"]:
        print("Please reply in 1 or 2")
        return

    if want == "1":
        check = parse_date(date=input("Date (YYYY-MM-DD): "))
        mask = dates == check
        selected_low = low[mask]
        selected_high = high[mask]

        print(f"Details of {check}\n"
              f"Low = {np.min(selected_low)}\n"
              f"High = {np.max(selected_high)}\n"
              f"Range = {np.max(selected_high) - np.min(selected_low):.2f}")

    elif want == "2":
        check1,check2 = parse_date(from_date=input("From Date (YYYY-MM-DD): "),to_date=input("To Date (YYYY-MM-DD): "))
        num_days = (check2 - check1).astype(int) + 1  # correct number of days

        for i in range(num_days):
            current_day = check1 + i
            mask_day = dates == current_day

            if not np.any(mask_day):  # skip if no data for that day
                continue

            day_low = low[mask_day]
            day_high = high[mask_day]

            print(f"Details of {current_day}\n"
                  f"Low = {np.min(day_low)}\n"
                  f"High = {np.max(day_high)}\n"
                  f"Range = {np.max(day_high) - np.min(day_low):.2f}")



def combine_spike_detector():
    """
    Detect spikes based on combined conditions (volume, price change, and volatility).

    Prompts the user for a date range. Calculates average thresholds for:
        - Volume (1.5 * avg volume)
        - Price change (2 * avg price change between open and close)
        - Volatility (1.5 * avg high-low range)

    Flags timestamps where at least 2 out of 3 conditions are met.

    Returns:
        None. Prints:
            - List of combined spike timestamps
            - Total number of spikes detected
    """
    check1,check2 = parse_date(from_date=input("From Date (YYYY-MM-DD): "),to_date=input("To Date (YYYY-MM-DD): "))
    details = {}
    # Select dates
    selected_dates = (check1 <= dates) & (dates <= check2)

    # Calculate averages
    avg_price_change = np.mean(abs(close[selected_dates] - open_[selected_dates]))
    avg_range = np.mean(high[selected_dates] - low[selected_dates])
    avg_vol = np.mean(volume[selected_dates])

    # Thresholds
    vol_thresh = 1.5 * avg_vol
    price_thresh = 2 * avg_price_change
    vola_thresh = 1.5 * avg_range

    # Boolean checks (1 if condition met, else 0)
    conditions = (
        (volume[selected_dates] > vol_thresh).astype(int) +
        (abs(close[selected_dates] - open_[selected_dates]) > price_thresh).astype(int) +
        ((high[selected_dates] - low[selected_dates]) > vola_thresh).astype(int)
    )

    # A spike = at least 2 conditions true
    indices = np.where(conditions >= 2)[0]

    # Store results
    details["Spike Points"] = timestamps[selected_dates][indices].astype(str).tolist()

    print(f"TOTAL SPIKES: {len(details["Spike Points"])}")
    print("SPIKE POINTS📈\n")
    return np.array(details["Spike Points"]).reshape(len(details["Spike Points"]),1)


"""IN PROGRESS🚀"""
def post_spike_analysis():
    """
    Analyze market behavior after detected spikes.

    This function takes spike points (from combine_spike_detector) and evaluates
    post-spike performance, such as price movement, volatility, and volume trends
    within a specified time window after each spike.
    """
    spike_points = combine_spike_detector().flatten().astype(np.datetime64)
    spike_analysis = {} #Stores all post spike analysis data.
    n_hours_analysis = int(input("Next Hours/Days (Enter 1 for Hour Analysis or Enter 2 for Days Analysis): ")) #Decide how many periods (hours/days) after the spike you want to study.
    if n_hours_analysis not in [1,2]:
        raise ValueError("Reply either 1 or 2")
    if n_hours_analysis==1:
        hours = int(input("Hours: "))
        if hours not in list(range(1,9)):
            raise ValueError("Spike effect beyond 8 hours is negligible. Please choose 1-8 hours.")

        for timestamp in spike_points:
            after_hours_timestamp = timestamp + np.timedelta64(hours,"h") #Adding user's input hours in each spike points.
            selected_timestamp = (timestamp<=timestamps) & (after_hours_timestamp>=timestamps)
            spike_analysis[f"Post spike analysis after {hours}Hrs of {timestamp}"] = np.mean(volume[selected_timestamp])
        
    pprint(spike_analysis)
# print(volume[timestamps==np.datetime64("2024-03-17T06:00:00")])

# post_spike_analysis()