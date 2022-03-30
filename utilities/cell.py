class Cell:
    """ 
    The class contains the cell object in the maze.

    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, east, south or west.
    """

    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """Initialize the cell at (x,y). At first, it is surrounded by walls."""

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def has_all_walls(self):
        """
        check if the cell have all his walls.
        :return: have or not
        :rtype: bool
        """

        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        """
        the function knock down the wall between cells self and other.
        :param other: other cell.
        :type other: Cell
        :param wall: the wall to take down.
        :type wall: str
        :return: None
        :rtype: None
        """

        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False
