"""
Ingesting NY Taxi data.
"""
import io
import requests
import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    NYTAXI data ingestion.
    """
    # taxi metadata
    taxi_dtypes = {
        'VendorID':str,
        'passenger_count': pd.Int64Dtype(),
        'trip_distance': float,
        'RatecodeID': str,
        'store_and_fwd_flag': str,
        'PULocationID': str,
        'DOLocationID': str,
        'payment_type': str,
        'fare_amount': float,
        'extra': float,
        'mta_tax': float,
        'tip_amount': float,
        'tolls_amount': float,
        'improvement_surcharge': float,
        'total_amount': float,
        'congestion_surcharge': float 
    }
    parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']

    # target url
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'
    df = pd.read_csv(url, sep=",", compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates)

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
