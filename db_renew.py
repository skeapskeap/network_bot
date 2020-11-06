import pandas as pd
from sqlalchemy import create_engine


def make_df():
    switch_list = pd.read_csv(
        open('../sw_list', 'r'),
        sep=';',
        names=['vendor', 'name', 'ip', 'extra']
        )
    switch_list = switch_list.drop(['extra'], axis=1)
    switch_list.replace(' ', '', regex=True)
    switch_list = switch_list.drop(switch_list.index[0])
    return switch_list


def save_to_db(df):
    engine = create_engine('sqlite:///hosts.db')
    df.to_sql('switch_list', con=engine, index=True, if_exists='replace')


if __name__ == '__main__':
    df = make_df()
    save_to_db(df)
