class UserInput:
    """
    The class contains the input from the user functions.
    """

    @staticmethod
    def get_solve_option():
        """
        the function ask the user if he wants the maze solution and return it.
        :return: the answer.
        :rtype: bool
        """
        solve_op = input("Would you like to get a solution as well? (y/n): ").lower()
        if solve_op in ['y', 'yes']:
            return True
        elif solve_op in ['n', 'no']:
            return False
        else:
            exit(f'Invalid option: {solve_op}')

    @staticmethod
    def visualize_solving():
        """
        the function ask the user if he wants to view the maze solving and return it.
        :return: the answer.
        :rtype: bool
        """
        view_solve = input("Would you like to view the solving algorithm (Only Available In Terminal)? (y/n): ").lower()
        if view_solve in ['y', 'yes']:
            return True
        elif view_solve in ['n', 'no']:
            return False
        else:
            exit(f'Invalid option: {view_solve}')

    @staticmethod
    def get_maze_size():
        """
        the function ask the user for the maze size / difficulty and return it.
        :return: the size / difficulty
        :rtype: int
        """
        maze_size = input("What size / difficulty would you like your maze to be? (5-50): ")
        if maze_size.isdigit():
            if 5 <= int(maze_size) <= 50:
                return int(maze_size)
        exit(f'Invalid size: {maze_size}')