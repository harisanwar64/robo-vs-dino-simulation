import numpy as np

simulation_grid = []
x_grid_space = 50
y_grid_space = 50

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

    def check_grid_spot_available(self, position):
        """Check for grid spot availability. If available, return current grid entities else return []."""

        try:
            grid_entities = grid_spots
            if [entity for entity in grid_entities if entity['x_cord'] == position[0] and entity['y_cord'] == position[1]]:
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
                    x_dino = np.random.randint(0, x_grid_space)
                    y_dino = np.random.randint(0, y_grid_space)
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


if __name__ == "__main__":
    RoboVsDino().create_grid()
    RoboVsDino().check_grid_spot_available((2, 4))
    RoboVsDino().fix_grid_spot((2, 4), "R", "Left")
    RoboVsDino().create_single_robo((5, 5), "Up")
    RoboVsDino().create_dino(100)
    RoboVsDino().display_grid()
