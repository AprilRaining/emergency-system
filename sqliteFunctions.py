from options import *
import pandas as pd
from myfunctionlib import *
from print_table import *


def list_to_sqlite_string(indexList):
    if type(indexList) == list:
        indexList = map(str, indexList)
        return '(' + ','.join(indexList) + ')'
    elif type(indexList) == int:
        return '({})'.format(indexList)


def read_all(table, index):
    with sqlite3.connect('emergency_system.db') as conn:
        return pd.read_sql_query(f'select * from {table} where {table}ID in {list_to_sqlite_string(index)}', conn)


def pd_read_by_IDs(table, IDs):
    with sqlite3.connect('emergency_system.db') as conn:
        return pd.read_sql_query(f'select * from {table} where {table}ID in {list_to_sqlite_string(IDs)}', conn)


def get_all_IDs(table):
    with sqlite3.connect('emergency_system.db') as conn:
        c = conn.cursor()
        result = c.execute(f'select {table}ID from {table}').fetchall()
        IDs = []
        for i in result:
            IDs.append(i[0])
        return IDs


def delete_by_IDs(table, IDs):
    with sqlite3.connect('emergency_system.db') as conn:
        c = conn.cursor()
        c.execute(
            f'delete from {table} where {table}ID in {list_to_sqlite_string(IDs)}')
        conn.commit()


def display_by_IDs(table, IDs):
    if IDs:
        table_df = pd_read_by_IDs(table, IDs)
        col_width = ()
        if table == 'plan':
            col_width = (8, 20, 30, 16, 20, 20, 14, 8)
        elif table == 'volunteer':
            col_width = (18, 25, 25, 25, 25, 20, 16, 20,
                         30, 30, 30, 30, 30, 30, 30, 200)
        elif table == 'refugee':
            col_width = (18, 16, 25, 25, 30, 25, 32, 70,
                         60, 70, 70, 60, 30, 30, 30, 25)
        print("\n")
        print_table(table_df.columns, table_df.to_numpy().tolist(), col_width)
    else:
        warn('\nNo Result!')


def get_linked_IDs(subTable, superTable, TableIDs):
    with sqlite3.connect('emergency_system.db') as conn:
        c = conn.cursor()
        result = c.execute(
            f'select {subTable}ID from {subTable} where {superTable}ID in {list_to_sqlite_string(TableIDs)}')
        sonTableIDs = []
        for i in result:
            sonTableIDs.append(i[0])
        return sonTableIDs


def search_sqlite(table):
    with sqlite3.connect('emergency_system.db') as conn:
        c = conn.cursor()
        result = c.execute(f'PRAGMA table_info({table})').fetchall()
        columns = []
        for i in range(1, len(result)):
            columns.append(result[i][1])
        options = Options(columns, limited=True)
        print(options)
        option = options.get_option(
            u"\U0001F539" + 'Please choose which one you want to search by: ')
        keyword = input("\n"+u"\U0001F531"+'Please input the search keyword: ')
        print("\n")
        IDs = search(table, options.values[option], keyword)
        return IDs
