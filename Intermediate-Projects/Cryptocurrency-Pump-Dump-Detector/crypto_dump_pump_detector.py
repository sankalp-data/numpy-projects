import numpy as np
from datetime import datetime
from collections import Counter,OrderedDict
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
    
    def high_low_range(self,want: int):
        if want==1:
            d = self.parse_date(date=input("Date (YYYY-MM-DD): "))
            mask = d == self.dates
            selected_low = self.low[mask]
            selected_high = self.high[mask]
            print(f"Details of {d}\n"
              f"Low = {np.min(selected_low)}\n"
              f"High = {np.max(selected_high)}\n"
              f"Range = {np.max(selected_high) - np.min(selected_low):.2f}")
        elif want==2:
            start,end = self.parse_date(from_date=input("From (YYYY-MM-DD): "),to_date=input("To Date (YYYY-MM-DD): "))
            num_days = (end - start).astype(int) + 1  # correct number of days

            for i in range(num_days):
                current_day = start + i
                mask_day = self.dates == current_day

                if not np.any(mask_day):  # skip if no data for that day
                    continue

                day_low = self.low[mask_day]
                day_high = self.high[mask_day]

                print(f"Details of {current_day}\n"
                    f"Low = {np.min(day_low)}\n"
                    f"High = {np.max(day_high)}\n"
                    f"Range = {np.max(day_high) - np.min(day_low):.2f}")
        else:
            print("Invalid Choice")
        
    def combine_spike_detector(self,from_date,to_date):
        start,end = self.parse_date(from_date=from_date,to_date=to_date)
        details = {}
        # Select dates
        selected_dates = (start <= self.dates) & (self.dates <= end)

        # Calculate averages
        avg_price_change = np.mean(abs(self.close[selected_dates] - self.open[selected_dates]))
        avg_range = np.mean(self.high[selected_dates] - self.low[selected_dates])
        avg_vol = np.mean(self.volume[selected_dates])

        # Thresholds
        vol_thresh = 1.5 * avg_vol
        price_thresh = 2 * avg_price_change
        vola_thresh = 1.5 * avg_range

        # Boolean checks (1 if condition met, else 0)
        conditions = (
            (self.volume[selected_dates] > vol_thresh).astype(int) +
            (abs(self.close[selected_dates] - self.open[selected_dates]) > price_thresh).astype(int) +
            ((self.high[selected_dates] - self.low[selected_dates]) > vola_thresh).astype(int)
        )

        # A spike = at least 2 conditions true
        indices = np.where(conditions >= 2)[0]

        # Store results
        details["Spike Points"] = self.timestamps[selected_dates][indices].astype(str).tolist()

        print(f"TOTAL SPIKES: {len(details["Spike Points"])}")
        print("SPIKE POINTS📈\n")
        return np.array(details["Spike Points"]).reshape(len(details["Spike Points"]),1)
    
    def moving_average(self,days: int):
            if days <= 0:
                print("Days must be greater than 0")
                return

            # moving average on CLOSE price
            window_size = days
            result = []

            # loop through dataset with sliding window
            for i in range(len(self.close) - window_size + 1):
                avg = np.mean(self.close[i:i+window_size])
                result.append((self.timestamps[i+window_size-1], float(avg)))

            # show last 10 values for quick view
            print(f"\nMoving Average ({days} days) calculated on Close Price:")
            for ts, val in result[-10:]:   # last 10 values
                print(str(ts), "->", val)

            print(f"\nTOTAL MOVING AVERAGE POINTS: {len(result)}")

    def post_spike_analysis(self, hours: int, from_date, to_date):

        if not 1 <= hours <= 8:
            raise ValueError("Please enter hours between 1 and 8. Beyond 8 hours, spike change is negligible.")


        spike_points = (
            self.combine_spike_detector(from_date=from_date, to_date=to_date)
            .flatten()
            .astype(np.datetime64)
        )


        for spike_point in spike_points:

            end_time = spike_point + np.timedelta64(hours, "h")


            mask = (self.timestamps > spike_point) & (self.timestamps <= end_time)

            if not np.any(mask):
                print(f"No data available for {hours} hours after spike at {spike_point}")
                continue


            spike_vol = self.volume[self.timestamps == spike_point][0]
            future_avg_vol = np.mean(self.volume[mask])
            volume_change = ((future_avg_vol - spike_vol) / spike_vol) * 100

            spike_price = self.close[self.timestamps == spike_point][0]
            future_avg_price = np.mean(self.close[mask])
            price_change = ((future_avg_price - spike_price) / spike_price) * 100

            spike_range = self.high[self.timestamps == spike_point][0] - self.low[self.timestamps == spike_point][0]
            future_avg_range = np.mean(self.high[mask] - self.low[mask])
            range_change = ((future_avg_range - spike_range) / spike_range) * 100 if spike_range != 0 else 0

            
            print(f"\n📊 Post Spike Analysis ({hours} hrs) for {spike_point}:")
            print(f"  - Volume Change: {volume_change:.2f}%")
            print(f"  - Price Change: {price_change:.2f}%")
            print(f"  - Range Change: {range_change:.2f}%")

    #In Progress🚀    
    def spike_seasonality(self, from_date, to_date):

        # Get spike timestamps
        spike_points = (
            self.combine_spike_detector(from_date=from_date, to_date=to_date)
            .flatten()
            .astype(np.datetime64)
        )

        if len(spike_points) == 0:
            print("⚠️ No spikes found in the given range.")
            return OrderedDict()

        # Extract hour part
        hours = [str(np.datetime64(ts, "h"))[-2:] for ts in spike_points]

        # Count spikes per hour
        counts = Counter(hours)

        # Sort by natural hour order (00–23)
        ordered_counts = OrderedDict(sorted(counts.items(), key=lambda x: int(x[0])))

        # Pretty-print summary
        print("\n🕒 Spike Seasonality (by Hour of Day)")
        print("Hour | Count")
        print("-----|------")
        for hour, count in ordered_counts.items():
            print(f"{hour}   | {count}")

        return ordered_counts
