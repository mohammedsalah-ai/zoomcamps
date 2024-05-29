#!/usr/bin/env python3
"""
CLI application to ingest .csv/.csv.gz data into a database.
"""
import os
import click
import time
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy import Integer, String, DateTime, Numeric

@click.command()
@click.option(
    '-u',
    '--username',
    type=str,
    prompt="username",
    help="db server username",
    required=True
)
@click.option(
    '-w',
    '--password',
    type=str,
    prompt="password",
    help="db server user password",
    required=True
)
@click.option(
    '-h',
    '--host',
    type=str,
    prompt="host",
    help="db host",
    required=True
)
@click.option(
    '-p',
    '--port',
    type=int,
    prompt="port",
    help="database port",
    required=True
)
@click.option(
    '-d',
    '--database',
    type=str,
    prompt="database",
    help="database to connect to",
    required=True
)
@click.option(
    '-t',
    '--table',
    type=str,
    prompt="table name",
    help="the name of the table that data will be ingested in",
    required=True
)
@click.option(
    '-l',
    '--url',
    type=str,
    prompt="url",
    help="url of the data to be ingested",
    required=True
)
def main(**kwargs):
    """CLI main functionality"""
    DATABASE_USERNAME = kwargs.get("username")
    DATABASE_PASSWORD = kwargs.get("password")
    DATABASE_HOST = kwargs.get("host")
    DATABASE_PORT = kwargs.get("port")
    DATABASE_NAME = kwargs.get("database")
    df_schema = {
     'tpep_pickup_datetime': DateTime,
     'tpep_dropoff_datetime': DateTime,
    }

    filename = kwargs.get('url').split("/")[-1]
    
    click.echo(click.style(f"Downloading {filename}...", fg="green"))
    os.system(f"wget {kwargs.get('url')} -O data/{filename}")

    connection_string = f"postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    click.echo(click.style(f"Connecting to the database...", fg="green"))
    engine = create_engine(connection_string)
    df_iter = pd.read_csv(f"data/{filename}", iterator=True, chunksize=100000)
    click.echo(click.style(f"Ingesting downloaded data...", fg="green"))
    for index, chunk in enumerate(df_iter):
        tik = time.time()
        chunk.to_sql(name=kwargs.get("table"), con=engine, if_exists='append', dtype=df_schema)
        tok = time.time()
        click.echo(click.style(f"chunk {index + 1} took {tok - tik} seconds", fg="black"))
    click.echo(click.style(f"Finished!", fg="green"))

if __name__ == "__main__":
    main()

