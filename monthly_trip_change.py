"""How does each group's usage change across months or seasons?"""

import pandas as pd


trip_data = pd.read_csv("Divvy_Trips_2019_2020_Q1_cleaned.csv", low_memory=False)
trip_data["starttime"] = pd.to_datetime(trip_data["starttime"])
trip_data["month"] = trip_data["starttime"].dt.month
monthly = (
    trip_data.groupby(["source_year", "usertype", "month"])
    .size()
    .rename("trips")
    .reset_index()
)
month_start = pd.to_datetime(
    monthly["source_year"].astype(str) + "-" + monthly["month"].astype(str) + "-01"
)
monthly["average_trips_per_day"] = monthly["trips"] / month_start.dt.days_in_month
profile = monthly.pivot_table(
    index="month", columns=["source_year", "usertype"], values="average_trips_per_day"
).reindex([1, 2, 3])
profile.index = ["Jan", "Feb", "Mar"]
profile.columns = [f"{year} {rider}" for year, rider in profile.columns]
print("Average trips per calendar day by month:")
print(profile.round(2))


"""
Output (average trips per calendar day):
     2019 Casual  2019 Member  2020 Casual  2020 Member
Jan       148.45      3182.90       251.13      4390.29
Feb        94.21      3341.00       443.79      4369.48
Mar       513.65      4828.65       897.58      3728.81

Interpretation:
In both Q1 periods, casual trip volume per day rose sharply by March. Member
trips per day increased from January to March in 2019, but declined across the
three months in 2020. The available data covers January through March only, so
it cannot establish full-year seasonality.
"""
