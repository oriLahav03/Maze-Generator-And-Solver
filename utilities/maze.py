import random
from os.path import exists

from utilities.cell import Cell


class Maze:
    """ 
    The class contains the Maze, represented as a grid of cells. 
    """

    def __init__(self, maze_columns, maze_rows, ix=0, iy=0):
        """Initialize the maze grid.
        The maze consists of maze_columns x maze_rows cells and will be constructed starting
        at the cell indexed at (ix, iy).
        """

        self.maze_number = 1
        self.file_created = False
        self.file_created2 = False
        self.final_maze_to_solve = []
        self.maze_columns, self.maze_rows = maze_columns, maze_rows
        self.ix, self.iy = ix, iy
        self.maze_map = [[Cell(x, y) for y in range(maze_rows)] for x in range(maze_columns)]

    def cell_at(self, x, y):
        """
        the function return the cell object at the given location.
        :param x: the x position.
        :type x: int
        :param y: the y position.
        :type y: int
        :return: the cell.
        :rtype:  Cell
        """
        return self.maze_map[x][y]

    def get_maze_rows(self):
        """
        The function make the maze format into a list.
        :return: the maze
        :rtype: list
        """
        maze_rows = ['#' * (self.maze_columns * 2 + 1)]
        for y in range(self.maze_rows):
            maze_row = ['#']
            for x in range(self.maze_columns):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' #')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['#']
            for x in range(self.maze_columns):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('##')
                else:
                    maze_row.append(' #')
            maze_rows.append(''.join(maze_row))

        maze_rows[0] = maze_rows[0][0] + 'O' + maze_rows[0][2:]
        maze_rows[-1] = maze_rows[-1][0:-2] + 'X' + maze_rows[-1][-1]

        self.final_maze_to_solve = maze_rows

        return maze_rows

    def write_svg(self, file_name, solve_maze, path=None):
        """
        The function creates image of the maze as SVG file.
        :param file_name: the maze name.
        :type file_name: str
        :param solve_maze: create image of the maze's solution?
        :type solve_maze: bool
        :param path: the solution path.
        :type path: list
        :return: None
        :rtype: None
        """

        aspect_ratio = self.maze_columns / self.maze_rows
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.maze_rows, width / self.maze_columns

        def write_wall(ww_f, ww_x1, ww_y1, ww_x2, ww_y2):
            """
            Write a single wall to the SVG image file handle f.
            """

            if round(ww_y1, 2) == 500 and round(ww_x2, 2) == 500 and round(ww_y2, 2) == 500:
                return

            print('  <line x1="{}" y1="{}" x2="{}" y2="{}"/>'
                  .format(ww_x1, ww_y1, ww_x2, ww_y2), file=ww_f)

        # Write the SVG image file for maze
        with open(file_name, 'w') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg" width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                  .format(width + 2 * padding, height + 2 * padding,
                          -padding, -padding, width + 2 * padding, height + 2 * padding),
                  file=f)
            print('  <defs>\n    <style type="text/css"><![CDATA[', file=f)
            print('      line {', file=f)
            print('      stroke: #000000;', file=f)
            print('      stroke-linecap: square;', file=f)
            print('      stroke-width: 5;\n      }]]>', file=f)
            print('    </style>\n  </defs>', file=f)
            print('  <!-- ############# Maze lines ############### -->', file=f)

            # Draw the "South" and "East" walls of each cell, if present (these
            # are the "North" and "West" walls of a neighbouring cell in
            # general, of course).

            for x in range(self.maze_columns):
                for y in range(self.maze_rows):
                    if self.cell_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)

            if solve_maze:
                print('\n', file=f)
                points = ''
                for index in path:
                    x = index[0]
                    y = index[1]
                    points += f'{y * scy // 2}, {x * scx // 2} '

                # create the red solution line
                print('  <!-- ############# Solved Maze lines ############### -->', file=f)
                print('  <polyline points="{}" stroke="red" fill="none" stroke-width="2"/>\n'
                      .format(points), file=f)
            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            print('  <line x1="{}" y1="0" x2="{}" y2="0"/>'.format(width / self.maze_rows, width), file=f)
            print('  <line x1="0" y1="0" x2="0" y2="{}"/>'.format(height), file=f)
            print('</svg>', file=f)

    def find_valid_neighbours(self, cell):
        """
        the function give valid neighbour cell.
        :param cell: the current cell.
        :type cell: Cell
        :return: the neighbours.
        :rtype: list
        """

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.maze_columns) and (0 <= y2 < self.maze_rows):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def make_maze(self):
        """
        The function generate a new maze.
        :return: None
        :rtype: None
        """
        # Total number of cells.
        total_cells_number = self.maze_columns * self.maze_rows
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        # Total number of visited cells during maze construction.
        number_cells_visited = 1

        while number_cells_visited < total_cells_number:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                # We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue

            # Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            number_cells_visited += 1

        self.get_maze_rows()
