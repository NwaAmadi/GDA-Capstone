"""Which starting and ending stations are most popular with each group?"""

import pandas as pd


trip_data = pd.read_csv("Divvy_Trips_2019_2020_Q1_cleaned.csv", low_memory=False)
trip_data["start_station"] = trip_data["from_station_name"].fillna(
    trip_data["start_station_name"]
)
trip_data["end_station"] = trip_data["to_station_name"].fillna(
    trip_data["end_station_name"]
)

station_results = []
for year in sorted(trip_data["source_year"].dropna().unique()):
    for rider in ["Casual", "Member"]:
        subset = trip_data.loc[
            (trip_data["source_year"] == year) & (trip_data["usertype"] == rider)
        ]
        for role, column in [("Start", "start_station"), ("End", "end_station")]:
            top_stations = subset[column].dropna().value_counts().head(5)
            for rank, (station, trips) in enumerate(top_stations.items(), start=1):
                station_results.append(
                    {
                        "year": int(year),
                        "rider_type": rider,
                        "station_role": role,
                        "rank": rank,
                        "station": station,
                        "trips": trips,
                    }
                )

result = pd.DataFrame(station_results)
print("Top five stations by Q1 trips, year, and rider type:")
print(result.to_string(index=False))


"""
Output (top five station counts):
 year rider_type station_role  rank                      station  trips
 2019     Casual        Start     1      Streeter Dr & Grand Ave   1219
 2019     Casual        Start     2    Lake Shore Dr & Monroe St   1142
 2019     Casual        Start     3               Shedd Aquarium    834
 2019     Casual        Start     4              Millennium Park    627
 2019     Casual        Start     5        Michigan Ave & Oak St    386
 2019     Casual          End     1      Streeter Dr & Grand Ave   1934
 2019     Casual          End     2    Lake Shore Dr & Monroe St    891
 2019     Casual          End     3              Millennium Park    820
 2019     Casual          End     4               Shedd Aquarium    640
 2019     Casual          End     5        Michigan Ave & Oak St    447
 2019     Member        Start     1 Clinton St & Washington Blvd   7611
 2019     Member        Start     2      Clinton St & Madison St   6345
 2019     Member        Start     3          Canal St & Adams St   6213
 2019     Member        Start     4          Canal St & Madison St   4461
 2019     Member        Start     5    Columbus Dr & Randolph St   4416
 2019     Member          End     1 Clinton St & Washington Blvd   7570
 2019     Member          End     2      Clinton St & Madison St   6666
 2019     Member          End     3          Canal St & Adams St   6649
 2019     Member          End     4          Canal St & Madison St   4748
 2019     Member          End     5     Kingsbury St & Kinzie St   4303
 2020     Casual        Start     1                        HQ QR   3766
 2020     Casual        Start     2    Lake Shore Dr & Monroe St   1590
 2020     Casual        Start     3      Streeter Dr & Grand Ave   1530
 2020     Casual        Start     4               Shedd Aquarium    998
 2020     Casual        Start     5              Millennium Park    779
 2020     Casual          End     1                        HQ QR   3764
 2020     Casual          End     2      Streeter Dr & Grand Ave   1856
 2020     Casual          End     3    Lake Shore Dr & Monroe St   1269
 2020     Casual          End     4              Millennium Park   1114
 2020     Casual          End     5               Shedd Aquarium    821
 2020     Member        Start     1          Canal St & Adams St   7586
 2020     Member        Start     2      Clinton St & Madison St   6546
 2020     Member        Start     3 Clinton St & Washington Blvd   5823
 2020     Member        Start     4     Kingsbury St & Kinzie St   4491
 2020     Member        Start     5 Columbus Dr & Randolph St   4099
 2020     Member          End     1          Canal St & Adams St   8158
 2020     Member          End     2 Clinton St & Washington Blvd   7010
 2020     Member          End     3      Clinton St & Madison St   6644
 2020     Member          End     4     Kingsbury St & Kinzie St   4495
 2020     Member          End     5 Michigan Ave & Washington St   3672

Interpretation:
Casual riders' leading stations cluster around Lake Shore Drive, Streeter
Drive, Shedd Aquarium, and Millennium Park in both years. Member leaders
cluster around Clinton and Canal streets. This suggests different popular
areas for the two groups, but station counts alone cannot prove trip purpose.
The 2020 casual results include many trips recorded at HQ QR, so that station
should be interpreted in the context of the source's station coding. Rankings
are kept separate by year because the 2020 source has a different station
schema and its station system may not be directly comparable.
"""
