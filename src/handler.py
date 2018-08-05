import os
import json
import sqlite3
# import main Flask class and request object
from flask import Flask, request
from jsonschema import validate
from sqlite3 import Error
from src.db import start_db, create_connection, select_and_return, update_table, remove_duplicates, create_insert_query

app = Flask(__name__)  # create the Flask app

database_name = os.environ.get('DATABASE_NAME', 'test.db')


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

    #if data does not contains all items it will be refused later
    if len(data) != 10:
        json_output = json.dumps(string_parsed)
        return json_output

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
    dict = {"logic": data[0],
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
        dict_output[counter] = {"logic": data[0],
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
    schema = {"title": "Terminal",
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


@app.route('/', methods=['POST'])
def main_method_post():
    conn, c = create_connection(database_name)
    if block_json_post():
        return "Cant handle application/json POST"

    string_parsed = retrieve_body_data()
    json_output = format_body_data_to_json(string_parsed)
    json_validation = validate_json_with_schema(json_output)

    if json_validation is True:
        insert_query = create_insert_query(json_output)
        c.execute(insert_query)  # executes insert query
        conn.commit()         # store in db
        return json_output
    else:
        return "Invalid Output"


@app.route('/<version>/<entity>/<int:logic>', methods=['GET'])
def main_method_get(version, entity, logic):
    database = entity
    conn, c = create_connection(database)
    remove_duplicates(conn)

    with conn:
            table_rows = select_and_return(conn, version, logic)
            return format_list_of_lists_to_json(table_rows)


@app.route('/<version>/<entity>/<int:logic>', methods=['PUT'])
def main_method_put(version, entity, logic):
    database = entity
    conn, c = create_connection(database)
    with conn:
        # have to verify if it is Json to do this
        body_json = retrieve_body_data()
        body_dict = json.loads(body_json[0])

        update_table(conn, version, logic, body_dict)
        return "Request OK"


if __name__ == '__main__':
    start_db(database_name)
    # run app in debug mode on port 8000 with gunicorn
    app.run()
