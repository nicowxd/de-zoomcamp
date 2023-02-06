from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_data(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""

    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("gcs-block")
    gcs_block.get_directory(from_path=gcs_path)
    
    return Path(gcs_path)

@task(log_prints=True)
def transform_data(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)

    print(f"Number of rows processed: {len(df)}")
    #print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    #df['passenger_count'].fillna(0, inplace=True)
    #print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")

    return df

@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BigQuery"""
    gcp_credentials = GcpCredentials.load("gcp-credentials")

    df.to_gbq(
        destination_table="de_zoomcamp_dataset.rides",
        project_id="de-zoomcamp-376310",
        credentials=gcp_credentials.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )

@flow()
def main_flow(months: list[int] = [2, 3], year: int = 2019, color: str = "yellow") -> None:
    """Main ETL flow to load data into Big Query"""

    for month in months:
        etl_gcs_to_bq(month, year, color)


@flow()
def etl_gcs_to_bq(month: int, year: int, color: str) -> None:
    """Subflow that executes ETL into Big Query"""

    path = extract_data(color, year, month)
    df = transform_data(path)
    write_bq(df)


if __name__ == "__main__":
    months = [2, 3]
    year = 2019
    color = "yellow"
    main_flow(months, year, color)