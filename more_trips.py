"""Which group takes more trips?"""

import pandas as pd


trip_data = pd.read_csv("Divvy_Trips_2019_2020_Q1_cleaned.csv", low_memory=False)
summary = trip_data.groupby(["source_year", "usertype"]).size().rename("trips").to_frame()
summary["share_pct"] = (
    summary["trips"]
    / summary.groupby(level="source_year")["trips"].transform("sum")
    * 100
).round(2)
print("Q1 trips by year and rider type:")
print(summary)


"""
Output:
                       trips  share_pct
source_year usertype                   
2019        Casual     23163       6.34
            Member    341906      93.66
2020        Casual     48480      11.36
            Member    378407      88.64

Interpretation:
Annual members took substantially more trips than casual riders in both Q1
periods. Casual riders accounted for a larger share in 2020 Q1 (11.36%) than
in 2019 Q1 (6.34%). These are Q1 comparisons, not full-year totals.
"""
