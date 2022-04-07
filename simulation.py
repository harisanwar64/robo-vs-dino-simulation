simulation_grid = []
x_grid_space = 5
y_grid_space = 5


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


if __name__ == "__main__":
    RoboVsDino().create_grid()
    RoboVsDino().display_grid()