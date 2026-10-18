"""How does average ride duration differ between the groups?"""

import pandas as pd


trip_data = pd.read_csv("Divvy_Trips_2019_2020_Q1_cleaned.csv", low_memory=False)
# Exclude missing, nonpositive, and over-24-hour durations from duration metrics.
valid_duration = trip_data["tripduration"].between(1, 24 * 60 * 60)
excluded = trip_data.loc[~valid_duration].groupby("source_year").size()
print("Trips excluded from duration metrics:")
print(excluded)

duration_summary = (
    trip_data.loc[valid_duration]
    .groupby(["source_year", "usertype"])["tripduration"]
    .agg(valid_trips="count", mean_seconds="mean", median_seconds="median")
)
duration_summary["mean_minutes"] = duration_summary["mean_seconds"] / 60
duration_summary["median_minutes"] = duration_summary["median_seconds"] / 60
duration_summary = duration_summary[
    ["valid_trips", "mean_minutes", "median_minutes"]
].round(2)
print("\nDuration in minutes:")
print(duration_summary)


"""
Output:
Trips excluded from duration metrics:
source_year
2019    72042
2020      500

Duration in minutes:
                      valid_trips  mean_minutes  median_minutes
source_year usertype                                           
2019        Casual           7651         10.28           10.38
            Member         285376          7.82            7.25
2020        Casual          48043         37.03           21.15
            Member         378344         11.50            8.57

Interpretation:
Casual riders had longer average and median rides than members in both years.
The difference was especially large in 2020, where the casual mean was pulled
above its median by a small number of long rides. Duration summaries omit
missing, nonpositive, and over-24-hour durations; 2019 has many missing
durations, so its reported averages use fewer trips.
"""
