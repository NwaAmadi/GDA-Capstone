"""How does each group's usage vary by day of the week?"""

import pandas as pd


trip_data = pd.read_csv("Divvy_Trips_2019_2020_Q1_cleaned.csv", low_memory=False)
trip_data["starttime"] = pd.to_datetime(trip_data["starttime"])
trip_data["day_of_week"] = trip_data["starttime"].dt.day_name()
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

counts = trip_data.groupby(["source_year", "usertype", "day_of_week"]).size()
shares = counts.groupby(level=["source_year", "usertype"]).apply(
    lambda values: values / values.sum() * 100
)
shares.index = shares.index.droplevel([0, 1])
shares = shares.rename("share_pct").reset_index()
shares = shares.pivot_table(
    index="day_of_week", columns=["source_year", "usertype"], values="share_pct", fill_value=0
).reindex(day_order)
shares.columns = [f"{year} {rider}" for year, rider in shares.columns]
print("Share of each year's rider-type trips by weekday (%):")
print(shares.round(2))


"""
Output (share of each year's rider-type trips, %):
             2019 Casual  2019 Member  2020 Casual  2020 Member
Monday              8.17        14.19        10.01        16.36
Tuesday            11.78        17.04        10.86        18.42
Wednesday          10.75        16.94        12.24        16.91
Thursday           12.61        18.71        10.10        16.18
Friday             14.57        17.45        10.66        14.67
Saturday           25.87         8.57        15.43         7.96
Sunday             16.26         7.09        30.71         9.50

Interpretation:
Members made a larger share of their trips Monday through Friday in both
years. Casual riders were more weekend-oriented: Saturday was their largest
share in 2019, while Sunday was their largest share in 2020. These percentages
compare each group's own trips, rather than raw totals between groups.
"""
