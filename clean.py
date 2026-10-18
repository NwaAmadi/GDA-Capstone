from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).parent
SOURCE_FILES = [
    (2019, DATA_DIR / "Datasets" / "Divvy_Trips_2019_Q1.csv"),
    (2020, DATA_DIR / "Datasets" / "Divvy_Trips_2020_Q1.csv"),
]
OUTPUT_FILE = DATA_DIR / "Divvy_Trips_2019_2020_Q1_cleaned.csv"


def load_source(year, path):
    data = pd.read_csv(path, low_memory=False)
    if year == 2019:
        data = data.rename(columns={"start_time": "starttime", "end_time": "stoptime"})
        data["usertype"] = data["usertype"].replace(
            {"Subscriber": "Member", "Customer": "Casual"}
        )
        data["trip_id"] = data["trip_id"].astype("string")
    else:
        data = data.rename(
            columns={
                "ride_id": "trip_id",
                "started_at": "starttime",
                "ended_at": "stoptime",
                "member_casual": "usertype",
            }
        )
        data["usertype"] = data["usertype"].replace(
            {"member": "Member", "casual": "Casual"}
        )
        data["trip_id"] = data["trip_id"].astype("string")
        # The 2020 export has timestamps but no tripduration column.
        start = pd.to_datetime(data["starttime"], errors="coerce")
        stop = pd.to_datetime(data["stoptime"], errors="coerce")
        data["tripduration"] = (stop - start).dt.total_seconds()
        data["gender"] = pd.NA
        data["birthyear"] = pd.NA

    data["source_year"] = year
    data["starttime"] = pd.to_datetime(data["starttime"], errors="coerce")
    data["stoptime"] = pd.to_datetime(data["stoptime"], errors="coerce")
    data["tripduration"] = pd.to_numeric(data["tripduration"], errors="coerce")
    for column in ("usertype", "gender", "from_station_name", "to_station_name"):
        if column in data:
            data[column] = data[column].astype("string").str.strip()
    return data


trip_data = pd.concat(
    [load_source(year, path) for year, path in SOURCE_FILES],
    ignore_index=True,
    sort=False,
)

print("Rows by source year:")
print(trip_data.groupby("source_year").size())
print("Duplicate rows:", trip_data.duplicated().sum())
print("Repeated trip IDs:", trip_data["trip_id"].duplicated().sum())

trip_data = trip_data.drop_duplicates().copy()
missing_times = trip_data[["starttime", "stoptime"]].isna().any(axis=1)
invalid_times = trip_data["stoptime"] <= trip_data["starttime"]
invalid_duration = trip_data["tripduration"] <= 0
over_24_hours = trip_data["tripduration"] > 24 * 60 * 60
print("Rows with missing timestamps:", missing_times.sum())
print("End time before or equal to start:", invalid_times.sum())
print("Zero or negative duration:", invalid_duration.sum())
print("Durations over 24 hours:", over_24_hours.sum())
print("Missing values by column:")
print(trip_data.isna().sum())
print("Earliest trip:", trip_data["starttime"].min())
print("Latest trip:", trip_data["starttime"].max())
print("Duration summary in seconds:")
print(trip_data["tripduration"].describe(percentiles=[0.5, 0.95, 0.99]))

trip_data.to_csv(OUTPUT_FILE, index=False)
print(f"Saved {len(trip_data):,} rows to {OUTPUT_FILE.name}")
