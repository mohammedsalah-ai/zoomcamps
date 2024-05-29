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
    length = len(df)
    partitions = []
    idx = 0
    while idx <= length:
        partitions.append(df.iloc[idx:idx + 100000])
        idx += 100000

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    container_name = 'zc-container'

    for index, pa in enumerate(partitions):
        blob_path = f'yellow_tripdata_2021-04-{index}.parquet'
        AzureBlobStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
            pa,
            container_name,
            blob_path,
        )