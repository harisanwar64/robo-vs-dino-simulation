import unittest
from run import app


class FlaskTest(unittest.TestCase):

    def test_webapp_home(self):
        """" Status code test case for home page at: http://<domain url>/webapp/. If successful, response should match
        200."""

        tester = app.test_client(self)
        response = tester.get("/webapp/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)


if __name__ == '__main__':
    unittest.main()