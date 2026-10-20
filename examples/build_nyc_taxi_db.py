# /// script
# requires-python = ">=3.11"
# dependencies = ["duckdb"]
# ///
"""Builds examples/nyc_taxi.db, the SQLite database nyc_taxi.ipynb queries.

    uv run examples/build_nyc_taxi_db.py

It downloads every yellow taxi trip in New York in January 2024 from the Taxi and Limousine
Commission (a Parquet file of about 50 MB) and its list of taxi zones, and writes them to SQLite:
about 3 million trips, about 475 MB. It takes a few minutes, most of them downloading. The
database is not in git: it is too large, and the city publishes the data.

DuckDB reads the Parquet file. `uv run` installs it for this script alone, so the project's own
environment is left as it is.
"""

import argparse
import csv
import io
import sqlite3
import tempfile
import urllib.request
from pathlib import Path

import duckdb

TLC = "https://d37ci6vzurychx.cloudfront.net"
TRIPS = f"{TLC}/trip-data/yellow_tripdata_2024-01.parquet"
ZONES = f"{TLC}/misc/taxi_zone_lookup.csv"

SCHEMA = """
CREATE TABLE zones (location_id INTEGER PRIMARY KEY, borough TEXT, zone TEXT, service_zone TEXT);
CREATE TABLE trips (
  vendor_id INTEGER, pickup_at TEXT, dropoff_at TEXT, passenger_count INTEGER, trip_distance REAL,
  rate_code_id INTEGER, store_and_fwd_flag TEXT, pickup_location_id INTEGER, dropoff_location_id INTEGER,
  payment_type INTEGER, fare_amount REAL, extra REAL, mta_tax REAL, tip_amount REAL, tolls_amount REAL,
  improvement_surcharge REAL, total_amount REAL, congestion_surcharge REAL, airport_fee REAL);
CREATE TABLE payment_types (payment_type INTEGER PRIMARY KEY, name TEXT);
INSERT INTO payment_types VALUES (0, 'Flex fare'), (1, 'Credit card'), (2, 'Cash'), (3, 'No charge'),
  (4, 'Dispute'), (5, 'Unknown'), (6, 'Voided trip');
"""

# The file has a few trips stamped outside January; only January's are kept, in pickup order.
SELECT = """
SELECT VendorID, strftime(tpep_pickup_datetime, '%Y-%m-%d %H:%M:%S'),
       strftime(tpep_dropoff_datetime, '%Y-%m-%d %H:%M:%S'), passenger_count, trip_distance,
       RatecodeID, store_and_fwd_flag, PULocationID, DOLocationID, payment_type, fare_amount, extra,
       mta_tax, tip_amount, tolls_amount, improvement_surcharge, total_amount, congestion_surcharge,
       Airport_fee
FROM read_parquet(?)
WHERE tpep_pickup_datetime >= '2024-01-01' AND tpep_pickup_datetime < '2024-02-01'
ORDER BY tpep_pickup_datetime
"""

INDEXES = """
CREATE INDEX trips_pickup_at ON trips (pickup_at);
CREATE INDEX trips_pickup_location ON trips (pickup_location_id);
CREATE INDEX trips_dropoff_location ON trips (dropoff_location_id);
"""


def build(out: Path) -> None:
    partial = out.with_suffix(".db.partial")
    partial.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as scratch:
        parquet = Path(scratch) / "yellow_tripdata_2024-01.parquet"
        print("downloading the trips (about 50 MB)", flush=True)
        urllib.request.urlretrieve(TRIPS, parquet)
        with urllib.request.urlopen(ZONES) as response:
            zones = list(csv.reader(io.TextIOWrapper(response, encoding="utf-8")))[1:]

        db = sqlite3.connect(partial)
        db.executescript(SCHEMA)
        db.executemany("INSERT INTO zones VALUES (?, ?, ?, ?)", zones)
        trips = duckdb.execute(SELECT, [str(parquet)])
        written = 0
        while batch := trips.fetchmany(200_000):
            db.executemany(f"INSERT INTO trips VALUES ({', '.join('?' * 19)})", batch)
            written += len(batch)
            print(f"  {written:,} trips", flush=True)
        print("indexing", flush=True)
        db.executescript(INDEXES)
        db.commit()
        db.close()
    # Renamed only when complete, so a build that stops halfway never leaves a database that looks whole.
    partial.replace(out)
    print(f"wrote {out}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "nyc_taxi.db")
    parser.add_argument("--force", action="store_true", help="build again even if the database exists")
    args = parser.parse_args()
    if args.out.exists() and not args.force:
        print(f"{args.out} already exists; --force builds it again")
        return
    build(args.out)


if __name__ == "__main__":
    main()
