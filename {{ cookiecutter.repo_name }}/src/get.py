"""get.py A CLI for getting data from Kusto via Azure Blob Storage"""
import os
import time
import logging
import click
import dotenv
import pandas as pd
import jinja2 as jj
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import (
    KustoAuthenticationError,
    KustoClientError,
)
from azure.kusto.data.helpers import dataframe_from_result_table
from azure.storage.blob import BlobClient
from typing import List

def get_kusto_client(server: str, database: str) -> KustoClient:
    """
    Helper to get an authenticated KustoClient.
    Try to use Az CLI cached credentials, fall back to device code auth.
    :param server: The (short) name of a Kusto server cluster, not the full URI
    :param database: The name of the initial catalog to connect to
    """
    logger = logging.getLogger(__name__)
    server_uri = f"https://{server}.kusto.windows.net"
    try:
        kcsb = KustoConnectionStringBuilder.with_az_cli_authentication(server_uri)
        client = KustoClient(kcsb)
        # hit the server to force authentication
        client.execute_query(database, "print('hi')")
        return client
    except KustoAuthenticationError:
        kcsb = KustoConnectionStringBuilder.with_aad_device_authentication(server_uri)
        client = KustoClient(kcsb)
        client.execute_query(database, "print('hi')")
        return client

def render_export_template(query, storage_uri, key, name_prefix, gzip):
    """
    Render the export template query.
    :param query: The Kusto (KQL) query to to execute
    :param storage_uri: The Azure Storage URI to export results to
    :param name_prefix: The exported data filename prefix
    :param gzip: Whether to compress the data file or not
    """
    template = jj.Template("""{% raw %}
.export
{% if gzip -%}
compressed
{% endif -%}
to csv (h@"{{ storage_uri }};{{ key }}")
with (
    sizeLimit=1073741824,
    namePrefix={{ name_prefix }},
    fileExtension=csv,
    {% if gzip -%}
    compressionType=gzip,
    {% endif -%}
    includeHeaders=firstFile,
    encoding=UTF8NoBOM,
    distributed=false
)
<|
{{ query }}
{% endraw %}""")

    result = template.render(
        storage_uri=storage_uri,
        key=key,
        query=query,
        gzip=gzip,
        name_prefix=name_prefix,
    )
    return result

def get_blob(storage_uri, key, file_path):
    """
    Download files from Azure Blob Storage to local file path
    :param storage_uri: The Azure Storage URI of the file to download
    :param file_path: The local file path to download to
    """
    blob = BlobClient.from_blob_url(storage_uri, credential=key)
    blob_data = blob.download_blob()
    file_dir = os.path.dirname(os.path.abspath(file_path))
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_path, "wb") as fd:
        blob_data.readinto(fd)

@click.command()
@click.argument("cluster", type=click.STRING)
@click.argument("database", type=click.STRING)
@click.argument("query_path", type=click.Path(exists=True))
@click.argument("account", type=click.STRING)
@click.argument("container", type=click.STRING)
@click.argument("key", type=click.STRING)
@click.argument("folder", type=click.STRING)
@click.argument("prefix", type=click.STRING)
@click.argument("dest", type=click.Path())
@click.option("--gzip/--no-gzip", default=False, help="Compress the file with gzip")
def export(cluster, database, query_path, account, container, key, folder, prefix, dest, gzip):
    """
    Run QUERY_PATH on CLUSTER/DATABASE, export to blob ACCOUNT/CONTAINER/FOLDER
    and download to local file DEST.
    """
    logger = logging.getLogger(__name__)

    with open(query_path, "r") as query_file:
        query = query_file.read()

    storage_uri = f"https://{account}.blob.core.windows.net/{container}/{folder}"
    command = render_export_template(query, storage_uri, key, prefix, gzip)

    client = get_kusto_client(cluster, database)
    logger.info("Exporting query %s to %s...", query_path, storage_uri)

    try:
        res = client.execute_mgmt(database, command)

        data = dataframe_from_result_table(res.primary_results[0])
        storage_path = data["Path"].values[0]
        logger.info("Successfully exported query %s to %s", query_path, storage_path)

        logger.info("Downloading file from %s to %s", storage_path, dest)
        get_blob(storage_path, key, dest)
        logger.info("Finished downloading file from %s to %s", storage_path, dest)
        
    except KustoClientError as e:
        logger.error("KustoClientError", exc_info=True)


def main():
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    dotenv.load_dotenv(dotenv.find_dotenv())
    export()


if __name__ == "__main__":
    main()
