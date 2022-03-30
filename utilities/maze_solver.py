import curses
import queue
import time


class MazeSolver:
    """ 
    The class contains the maze solving functions.
    """

    def find_path(self, maze, visualize, stdScreen):
        """
        The function finds the solution path of the maze.
        :param maze: the maze.
        :type maze: list
        :param visualize: check if the user want to see the maze solving in action.
        :type visualize: bool
        :param stdScreen: the screen curses object
        :type stdScreen: curses.window()
        :return: the path
        :rtype: list
        """

        start_char = "O"
        end_char = "X"
        start_pos = self.find_start(maze, start_char)

        q = queue.Queue()
        q.put((start_pos, [start_pos]))

        visited = set()

        while not q.empty():
            current_pos, path = q.get()
            row, col = current_pos

            if visualize:
                stdScreen.clear()
                self.print_maze(maze, stdScreen, path)
                time.sleep(0.2)
                stdScreen.refresh()

            if maze[row][col] == end_char:
                return path

            neighbors = self.find_neighbors(maze, row, col)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue

                r, c = neighbor
                if maze[r][c] == "#":
                    continue

                new_path = path + [neighbor]
                q.put((neighbor, new_path))
                visited.add(neighbor)

    @staticmethod
    def find_start(maze, start):
        """
        The function find the start cell according to the start char.
        :param maze: the maze.
        :type maze: list
        :param start: Start char
        :type start: str
        :return: the coordinates or None
        :rtype: tuple or None
        """
        for i, row in enumerate(maze):
            for j, value in enumerate(row):
                if value == start:
                    return i, j

        return None

    @staticmethod
    def print_maze(maze, stdScreen, path=None):
        """
        The function print the maze to the screen.
        :param maze: the maze.
        :type maze: list
        :param stdScreen: the screen curses object
        :type stdScreen: curses.window()
        :param path: the solution path
        :type path: list
        :return: None
        :rtype: None
        """

        if path is None:
            path = []

        BLUE = curses.color_pair(1)
        RED = curses.color_pair(2)

        for i, row in enumerate(maze):
            for j, value in enumerate(row):
                try:
                    if (i, j) in path:
                        stdScreen.addstr(i, j * 2, "X", RED)
                    else:
                        stdScreen.addstr(i, j * 2, value, BLUE)
                except curses.error:
                    pass

    @staticmethod
    def find_neighbors(maze, row, col):
        """
        The function find the neighbours.
        :param maze: the maze.
        :type maze: list
        :param row: the row number.
        :type row: int
        :param col: the column number.
        :type col: int
        :return: the neighbours
        :rtype: list
        """
        neighbors = []

        if row > 0:  # UP
            neighbors.append((row - 1, col))
        if row + 1 < len(maze):  # DOWN
            neighbors.append((row + 1, col))
        if col > 0:  # LEFT
            neighbors.append((row, col - 1))
        if col + 1 < len(maze[0]):  # RIGHT
            neighbors.append((row, col + 1))

        return neighbors
