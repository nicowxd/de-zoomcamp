import pandas as pd
from sqlalchemy import create_engine 

zones_dtype = {
    "LocationID": "Int64",
    "Borough": "string",
    "Zone": "string",
    "service_zone": "string"
}

def insert_trips(URL, PG_HOST, PG_USER, PG_PASS, PG_PORT, PG_DB, TARGET_TABLE):

    print("Inserting green taxi trips...")
    df_trips = pd.read_parquet('data/green_tripdata_2025-11.parquet')

    POSTGRES_URL=f"postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

    engine = create_engine(f"{POSTGRES_URL}")

    df_trips.to_sql(name=TARGET_TABLE, con=engine, if_exists='replace')

    print("Inserted all the green taxi trips succesfully!")

def insert_zones(URL, PG_HOST, PG_USER, PG_PASS, PG_PORT, PG_DB, TARGET_TABLE):

    print("Inserting zones...")
    df_zones = pd.read_csv(URL, dtype=zones_dtype)

    POSTGRES_URL=f"postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"

    engine = create_engine(f"{POSTGRES_URL}")

    df_zones.to_sql(name=TARGET_TABLE, con=engine, if_exists="replace")

    print("Inserted all the zones succesfully!")

if __name__ == "__main__":

    insert_trips(
        URL="data/green_tripdata_2025-11.parquet"
        PG_HOST="localhost"
        PG_USER="postgres"
        PG_PASS="postgres"
        PG_PORT="5433"
        PG_DB="ny_taxi"
        TARGET_TABLE="green_taxi_data"
    )

    insert_zones(
        URL="data/taxi_zone_lookup.csv",
        PG_HOST="localhost"
        PG_USER="postgres"
        PG_PASS="postgres"
        PG_PORT="5433"
        PG_DB="ny_taxi"
        TARGET_TABLE="taxi_zone_lookup"
    )