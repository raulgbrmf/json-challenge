import os
import json
import requests
import unittest
import handler
from db import start_db
from handler import app
from unittest.mock import patch

class UserTest(unittest.TestCase):
    def setUp(self):
        with patch.dict('os.environ', {'DATABASE_NAME': 'mock.db'}):
            self.app = app.test_client() # app'mock
            start_db(os.environ['DATABASE_NAME'])


    def test_post_block_json(self):
        dict = {"test": 123}
        json_input = json.dumps(dict)
        response = self.app.post('/',
                                data=json_input,
                                headers={"content-type": "application/json"})
        self.assertEqual("Cant handle application/json POST", response.get_data().decode("utf-8"))

    def test_post_invalid_output(self):
        dict = 123
        json_input = json.dumps(dict)
        response = self.app.post('/',
                                data=json_input,
                                headers={"content-type": "text/html"})
        self.assertEqual("Invalid Output", response.get_data().decode("utf-8"))

    def test_post_returns_json_output(self):
        with patch.dict('os.environ', {'DATABASE_NAME': 'mock.db'}):
            input = "1234;abc;QWE;0;F12A;4;8.00b;0;09876;something"
            output = {"logic": 1234, "serial": "abc", "model": "QWE", "sam": 0,
                    "ptid": "F12A", "plat": 4, "version": "8.00b", "mxr": 0,
                    "mxf": 9876, "VERFM": "something"}
            response = self.app.post('/',
                                    data=input,
                                    headers={"content-type": "text/html"})
            dict_response = json.loads(response.get_data().decode("utf-8"))
            self.assertEqual(output, dict_response)

    def test_get_after_post(self):
        input = "1234;abc;QWE;0;F12A;4;version1;0;09876;something"
        response = self.app.post('/',
                                 data=input,
                                 headers={"content-type": "text/html"})
        response = self.app.get('/version1/test.db/1234')
        dict_output = json.loads(response.get_data().decode("utf-8"))
        dict_expected = {"0":{"logic": "1234", "serial": "abc", "model": "QWE",
                        "sam": 0, "ptid": "F12A", "plat": 4, "version": "version1",
                        "mxr": 0, "mxf": 9876, "VERFM": "something"}}

        self.assertEqual(dict_expected, dict_output)

    def test_put_after_post(self):
        input = "5678;abc;QWE;0;F12A;4;version2;0;09876;something"
        response_post = self.app.post('/',
                                 data=input,
                                 headers={"content-type": "text/html"})

        put_dict = {"logic": "5678", "serial": "abc", "model": "QWE",
                    "sam": 0, "ptid": "F12A", "plat": 4, "version": "version2",
                    "mxr": 0, "mxf": 9876, "VERFM": "something"}
        json_input = json.dumps(put_dict)
        response_put = self.app.put('/version2/test.db/5678',
                                data=json_input,
                                headers={"content-type": "application/json"})

        self.assertEqual("Request OK", response_put.get_data().decode("utf-8"))


    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
