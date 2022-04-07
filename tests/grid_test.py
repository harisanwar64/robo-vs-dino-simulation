import unittest
from app.simulation import RoboVsDino


class TestUser(unittest.TestCase):

    def test_grid_spot_availability(self):
        RoboVsDino().create_grid()
        RoboVsDino().create_single_robo((2, 4), "Up")
        available = RoboVsDino().check_grid_spot_available((2, 4))
        self.assertEqual(len(available), 0)


if __name__ == '__main__':
    unittest.main()