import sqlite3
import asyncio

def adduser(id : str, db_name : str, table_name : str):
    sqlite_connection = sqlite3.connect(db_name)
    cursor = sqlite_connection.cursor()
    insert_comm = '''INSERT OR IGNORE INTO {} (id)
                    VALUES ({});
                    '''.format(table_name, id)
    cursor.execute(insert_comm)
    sqlite_connection.commit()
    cursor.close()

def adduserinfo(id : str, val : str, val_name : str, db_name : str, table_name : str):
    sqlite_connection = sqlite3.connect(db_name)
    cursor = sqlite_connection.cursor()
    insert_comm = '''UPDATE {}
                    SET {} = {}
                    WHERE id = {};
                    '''.format(table_name, val_name,"'" + val + "'", id)
    print(insert_comm)
    cursor.execute(insert_comm)
    sqlite_connection.commit()
    cursor.close()


def getdate(id : str, db_name : str, table_name : str):
    sqlite_connection = sqlite3.connect(db_name)
    cursor = sqlite_connection.cursor()
    insert_comm = '''SELECT birth_day, birth_month
                    FROM {}
                    WHERE id = '{}';
                    '''.format(table_name, id)
    cursor.execute(insert_comm)
    output = cursor.fetchall()
    cursor.close()
    return output[0]

def getsign(id : str, db_name : str, table_name : str):
    sqlite_connection = sqlite3.connect(db_name)
    cursor = sqlite_connection.cursor()
    insert_comm = '''SELECT sign
                    FROM {}
                    WHERE id = '{}';
                    '''.format(table_name, id)
    cursor.execute(insert_comm)
    output = cursor.fetchall()
    cursor.close()
    return output[0][0]