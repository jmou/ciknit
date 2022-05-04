import os
import subprocess

from google.cloud import bigquery


def ref(step, production):
    if 'KNIT' in os.environ:
        command = [os.environ['KNIT'], 'show-output', production, 'out/table']
        return subprocess.check_output(command, cwd='/home/joe/src/fabric',
                                       text=True)
    else:
        return 'STUB'


def creds_file():
    if os.path.exists('session'):
        with open('session') as fh:
            for line in fh:
                if line.startswith('credentials='):
                    return line.split('=', 1)[1].strip()
    return '/home/joe/src/bigquery-module/dbt-tutorial-329716-f95310c71231.json'


def bigquery_table(resource):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds_file()
    client = bigquery.Client()
    attrs = {}
    for line in resource.splitlines():
        key, value = line.split('=', 1)
        attrs[key] = value
    assert attrs['store'] == 'bigquery'
    # TODO should verify tamper
    sql = f'select * from `{attrs["projectid"]}.{attrs["datasetid"]}.{attrs["tableid"]}`'
    return client.query(sql).to_dataframe()


if __name__ == '__main__':
    gestation = ref('gestation', 'a3f9e9dea2fce7a386e1af6736bc8b8e190e8a9e')
    df = bigquery_table(gestation)
