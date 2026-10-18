"""How does each group's usage vary by time of day?"""

import pandas as pd


trip_data = pd.read_csv("Divvy_Trips_2019_2020_Q1_cleaned.csv", low_memory=False)
trip_data["starttime"] = pd.to_datetime(trip_data["starttime"])
trip_data["start_hour"] = trip_data["starttime"].dt.hour

counts = trip_data.groupby(["source_year", "usertype", "start_hour"]).size()
shares = counts.groupby(level=["source_year", "usertype"]).apply(
    lambda values: values / values.sum() * 100
)
shares.index = shares.index.droplevel([0, 1])
shares = shares.rename("share_pct").reset_index()
shares = shares.pivot_table(
    index="start_hour", columns=["source_year", "usertype"], values="share_pct", fill_value=0
).reindex(range(24), fill_value=0)
shares.columns = [f"{year} {rider}" for year, rider in shares.columns]
print("Share of each year's rider-type trips by starting hour (%):")
print(shares.round(2))


"""
Output (share of each year's rider-type trips, %):
            2019 Casual  2019 Member  2020 Casual  2020 Member
            start_hour                                                    
0                  0.66         0.45         0.64         0.37
1                  0.46         0.26         0.46         0.22
2                  0.48         0.18         0.28         0.14
3                  0.19         0.15         0.21         0.10
4                  0.16         0.28         0.12         0.27
5                  0.26         1.13         0.28         1.36
6                  0.61         3.77         0.70         3.92
7                  1.24         7.88         1.56         8.37
8                  2.87        10.90         2.77        10.95
9                  3.27         4.98         3.89         5.01
10                 4.71         3.32         5.69         3.42
11                 6.40         3.93         6.91         4.19
12                 7.78         4.49         8.76         4.81
13                10.72         4.35        10.34         4.80
14                10.88         4.33        11.15         4.59
15                11.76         5.82        10.88         6.11
16                11.03        10.74        10.54        10.48
17                10.11        13.93         9.62        12.75
18                 6.46         7.98         5.73         7.47
19                 3.60         4.64         3.38         4.42
20                 2.18         2.76         2.13         2.59
21                 1.71         1.90         1.86         1.88
22                 1.47         1.17         1.23         1.13
23                 1.00         0.67         0.86         0.64

Interpretation:
Member trips show pronounced morning and late-afternoon peaks, especially at
8 a.m. and 5 p.m. Casual trips are concentrated more in the afternoon, with
their largest hourly shares from 1 p.m. to 4 p.m. in both years. This pattern
is consistent with different trip rhythms, though these data do not establish
trip purpose.
"""
