from mage_ai.settings.repo import get_repo_path
from mage_ai.io.azure_blob_storage import AzureBlobStorage
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_azure_blob_storage(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a Azure Blob Storage.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    container_name = 'zoomcamp'

    length = len(df)
    chunk_size = 200000

    chunks = (length // chunk_size) + (length % chunk_size > 0)
    for i in range(chunks):
        start = i * chunk_size
        end = min(length, start + chunk_size)
        partition = df.iloc[start:end]
        blob_path = f'yellow-taxi-2021-{i}.parquet'

        print(f"partition {blob_path}: {start} -> {end}")  
        AzureBlobStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
            partition,
            container_name,
            blob_path,
        )
