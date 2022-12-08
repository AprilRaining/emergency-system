import pandas as pd

from myfunctionlib import *
from options import *


def list_to_sqlite_string(indexList):
    if type(indexList) == list:
        indexList = map(str, indexList)
        return '(' + ','.join(indexList) + ')'
    elif type(indexList) == int:
        return '({})'.format(indexList)


def read_all(table, index):
    with sqlite3.connect('info_files/emergency_system.db') as conn:
        return pd.read_sql_query(f'select * from {table} where {table}ID in {list_to_sqlite_string(index)}', conn)


def pd_read_by_IDs(table, IDs):
    with sqlite3.connect('info_files/emergency_system.db') as conn:
        return pd.read_sql_query(f'select * from {table} where {table}ID in {list_to_sqlite_string(IDs)}', conn)


def get_all_IDs(table):
    with sqlite3.connect('info_files/emergency_system.db') as conn:
        c = conn.cursor()
        result = c.execute(f'select {table}ID from {table}').fetchall()
        IDs = []
        for i in result:
            IDs.append(i[0])
        return IDs


def delete_by_IDs(table, IDs):
    with sqlite3.connect('info_files/emergency_system.db') as conn:
        c = conn.cursor()
        c.execute(
            f'delete from {table} where {table}ID in {list_to_sqlite_string(IDs)}')
        conn.commit()


def display_by_IDs(table, IDs):
    if IDs:
        print(pd_read_by_IDs(table, IDs).to_string(index=False))
    else:
        print('No Result!')


def get_linked_IDs(sonTable, fatherTable, TableIDs):
    with sqlite3.connect('info_files/emergency_system.db') as conn:
        c = conn.cursor()
        result = c.execute(
            f'select {sonTable}ID from {sonTable} where {fatherTable}ID in {list_to_sqlite_string(TableIDs)}')
        sonTableIDs = []
        for i in result:
            sonTableIDs.append(i[0])
        return sonTableIDs


def search_sqlite(table):
    with sqlite3.connect('info_files/emergency_system.db') as conn:
        c = conn.cursor()
        result = c.execute(f'PRAGMA table_info({table})').fetchall()
        columns = []
        for i in range(1, len(result)):
            columns.append(result[i][1])
        options = Options(columns, limited=True)
        print(options)
        option = options.get_option(
            'Please choose which one you want to search by: ')
        keyword = input('Please input the keyword:')
        IDs = search(table, options.values[option], keyword)
        return IDs


def select_sqlite(table):
    IDs = get_all_IDs(table)
    while True:
        display_by_IDs(table, IDs)
        print('Input 0 to search')
        IDs.append(0)
        ID = Get.option_in_list(
            IDs, f'Please input the {table}ID to choose a {table}: ')
        if ID == 0:
            IDs = search_sqlite(table)
        else:
            return ID
