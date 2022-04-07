import unittest
from app.simulation import RoboVsDino


class TestUser(unittest.TestCase):

    def test_grid_spot_availability(self):
        # RoboVsDino().create_grid()
        # RoboVsDino().create_single_robo((2, 4), "Up")
        available = RoboVsDino().check_grid_spot_available((2, 4), 'app/simulation_data/robo_vs_dino.json')
        self.assertNotEqual(len(available), 0)


if __name__ == '__main__':
    # todo: more test cases can be written for cases like 'is dinosaur actually killed after attack', 'direction updates
    #  successfully or not', 'only robot kill dinosaur' etc.
    unittest.main()