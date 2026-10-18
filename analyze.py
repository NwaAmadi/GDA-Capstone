import pandas as pd


trip_data = pd.read_csv("Divvy_Trips_2019_2020_Q1_cleaned.csv", low_memory=False)
core_columns = ["trip_id", "starttime", "stoptime", "usertype", "tripduration"]

print(f"Combined Q1 trips: {len(trip_data):,}")
for year, year_data in trip_data.groupby("source_year"):
    missing_rows = year_data[core_columns].isna().any(axis=1)
    print(
        f"{year} Q1 rows missing at least one core field: "
        f"{missing_rows.sum():,} ({missing_rows.mean() * 100:.2f}%)"
    )
    print("Missing core fields:")
    print(year_data[core_columns].isna().sum())
