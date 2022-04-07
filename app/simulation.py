import numpy as np
import pandas as pd
import json
import sys
from .storage_util import StorageUtility
sys.path.append('.')
from config import SimulationConfig
import logging
logging.getLogger().setLevel(logging.INFO)

simulation_grid = []
x_grid_space = SimulationConfig().x_grid_space_rows
y_grid_space = SimulationConfig().y_grid_space_cols

grid_spots = [
    {
        'id': 1,
        'type': 'D',
        'x_cord': 4,
        'y_cord': 8,
        'direction': '*',
        'description': 'default dino 1'
    },
    {
        'id': 2,
        'type': 'D',
        'x_cord': 21,
        'y_cord': 2,
        'direction': '*',
        'description': 'default dino 2'
    },
    {
        'id': 3,
        'type': 'D',
        'x_cord': 13,
        'y_cord': 34,
        'direction': '*',
        'description': 'default dino 3'
    }
]


class RoboVsDino:

    def create_grid(self):
        """This method create an empty grid of size (x_grid_space, y_grid_space) and return grid."""

        for i in range(x_grid_space):
            row = []
            for j in range(y_grid_space):
                row.append('-')
            simulation_grid.append(row)
        return simulation_grid

    def display_grid(self):
        """This method display simulation_grid of size (x_grid_space, y_grid_space) and print in console."""

        for row in simulation_grid:
            for col in row:
                print(col, end='\t')
            print(' ')

    def fix_grid_spot(self, position, player, direction='*'):
        """This function takes position (x, y), player/entity type and direction and reserve place on grid"""

        try:
            if simulation_grid[position[0]][position[1]] == '-':
                simulation_grid[position[0]][position[1]] = (player, direction)
            else:
                print(" ! No spot available for Robot, All grid captured by Dino :/")

        except TypeError as e:
            print(" ! Both values have of coordinaes have to be integers. " + str(e))

        except Exception as e:
            print(e)

    def check_grid_spot_available(self, position, json_file):
        """Check for grid spot availability. If available, return current grid entities else return []."""

        try:
            grid_entities = list(StorageUtility().read_json(json_file))
            if [entity for entity in grid_entities if
                entity['x_cord'] == position[0] and entity['y_cord'] == position[1]]:
                return []
            else:
                return grid_entities

        except TypeError as e:
            print(" ! Both values coordinates have to be integers. " + str(e))

        except Exception as e:
            print(e)

    def create_dino(self, num_of_dino):
        """Create n number of dinosaurs (within 50*50) randomly in simulation grid."""

        if num_of_dino <= sum(row.count('-') for row in simulation_grid):
            count = num_of_dino
            while count != 0:
                try:
                    # randomly chosen coordinates for dinosaurs
                    x_dino = np.random.randint(0, x_grid_space)
                    y_dino = np.random.randint(0, y_grid_space)

                    # fix spot for dinosaur only if spot is available
                    if simulation_grid[x_dino][y_dino] == '-':
                        self.fix_grid_spot((x_dino, y_dino), 'D')
                        count -= 1
                except:
                    print("This name is not registered")
        else:
            print(" ! Dinos not more than grid spots")

    def create_single_robo(self, position, direction):
        """ Creates a single robot at certain position with direction."""

        self.fix_grid_spot(position, 'R', direction)

    def entities_mapping_to_grid(self, grid_spots):
        """ This method takes gird_spots (json objects) and outputs a python dataframe. This dataframe can be later
        easily move to .html (frontend webpage). """

        simulation_grid = self.create_grid()
        try:
            for spot in grid_spots:
                player = spot.get('type', "R")
                x_cord = spot.get('x_cord')
                y_cord = spot.get('y_cord')
                direction = spot.get('direction', "*")
                simulation_grid[x_cord][y_cord] = (player, direction)

            # columns name from 0 to num of x_axis points in grid space
            cords = list(range(0, x_grid_space))
            return pd.DataFrame(simulation_grid, columns=cords)[:y_grid_space]

        except TypeError as e:
            print(" ! Both values of coordinates have to be integers. " + str(e))

        except Exception as e:
            print(e)

    def add_entity(self, id, type, x_cord, y_cord, direction, desc, json_file):
        """This method add entity (robot or dinosaur) to the grid simulation space by take reuqired parameters i.e.
        id, type, x_cord, y_cord, direction, desc, json_file. On success, it writes to the backend json file that
        take record of all entities and simulation status. """

        try:
            grid_space = self.check_grid_spot_available((x_cord, y_cord), json_file)
            if grid_space:
                # direction is not required in case of dinosaurs but required for robots
                if type != 'R':
                    direction = "*"

                grid_space.append({
                    "id": id,
                    "type": type,
                    "x_cord": x_cord,
                    "y_cord": y_cord,
                    "direction": direction,
                    "description": desc
                })
                # saving entity to backend (json file) to preserves
                StorageUtility().write_json(json.dumps(grid_space), json_file)
                return grid_space
            else:
                return False
        except Exception as e:
            print(e)


if __name__ == "__main__":
    RoboVsDino().create_grid()
    RoboVsDino().check_grid_spot_available((2, 4))
    RoboVsDino().fix_grid_spot((2, 4), "R", "Left")
    RoboVsDino().create_single_robo((5, 5), "Up")
    RoboVsDino().create_dino(100)
    RoboVsDino().display_grid()