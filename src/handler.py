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

# Requests besides POST will be blocked
@app.route('/textHtml', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True, port=5000) # run app in debug mode on port 5000
