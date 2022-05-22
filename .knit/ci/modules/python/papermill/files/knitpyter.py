import io
import os

import pandas as pd
from google.cloud import bigquery


def _creds_file():
    if os.path.exists('session'):
        with open('session') as fh:
            for line in fh:
                if line.startswith('credentials='):
                    return line.split('=', 1)[1].strip()
    return '/home/joe/src/bigquery-module/dbt-tutorial-329716-f95310c71231.json'


def _resolve(resource, path):
    if resource.startswith('@ref(') and resource.endswith(')'):
        if os.path.isdir('../../in/parameters'):
            step = resource[5:-1]
            with open(f'../../in/parameters/{step}/{path}') as fh:
                return fh.read()
    return resource


def read_csv(resource):
    return pd.read_csv(io.StringIO(_resolve(resource, 'stdout')))


def read_bigquery(resource):
    resource_data = _resolve(resource, 'table')
    attrs = dict(line.split('=', 1) for line in resource_data.splitlines())
    assert attrs['store'] == 'bigquery'
    # TODO should verify tamper
    sql = f'select * from `{attrs["projectid"]}.{attrs["datasetid"]}.{attrs["tableid"]}`'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = _creds_file()
    client = bigquery.Client()
    return client.query(sql).to_dataframe()
