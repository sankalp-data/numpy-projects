import numpy as np
from datetime import datetime
from pprint import pprint

# Wherever I have written the path of my file, you have to replace it with your own file path.

class CryptoAnalyzer:
    def __init__(self,csv_file: str):
        data = np.genfromtxt(csv_file, delimiter=",", dtype=None, encoding="utf-8", skip_header=1)
        self.timestamps = np.array([row[0] for row in data], dtype="datetime64[s]")
        self.dates = np.array([ts.astype("datetime64[D]") for ts in self.timestamps])
        self.open = np.array([row[1] for row in data], dtype=float)
        self.high = np.array([row[2] for row in data], dtype=float)
        self.low = np.array([row[3] for row in data], dtype=float)
        self.close = np.array([row[4] for row in data], dtype=float)
        self.volume = np.array([row[5] for row in data], dtype=float)
        self.start_date = self.dates.min()
        self.end_date = self.dates.max()
    
    def parse_date(self, from_date=None, to_date=None, date=None):
        if from_date and to_date:
            try:
                start = np.datetime64(datetime.strptime(from_date,"%Y-%m-%d").date(),"D")
                end = np.datetime64(datetime.strptime(to_date,"%Y-%m-%d").date(),"D")
            except ValueError:
                raise ValueError("Incorrect date(s) format!")
            if start < self.start_date or end > self.end_date or start > self.end_date or end < self.start_date:
                raise ValueError("Date(s) out of range")
            return start, end
        elif date:
            try:
                d = np.datetime64(datetime.strptime(date,"%Y-%m-%d").date(),"D")
            except ValueError:
                raise ValueError("Incorrect date(s) format!")
            if d not in self.dates:
                raise ValueError("Date out of range")
            return d
        else:
            raise ValueError("Provide from_date & to_date or date")
    
    def volume_spike_detector(self, from_date, to_date):
        start, end = self.parse_date(from_date=from_date, to_date=to_date)
        mask = (self.dates >= start) & (self.dates <= end)
        avg_vol = np.mean(self.volume[mask])
        spikes = self.timestamps[mask][self.volume[mask] > 1.5 * avg_vol]
        print(f"TOTAL SPIKES: {len(spikes)}")
        return spikes
    
    # def high_low_range(self,want: int):
    #     if want==1:
    #         d = self.parse_date(date=input("Date (YYYY-MM-DD): "))
    #         mask = d == self.dates
    #         selected_low = self.low[mask]
    #         selected_high = self.high[mask]
    #         print(f"Details of {d}\n"
    #           f"Low = {np.min(selected_low)}\n"
    #           f"High = {np.max(selected_high)}\n"
    #           f"Range = {np.max(selected_high) - np.min(selected_low):.2f}")
    #     elif want==2:
    #         start,end = self.parse_date(from_date=input("Start (YYYY-MM-DD): "),to_date=input("To Date (YYYY-MM-DD): "))




# # === Feature 2: Moving Average ===
# def moving_average():
#     """
#     Calculate and display the moving average of the close price.

#     Prompts the user to input the number of days for the moving average window.
#     Computes rolling averages on close prices and prints the last 10 results.

#     Returns:
#         None. Prints:
#             - Last 10 moving average values with timestamps
#             - Total number of calculated points
#     """
#     try:
#         days = int(input("Enter number of days for moving average: "))
#     except ValueError:
#         print("Invalid number!")
#         return

#     if days <= 0:
#         print("Days must be greater than 0")
#         return

#     # moving average on CLOSE price
#     window_size = days
#     result = []

#     # loop through dataset with sliding window
#     for i in range(len(close) - window_size + 1):
#         avg = np.mean(close[i:i+window_size])
#         result.append((timestamps[i+window_size-1], float(avg)))

#     # show last 10 values for quick view
#     print(f"\nMoving Average ({days} days) calculated on Close Price:")
#     for ts, val in result[-10:]:   # last 10 values
#         print(str(ts), "->", val)

#     print(f"\nTOTAL MOVING AVERAGE POINTS: {len(result)}")

# # === Feature 3: High-Low Range ===
# def high_low_range():
#     """
#     Analyze the high-low price range for one or multiple days.

#     Prompts the user:
#         - Option 1: Enter a single date → shows low, high, and daily range.
#         - Option 2: Enter a date range → shows low, high, and range for each day.

#     Returns:
#         None. Prints details for each day analyzed.
#     """
#     want = input("Enter 1 for one day analysis\nEnter 2 for multiple days analysis: ")
#     if want == "1":
#         check = parse_date(date=input("Date (YYYY-MM-DD): "))
#         mask = dates == check
#         selected_low = low[mask]
#         selected_high = high[mask]

#         print(f"Details of {check}\n"
#               f"Low = {np.min(selected_low)}\n"
#               f"High = {np.max(selected_high)}\n"
#               f"Range = {np.max(selected_high) - np.min(selected_low):.2f}")

#     elif want == "2":
#         check1,check2 = parse_date(from_date=input("From Date (YYYY-MM-DD): "),to_date=input("To Date (YYYY-MM-DD): "))
#         num_days = (check2 - check1).astype(int) + 1  # correct number of days

#         for i in range(num_days):
#             current_day = check1 + i
#             mask_day = dates == current_day

#             if not np.any(mask_day):  # skip if no data for that day
#                 continue

#             day_low = low[mask_day]
#             day_high = high[mask_day]

#             print(f"Details of {current_day}\n"
#                   f"Low = {np.min(day_low)}\n"
#                   f"High = {np.max(day_high)}\n"
#                   f"Range = {np.max(day_high) - np.min(day_low):.2f}")
#     else:
#         print("Invalid choice.")


# # === Feature 4: Combined Spike Detector ===
# def combine_spike_detector():
#     """
#     Detect spikes based on combined conditions (volume, price change, and volatility).

#     Prompts the user for a date range. Calculates average thresholds for:
#         - Volume (1.5 * avg volume)
#         - Price change (2 * avg price change between open and close)
#         - Volatility (1.5 * avg high-low range)

#     Flags timestamps where at least 2 out of 3 conditions are met.

#     Returns:
#         None. Prints:
#             - List of combined spike timestamps
#             - Total number of spikes detected
#     """
#     check1,check2 = parse_date(from_date=input("From Date (YYYY-MM-DD): "),to_date=input("To Date (YYYY-MM-DD): "))
#     details = {}
#     # Select dates
#     selected_dates = (check1 <= dates) & (dates <= check2)

#     # Calculate averages
#     avg_price_change = np.mean(abs(close[selected_dates] - open_[selected_dates]))
#     avg_range = np.mean(high[selected_dates] - low[selected_dates])
#     avg_vol = np.mean(volume[selected_dates])

#     # Thresholds
#     vol_thresh = 1.5 * avg_vol
#     price_thresh = 2 * avg_price_change
#     vola_thresh = 1.5 * avg_range

#     # Boolean checks (1 if condition met, else 0)
#     conditions = (
#         (volume[selected_dates] > vol_thresh).astype(int) +
#         (abs(close[selected_dates] - open_[selected_dates]) > price_thresh).astype(int) +
#         ((high[selected_dates] - low[selected_dates]) > vola_thresh).astype(int)
#     )

#     # A spike = at least 2 conditions true
#     indices = np.where(conditions >= 2)[0]

#     # Store results
#     details["Spike Points"] = timestamps[selected_dates][indices].astype(str).tolist()

#     print(f"TOTAL SPIKES: {len(details["Spike Points"])}")
#     print("SPIKE POINTS📈\n")
#     return np.array(details["Spike Points"]).reshape(len(details["Spike Points"]),1)


# """IN PROGRESS🚀"""
# # === Feature 5: Post-Spike Analysis ===
# def post_spike_analysis():
#     """
#     Analyze market behavior after detected spikes.

#     This function takes spike points (from combine_spike_detector) and evaluates
#     post-spike performance, such as price movement and volume trends
#     within a specified time window after each spike.
#     """
#     spike_points = combine_spike_detector().flatten().astype(np.datetime64)
#     spike_analysis = {} #Stores all post spike analysis data.
#     n_hours_analysis = int(input("Next Hours/Days (Enter 1 for Hour Analysis or Enter 2 for Days Analysis): ")) #Decide how many periods (hours/days) after the spike you want to study.
#     if n_hours_analysis not in [1,2]:
#         raise ValueError("Reply either 1 or 2")
#     if n_hours_analysis==1:
#         hours = int(input("Hours: "))
#         if hours not in list(range(1,9)):
#             raise ValueError("Spike effect beyond 8 hours is negligible. Please choose 1-8 hours.")
        
#         for timestamp in spike_points:
#             after_hours_timestamp = timestamp + np.timedelta64(hours,"h") #Adding user's input hours in each spike points.
#             selected_timestamp = (timestamp<timestamps) & (after_hours_timestamp>=timestamps)
#             selected_volume = float(np.mean(volume[selected_timestamp])) - volume[timestamp==timestamps]
#             selected_price = float(np.mean(close[selected_timestamp])) - close[timestamp==timestamps]
#             spike_analysis[f"Post Spike Analysis After {hours}Hrs of {timestamp}"] = f"Volume Change After Spike: {((selected_volume/volume[timestamp==timestamps])*100)[0]:.2f}% Price Change After Spike: {(((selected_price/close[timestamp==timestamps]))*100)[0]:.2f}%"
        
#     elif n_hours_analysis==2:
#         days = int(input("Days (1-3): "))
#         if days not in list(range(1,4)):
#             raise ValueError("Spike effect beyond 3 days is negligible. Please choose 1-3 days.")
#         for timestamp2 in spike_points:
#             after_hours_timestamp2 = timestamp2 + np.timedelta64(days,"D")
#             selected_timestamp2 = (timestamp2<timestamps) & (after_hours_timestamp2>=timestamps)
#             selected_volume2 = float(np.mean(volume[selected_timestamp2])) - volume[timestamp2==timestamps]
#             selected_price2 = float(np.mean(close[selected_timestamp2])) - close[timestamp2==timestamps]
#             spike_analysis[f"Post Spike Analysis After {days} Days of {timestamp2}"] = f"Volume Change After Spike: {((selected_volume2/volume[timestamp2==timestamps])*100)[0]:.2f}% Price Change After Spike: {(((selected_price2/close[timestamp2==timestamps]))*100)[0]:.2f}%"
#     pprint(spike_analysis)























