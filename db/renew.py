import pandas as pd
import subprocess as sp
from db import engine
from utils import logger


def make_df():
    switch_list = pd.read_csv(
        open('sw_list.csv', 'r'),
        sep=';',
        names=['vendor', 'name', 'ip', 'extra']
        )
    switch_list = switch_list.drop(['extra'], axis=1)
    switch_list.replace(' ', '', regex=True)
    switch_list = switch_list.drop(switch_list.index[0])
    return switch_list


def save_to_db(df):
    df.to_sql('switch_list', con=engine, index=True, if_exists='replace')


def renew_db():
    new_sw_list = sp.Popen(['sh', 'get_switch_list.sh'])
    try:
        new_sw_list.wait(timeout=30)
        df = make_df()
        save_to_db(df)
        logger.info('renew switch db success')
    except sp.TimeoutExpired:
        new_sw_list.kill()
        logger.info('renew switch db failed')


if __name__ == '__main__':
    renew_db()
