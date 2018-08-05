import os
import json
import unittest
from src.db import start_db, select_and_return, remove_duplicates, update_table
from src.handler import create_insert_query

class UserTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_insert_and_select(self):
        conn, cur = start_db(os.environ['DATABASE_NAME'])
        dict = {"logic": 123,
                "serial": 'abc',
                "model": 'MODEL',
                "sam": 1,
                "ptid": 'PTIDABCD',
                "plat": 2,
                "version": 'v1',
                "mxr": 3,
                "mxf": 4,
                "VERFM": 'last information'
                }
        json_dict = json.dumps(dict)
        insert_query = create_insert_query(json_dict)
        cur.execute(insert_query)
        conn.commit()
        remove_duplicates(conn) # in case there is an old duplicate
        # retrieve data
        table_rows = select_and_return(conn, 'v1', 123)
        expected = [('123', 'abc', 'MODEL', 1, 'PTIDABCD', 2, 'v1', 3, 4, 'last information')]

        self.assertEqual(table_rows, expected)


    def test_insert_duplicate_and_remove_duplicates(self):
        # insert data twice in database
        conn, cur = start_db(os.environ['DATABASE_NAME'])
        dict = {"logic": 123,
                "serial": 'abc',
                "model": 'MODEL',
                "sam": 1,
                "ptid": 'PTIDABCD',
                "plat": 2,
                "version": 'v1',
                "mxr": 3,
                "mxf": 4,
                "VERFM": 'last information'
                }
        json_dict = json.dumps(dict)
        insert_query = create_insert_query(json_dict)
        cur.execute(insert_query)
        conn.commit()
        # remove duplicates
        remove_duplicates(conn) # to remove duplicate from test before
        table_rows = select_and_return(conn, 'v1', 123)
        expected = [('123', 'abc', 'MODEL', 1, 'PTIDABCD', 2, 'v1', 3, 4, 'last information')]
        self.assertEqual(table_rows, expected)

    def test_update_table(self):
        conn, cur = start_db(os.environ['DATABASE_NAME'])
        old_entry = {"logic": 123,
                    "serial": 'abc',
                    "model": 'MODEL',
                    "sam": 1,
                    "ptid": 'PTIDABCD',
                    "plat": 2,
                    "version": 'v2',
                    "mxr": 3,
                    "mxf": 4,
                    "VERFM": 'first information'
                    }
        json_dict = json.dumps(old_entry)
        insert_query = create_insert_query(json_dict)
        cur.execute(insert_query)
        conn.commit()
        new_entry = {"logic": 123,
                    "serial": 'abc',
                    "model": 'MODEL',
                    "sam": 1,
                    "ptid": 'PTIDABCD',
                    "plat": 2,
                    "version": 'v2',
                    "mxr": 3,
                    "mxf": 4,
                    "VERFM": 'new information'
                    }
        update_table(conn, 'v2', 123, new_entry)
        remove_duplicates(conn)
        table_rows = select_and_return(conn, 'v2', 123)
        expected = [('123', 'abc', 'MODEL', 1, 'PTIDABCD', 2, 'v2', 3, 4, 'new information')]
        self.assertEqual(table_rows, expected)



    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
