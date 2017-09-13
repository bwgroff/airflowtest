import pandas as pd
from airflow.hooks.mysql_hook import MySqlHook


def sqrt_transform(table, column, tmp_file):
    mysql = MySqlHook(mysql_conn_id='og')
    df = mysql.get_pandas_df('SELECT * FROM {}'.format(table))

    df[column + '_root'] = df[column] ** 0.5
    del df[column]
    df = df.fillna(0)

    df.to_csv(tmp_file)
    return 0
