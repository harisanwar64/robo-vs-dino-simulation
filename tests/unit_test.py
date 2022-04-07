import unittest
from run import app
import json


class FlaskTest(unittest.TestCase):

    def test_webapp_home(self):
        """" Status code test case for home page at: http://<domain url>/webapp/. If successful, response should match
        200."""

        tester = app.test_client(self)
        response = tester.get("/webapp/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_create_entity(self):
        tester = app.test_client(self)
        test_payload = {
            "description": "unit test desc",
            "direction": "Left",
            "id": "xyz",
            "type": "R",
            "x_cord": 45,
            "y_cord": 21
        }
        response = tester.post("webapp/create_entity", data=json.dumps(test_payload),
                               headers={'Content-Type': 'application/json'})
        statuscode = response.status_code
        self.assertEqual(
            200,
            statuscode
        )


if __name__ == '__main__':
    # todo: more test cases can be written for 'issue instructiion to robot' etc.
    unittest.main()