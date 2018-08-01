# To run in you browser
# http://127.0.0.1:5000/post (or localhost:5000/post)

import json
import sqlite3
from flask import Flask, request # import main Flask class and request object
from jsonschema import validate
from sqlite3 import Error


app = Flask(__name__) #create the Flask app

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
    try:
        conn = sqlite3.connect(db_file)
        return conn
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
    cur.execute("SELECT * FROM entries WHERE version=? AND logic=?", (version_value, logic_value,))

    rows = cur.fetchall()

    return rows

def remove_duplicates(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM entries WHERE rowid NOT IN ( SELECT MIN(rowid) FROM entries GROUP BY version, logic)")

def create_insert_query(json_output):
    json_dict = json.loads(json_output) # tentar colocar tudo numa lista
    keys = [val for val in json_dict.keys()]
    values = [val for val in json_dict.values()]
    concat = keys + values
    insert_query = """insert into entries ({0}, {1}, {2}, {3},
                    {4}, {5}, {6}, {7}, {8}, {9}) Values ({10},
                    '{11}' ,'{12}', {13}, '{14}', {15}, '{16}',
                    {17}, {18}, '{19}');""".format(*concat)
    return insert_query

# FlASK METHODS
def block_json_post():
    if request.is_json:
        return True
    else:
        return False

def retrieve_body_data():
    req_bytes = request.get_data()
    req_data = req_bytes.decode(encoding='UTF-8')
    string_parsed = req_data.split(";")
    return string_parsed

def format_body_data_to_json(string_parsed):
    data = string_parsed
    # try block to try to convert the string into int values
    try:
        data[0] = int(data[0])
    except:
        pass
    try:
        data[3] = int(data[3])
    except:
        pass
    try:
        data[5] = int(data[5])
    except:
        pass
    try:
        data[7] = int(data[7])
    except:
        pass
    try:
        data[8] = int(data[8])
    except:
        pass
    dict = { "logic": data[0],
             "serial": data[1],
             "model": data[2],
             "sam": data[3],
             "ptid": data[4],
             "plat": data[5],
             "version": data[6],
             "mxr": data[7],
             "mxf": data[8],
             "VERFM": data[9]
             }
    json_output = json.dumps(dict)
    return json_output

def format_list_of_lists_to_json(db_output):
    dict_output = {}
    counter = 0
    for data in db_output:
        dict_output[counter] = { "logic": data[0], # have to look here how to put one dict after another
                         "serial": data[1],
                         "model": data[2],
                         "sam": data[3],
                         "ptid": data[4],
                         "plat": data[5],
                         "version": data[6],
                         "mxr": data[7],
                         "mxf": data[8],
                         "VERFM": data[9]
                         }
        counter += 1
    json_output = json.dumps(dict_output)
    return json_output

def validate_json_with_schema(json_output):
    schema = { "title": "Terminal",
                "type": "object",
                "properties": {
                        "logic": {
                                    "type": "integer"
                        },
                        "serial": {
                                    "type": "string"
                        },
                        "sam": {
                                "type": "integer",
                                "minimum": 0
                        },
                        "ptid": {
                                "type": "string"
                        },
                        "plat": {
                                "type": "integer"
                        },
                        "version": {
                                    "type": "string"
                        },
                        "mxr": {
                                "type": "integer"
                        },
                        "VERFM": {
                                "type": "string"
                        }
                },
                "required": ["logic", "serial", "model", "version"]
            }
    try:
        validate(json.loads(json_output), schema)
        return True
    except:
        return False

# DELETE requests will be blocked
@app.route('/post', methods=['POST'])
def main_method_post():

    db_path = 'test.db'
    conn, c = start_db(db_path)

    if block_json_post():
        return "Cant handle application/json POST"

    string_parsed = retrieve_body_data()
    json_output = format_body_data_to_json(string_parsed)
    json_validation = validate_json_with_schema(json_output)

    if json_validation is True:
        insert_query = create_insert_query(json_output)
        c.execute(insert_query)
        conn.commit()
        return json_output
    else:
        return "Invalid Output"

@app.route('/get', methods=['GET'])
def main_method_get():

    database = 'test.db'
    # create database connection
    conn = create_connection(database)

    remove_duplicates(conn)

    with conn:
        version = request.args.get('version')
        logic = request.args.get('logic')
        if (version and logic) != None: # if key does not exist, returns None
            table_rows = select_and_return(conn, version, logic)
            return format_list_of_lists_to_json(table_rows)
        else:
            return "Invalid request"

if __name__ == '__main__':
    app.run(debug=True, port=5000) # run app in debug mode on port 5000
