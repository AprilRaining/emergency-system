import sqlite3

import pandas as pd


def list_to_sqlite_string(indexList):
    if type(indexList) == list:
        indexList = map(str, indexList)
        return '(' + ','.join(indexList) + ')'
    elif type(indexList) == int:
        return '({})'.format(indexList)


def read_all(table, index):
    with sqlite3.connect('../info_files/emergency_system.db') as conn:
        return pd.read_sql_query(f'select * from {table} where {table}ID in {list_to_sqlite_string(index)}', conn)


def pd_read_by_IDs(table, IDs):
    with sqlite3.connect('../info_files/emergency_system.db') as conn:
        return pd.read_sql_query(f'select * from {table} where {table}ID in {list_to_sqlite_string(IDs)}', conn)


def get_all_IDs(table):
    with sqlite3.connect('../info_files/emergency_system.db') as conn:
        c = conn.cursor()
        result = c.execute(f'select {table}ID from plan').fetchall()
        IDs = []
        for i in result:
            IDs.append(i[0])
        return IDs


def delete_by_IDs(table, IDs):
    with sqlite3.connect('../info_files/emergency_system.db') as conn:
        c = conn.cursor()
        c.execute(
            f'delete from {table} where {table}ID in {list_to_sqlite_string(IDs)}')


def display_by_IDs(table, IDs):
    if IDs:
        print(pd_read_by_IDs(table, IDs).to_string(index=False))
    else:
        print('No Result!')


def get_linked_IDs(sonTable, fatherTable, TableIDs):
    with sqlite3.connect('../info_files/emergency_system.db') as conn:
        c = conn.cursor()
        result = c.execute(
            f'select {sonTable}ID from {sonTable} where {fatherTable}ID in {list_to_sqlite_string(TableIDs)}')
        sonTableIDs = []
        for i in result:
            sonTableIDs.append(i[0])
        return sonTableIDs
