import os
import json
import sqlite3
# import main Flask class and request object
from flask import Flask, request
from jsonschema import validate
from sqlite3 import Error


# SQLITE METHODS
def start_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS entries (logic text,
    serial integer, model text, sam integer, ptid text, plat integer,
    version string, mxr integer, mxf integer, VERFM text)""")
    return conn, c

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    if not os.path.isfile(db_file):
        return start_db(db_file)
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        return conn, c
    except Error as e:
        print(e)

    return None


def select_and_return(conn, version_value, logic_value):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("""SELECT * FROM entries WHERE version=? AND logic=?""",
                (version_value, logic_value,))

    rows = cur.fetchall()

    return rows


def update_table(conn, version_value, logic_value, body_dict):
    sql = ''' UPDATE entries
              SET serial=?,
              model=?,
              sam=?,
              ptid=?,
              plat=?,
              mxr=?,
              mxf=?,
              VERFM=?
              WHERE version=? AND logic=?'''

    cur = conn.cursor()
    cur.execute(sql, (body_dict["serial"], body_dict["model"], body_dict["sam"],
                      body_dict["ptid"], body_dict["plat"],  body_dict["mxr"], body_dict["mxf"],
                      body_dict["VERFM"], version_value, logic_value))


def remove_duplicates(conn):
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM entries WHERE rowid NOT IN ( SELECT MIN(rowid) FROM entries GROUP BY version,logic )")


def create_insert_query(json_output):
    # tentar colocar tudo numa lista
    json_dict = json.loads(json_output)
    keys = [val for val in json_dict.keys()]
    values = [val for val in json_dict.values()]
    concat = keys + values
    insert_query = """insert into entries ({0}, {1}, {2}, {3},
                    {4}, {5}, {6}, {7}, {8}, {9}) Values ({10},
                    '{11}' ,'{12}', {13}, '{14}', {15}, '{16}',
                    {17}, {18}, '{19}');""".format(*concat)
    return insert_query
