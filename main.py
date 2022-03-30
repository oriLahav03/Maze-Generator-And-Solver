import curses

from utilities.maze import Maze
from utilities.maze_solver import MazeSolver
from utilities.user_input import UserInput


def main(stdScreen=None, **kwargs):
    solve_maze = kwargs['kwargs']['solve_maze']
    visualize = kwargs['kwargs']['visualize']
    maze_size = kwargs['kwargs']['maze_size']

    maze_columns, maze_rows = maze_size, maze_size

    maze = Maze(maze_columns, maze_rows, 0, 0)
    maze.make_maze()

    solver = MazeSolver()

    if visualize:
        # initialize the colors
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

        path = solver.find_path(maze.final_maze_to_solve, visualize, stdScreen)
        maze.write_svg('mazes/maze.svg', True, path)
        stdScreen.getch()

    elif solve_maze:
        path = solver.find_path(maze.final_maze_to_solve, visualize, stdScreen)
        maze.write_svg('mazes/maze-solved.svg', True, path)

    maze.write_svg('mazes/maze.svg', False)


if __name__ == '__main__':
    size = UserInput.get_maze_size()
    view = UserInput.visualize_solving()

    if view:
        try:
            curses.wrapper(main, kwargs={'maze_size': size, 'visualize': view, 'solve_maze': True})
        except curses.error:
            exit('Visualization only works in terminal.')
    else:
        solve = UserInput.get_solve_option()
        main(None, kwargs={'maze_size': size, 'visualize': False, 'solve_maze': solve})
