"""
AI Assignment 1
N-Queens Problem
Group 10
"""
import random
import time


class NQueens:
    def __init__(self, n):
        """
        Constructor

        :param n: size of the board
        """
        self.n = n
        self.positions = []
        self.num_conflicts = []
        self.col_to_occurrence = dict()
        # left diagonal keys from -(n-1) to n-1, right diagonal keys from 0 to 2*(n-1)
        # add 1 to the right end due to definition of range function, and we get (n-1)+1 = n, and 2*(n-1)+1 = 2*n-1
        self.left_diagonal_to_rows = dict.fromkeys([x for x in range(-n + 1, n)])
        self.right_diagonal_to_rows = dict.fromkeys([x for x in range(0, 2 * n - 1)])
        self.column_number_to_rows = dict.fromkeys(x for x in range(0, n))
        # parameters for algorithm analysis
        self.num_attempts = 1
        self.num_steps = 0
        self.start_time = time.time()
        self.initialization_time_duration = 0

    def nqueens_min_conflicts_iterative_repair(self):
        """
        Uses iterative repair method along with the min-conflicts heuristic to find a solution to the N-Queens problem.

        :return: a list representing a solution to the N-Queens problem
        """
        self.reset_parameters()
        self.generate_initial_positions()
        self.initialization_time_duration = time.time() - self.start_time
        queens_left = self.new_queens_left_set()
        iteration_number = 0
        max_iteration_number = self.n * 100
        while iteration_number < max_iteration_number:
            # todo: remove testing
            if iteration_number % 100 == 0:
                print('iteration_number is', iteration_number)
            if self.is_solution():
                self.num_steps = iteration_number
                return self.positions
            if len(queens_left) == 0:
                queens_left = self.new_queens_left_set()

            queen_to_move = self.find_max(queens_left)
            queens_left.remove(queen_to_move)
            destination_col, conflicts_decrement_list, conflicts_increment_list = self.min_conflicts(queen_to_move)
            self.move_queen(queen_to_move, destination_col, conflicts_decrement_list, conflicts_increment_list)
            # print(iteration_number, "moved queen at row:", queen_to_move,
            #       "to col", destination_col, "     positions:", self.positions)
            # print("queens_left, num_conflicts:", queens_left, self.num_conflicts)
            iteration_number += 1

        if self.is_solution():
            self.num_steps = self.num_steps + iteration_number + 1
            return self.positions
        else:
            self.num_attempts += 1
            # todo: remove testing
            print('Current number of attempts (caused by restarting) is', self.num_attempts)
            return self.nqueens_min_conflicts_iterative_repair()

    def reset_parameters(self):
        """
        Reset the parameters of the class in order to restart the search for a solution.
        """
        self.positions = []
        self.num_conflicts = [0 for x in range(self.n)]
        for i in range(0, self.n):
            self.col_to_occurrence[i] = 0

        for k in self.left_diagonal_to_rows.keys():
            self.left_diagonal_to_rows[k] = set()

        for k in self.right_diagonal_to_rows.keys():
            self.right_diagonal_to_rows[k] = set()

        for k in self.column_number_to_rows.keys():
            self.column_number_to_rows[k] = set()

    def new_queens_left_set(self):
        """
        Create a new set for queens_left.

        :return: a set consists of numbers from 0 to n-1
        """
        return set(x for x in range(0, self.n))

    def is_solution(self):
        """
        Checks whether a solution is found, that is, whether all elements in the num_conflicts list is 0.

        :return: a boolean indicating whether num_conflicts has size n and all elements of the num_conflicts is 0.
        """
        return not any(self.num_conflicts)

    def generate_initial_positions(self):
        """
        Populate self.positions with values representing queens columns.
        """
        for row in range(0, self.n):
            # todo: remove testing
            if row % 100 == 0:
                print("Creating queen at row", row)
            destination_col, conflicts_decrement_list, conflicts_increment_list = self.min_conflicts(row)
            self.col_to_occurrence[destination_col] = self.col_to_occurrence[destination_col] + 1
            self.positions.append(destination_col)
            self.update_num_conflicts(row, destination_col, conflicts_decrement_list, conflicts_increment_list)

    def min_conflicts(self, row):
        """
        Find a square with minimum number of conflicts on the given row number.

        :param row: a row number of concern on the chess board.
        :return: the destination column number of where the queen should be moved to,
                 the list of row numbers where their conflict numbers need to be reduced by 1, and
                 the list of row numbers where their conflict numbers need to be increased by 1
        """
        # min_conflict is the current minimum number of conflicts at a column along the row.
        # Must be initialized to a number greater than the largest possible number of conflicts, i.e. self.n
        min_conflict = self.n
        min_conflict_cols = []  # columns with the minimum number of conflicts

        # len(self.positions <= row if and only if the program is generating initial positions.
        if len(self.positions) <= row:
            col1 = None
        else:
            col1 = self.positions[row]

        not_found = -1  # must be a number outside of range 0 to n-1 inclusive.
        destination_col = not_found
        for col2 in self.col_to_occurrence:
            if col1 != col2 and self.col_to_occurrence[col2] == 0:
                if self.is_num_conflict_at_square_zero(row, col2):
                    destination_col = col2
                    # break
                    min_conflict_cols.append(col2)
        if len(min_conflict_cols) > 0:
            destination_col = self.select_random_element(min_conflict_cols)

        if destination_col == not_found:
            found_one_conflict_col = False
            counter = 0
            max_num_tries = self.n
            while not found_one_conflict_col and counter < max_num_tries:
                rand_col = random.randrange(0, self.n)
                if col1 != rand_col and self.is_num_conflict_at_square_one(row, rand_col) == 1:
                    destination_col = rand_col
                    found_one_conflict_col = True
                counter = counter + 1

        if destination_col == not_found:
            # Iterate through all the columns along the given row.
            for col2 in range(0, self.n):
                if col2 != col1:
                    num = self.get_num_conflict_at_square(row, col2)
                    if num < min_conflict:
                        min_conflict = num
                        min_conflict_cols = [col2]
                    elif num == min_conflict:
                        min_conflict_cols.append(col2)
            destination_col = self.select_random_element(min_conflict_cols)

        if col1 is not None:
            self.remove_from_maps_for_queen(row, col1)
        self.add_to_maps_for_queen(row, destination_col)
        conflicts_decrement_list, conflicts_increment_list = \
            self.compute_conflict_changes_lists(row, col1, destination_col)

        return destination_col, conflicts_decrement_list, conflicts_increment_list

    def get_num_conflict_at_square(self, row1, col1):
        """
        Compute the number of conflicts at the given square.

        :param row1: the row index of the square
        :param col1: the column index of the square
        :return: the number of conflicts at the square
        """
        num_conflict_at_square = 0
        for row2 in range(0, len(self.positions)):
            if row1 != row2:
                col2 = self.positions[row2]
                if self.has_conflict(row1, col1, row2, col2):
                    num_conflict_at_square += 1

        return num_conflict_at_square

    def is_num_conflict_at_square_zero(self, row1, col1):
        """
        Checks whehter the number of conflicts at the given square is 0.

        :param row1: the row index of the square
        :param col1: the column index of the square
        :return: a boolean indicating whether the number of conflict is 0 at the given square.
        """
        left_diagonal_index = self.get_left_diagonal_index(row1, col1)
        right_diagonal_index = self.get_right_diagonal_index(row1, col1)

        left_diagonal_queens = self.left_diagonal_to_rows[left_diagonal_index]
        right_diagonal_queens = self.right_diagonal_to_rows[right_diagonal_index]
        col_queens = self.column_number_to_rows[col1]
        if len(left_diagonal_queens) != 0 or len(right_diagonal_queens) != 0 or len(col_queens) != 0:
            return False
        return True

    def is_num_conflict_at_square_one(self, row1, col1):
        """
        Checks whehter the number of conflicts at the given square is 1.

        :param row1: the row index of the square
        :param col1: the column index of the square
        :return: a boolean indicating whether the number of conflict is 1 at the given square.
        """
        left_diagonal_index = self.get_left_diagonal_index(row1, col1)
        right_diagonal_index = self.get_right_diagonal_index(row1, col1)

        left_diagonal_queens = self.left_diagonal_to_rows[left_diagonal_index]
        right_diagonal_queens = self.right_diagonal_to_rows[right_diagonal_index]
        col_queens = self.column_number_to_rows[col1]
        if len(left_diagonal_queens) + len(right_diagonal_queens) + len(col_queens) != 1:
            return False
        return True

    def has_conflict(self, row1, col1, row2, col2):
        """
        Determines whether two queens on the given row numbers and column numbers will have a conflict.

        :param row1: row number of the first square
        :param col1: column number of the first square
        :param row2: row number of the second square
        :param col2: column number of the second square
        :return: a boolean indicating whether queens on these two squares will have a conflict
        """
        return (row1 == row2) or (col1 == col2) or (row1 - col1 == row2 - col2) or (row1 + col1 == row2 + col2)

    def select_random_element(self, lis):
        """
        Randomly select an element from the given list.

        :param lis: a list
        :return: a random element in the list
        """
        index = random.randrange(0, len(lis))
        return lis[index]

    def compute_conflict_changes_lists(self, row, col1, col2):
        """
        Compute the lists that contains the row numbers where their conflict numbers need to be reduced by 1 and
        increased by 1.

        :param row: the row of the queen
        :param col1: the original column of the queen
        :param col2: the destination column of the queen
        :return: the list of row numbers where their conflict numbers need to be reduced by 1, and
                 the list of row numbers where their conflict numbers need to be increased by 1
        """
        conflicts_decrement_list = []
        if col1 is not None:
            conflicts_decrement_list = self.get_conflicting_positions(row, col1)
        conflicts_increment_list = self.get_conflicting_positions(row, col2)

        return conflicts_decrement_list, conflicts_increment_list

    def get_conflicting_positions(self, row1, col1):
        """
        Get a list of row numbers representing the queens in conflict with this square,
        not including the square itself.

        :param row1: row index of the square
        :param col1: column index of the square
        :return: a list of row numbers representing the queens in conflict with this square
        """
        conflicting_positions = []
        left_diagonal_index = self.get_left_diagonal_index(row1, col1)
        right_diagonal_index = self.get_right_diagonal_index(row1, col1)

        left_diagonal_queens = self.left_diagonal_to_rows[left_diagonal_index]
        right_diagonal_queens = self.right_diagonal_to_rows[right_diagonal_index]
        col_queens = self.column_number_to_rows[col1]

        for queen in left_diagonal_queens:
            if queen != row1:
                conflicting_positions.append(queen)
        for queen in right_diagonal_queens:
            if queen != row1:
                conflicting_positions.append(queen)
        for queen in col_queens:
            if queen != row1:
                conflicting_positions.append(queen)

        return conflicting_positions

    def move_queen(self, source_row, destination_col, conflicts_decrement_list, conflicts_increment_list):
        """
        Moves a queen on the given row number to the destination column on the same row.
        The function also updates the num_conflicts list.

        :param source_row: the row number of the queen to be moved
        :param destination_col: the col number of the queen to be moved to on the source_row
        :param conflicts_decrement_list: the list of row numbers where their conflict numbers need to be reduced by 1
        :param conflicts_increment_list: the list of row numbers where their conflict numbers need to be increased by 1
        """
        source_col = self.positions[source_row]
        self.col_to_occurrence[source_col] = self.col_to_occurrence[source_col] - 1
        self.col_to_occurrence[destination_col] = self.col_to_occurrence[destination_col] + 1
        self.positions[source_row] = destination_col
        self.update_num_conflicts(source_row, destination_col, conflicts_decrement_list, conflicts_increment_list)

    def update_num_conflicts(self, source_row, destination_col, conflicts_decrement_list, conflicts_increment_list):
        """
        Update the number of conflicts for each queen.

        :param source_row: the row index of the queen in change
        :param destination_col: the column index of the queen in change
        :param conflicts_decrement_list: the list of row numbers where their conflict numbers need to be reduced by 1
        :param conflicts_increment_list: the list of row numbers where their conflict numbers need to be increased by 1
        """
        self.num_conflicts[source_row] = self.get_num_conflict_at_square(source_row, destination_col)
        self.num_conflicts_decrement(conflicts_decrement_list)
        self.num_conflicts_increment(conflicts_increment_list)

    def num_conflicts_decrement(self, conflicts_decrement_list):
        """
        Decrease the number of conflicts for the queens at the rows given in conflicts_decrement_list by 1.

        :param conflicts_decrement_list: a list of row numbers of queens where number of conflicts to be reduced.
        """
        for row in conflicts_decrement_list:
            self.num_conflicts[row] = self.num_conflicts[row] - 1

    def num_conflicts_increment(self, conflicts_increment_list):
        """
        Increase the number of conflicts for the queens at the rows given in conflicts_decrement_list by 1.

        :param conflicts_increment_list: a list of row numbers of queens where number of conflicts is to be increase.
        """
        for row in conflicts_increment_list:
            self.num_conflicts[row] = self.num_conflicts[row] + 1

    def find_max(self, queens_left):
        """
        Find the queen with the maximum number of conflicts that has been moved the least amount of times so far.
        If there are more than one queen that satisfies, then choose a queen randomly.

        :param queens_left: a list of row numbers for the queens that have been moved the least amount of times.
        :return: a row number representing the queen with maximum number of conflicts.
        """
        max_num_conflicts = -1
        max_conflict_row_index = -1
        for row in queens_left:
            num_conflict = self.num_conflicts[row]
            if num_conflict > max_num_conflicts:
                max_num_conflicts = num_conflict
                max_conflict_row_index = row
        return max_conflict_row_index

    def get_left_diagonal_index(self, row):
        """
        Get a unique index key of the left diagonal that the queen is at.

        :param row: row number of a queen
        :return: the index of the uniquely defined left diagonal for the queen.
        """
        return row - self.positions[row]

    def get_left_diagonal_index(self, row, col):
        """
        Get a unique index key of the left diagonal of a square.

        :param row: row number of a square
        :param col: column number of a square
        :return: the index of the uniquely defined left diagonal for the square.
        """
        return row - col

    def get_right_diagonal_index(self, row):
        """
        Get a unique index key of the right diagonal that the queen is at.

        :param row: row number of a queen
        :return: the index of the uniquely defined right diagonal for the queen.
        """
        return row + self.positions[row]

    def get_right_diagonal_index(self, row, col):
        """
        Get a unique index key of the right diagonal of a square.

        :param row: row number of a square
        :param col: column number of a square
        :return: the index of the uniquely defined right diagonal for the square.
        """
        return row + col

    def add_to_maps_for_queen(self, row, col):
        """
        Update mapping information for the queen placed at the given row and column.

        :param row: row number of the queen
        :param col: column number of the queen
        """
        left_diagonal_index = row - col
        right_diagonal_index = row + col
        self.column_number_to_rows[col].add(row)
        self.left_diagonal_to_rows[left_diagonal_index].add(row)
        self.right_diagonal_to_rows[right_diagonal_index].add(row)

    def remove_from_maps_for_queen(self, row, col):
        """
        Update mapping information for the queen removed from the given row and column.

        :param row: row number of the queen
        :param col: column number of the queen
        """
        left_diagonal_index = row - col
        right_diagonal_index = row + col
        # remark: potentially need to check existence before removing.
        # but do not necessarily need to check because when the functions is called
        # the row must have been added to the mappings.
        self.column_number_to_rows[col].remove(row)
        self.left_diagonal_to_rows[left_diagonal_index].remove(row)
        self.right_diagonal_to_rows[right_diagonal_index].remove(row)


def read_file_to_list(file_name):
    file = open(file_name, 'r')
    input_data = [int(line.rstrip('\n')) for line in file]
    file.close()
    return input_data


def write_1d_list_to_file(data, file_name):
    file = open(file_name, 'a+')
    # needed to add 1 to x because row and column numbers on a chess board
    # are 1 higher than Python list indices.
    new_line = '[' + ''.join([(str(x + 1) + ',') for x in data]).rstrip(',') + ']'
    file.write(new_line + '\n')
    file.close()


def write_2d_list_to_file(data, file_name):
    file = open(file_name, 'w+')
    for row in range(0, len(data)):
        # needed to add 1 to x because row and column numbers on a chess board
        # are 1 higher than Python list indices.
        new_line = '[' + ''.join([(str(x + 1) + ',') for x in data[row]]).rstrip(',') + ']'
        file.write(new_line + '\n')
    file.close()


def main():
    input_file_name = 'nqueens.txt'
    output_file_name = 'nqueens_out.txt'
    # open and then close the file with w+ so that the file starts empty
    file = open(output_file_name, 'w+')
    file.close()

    input_data = read_file_to_list(input_file_name)
    # results = []
    for n in input_data:
        if n >= 4:
            print("Finding a solution for n =", n)
            start_time = time.time()
            nqueens = NQueens(n)
            # results.append(nqueens.nqueens_min_conflicts_iterative_repair())
            write_1d_list_to_file(nqueens.nqueens_min_conflicts_iterative_repair(), output_file_name)
            print("The time duration for initialization is", nqueens.initialization_time_duration)
            print("The total time used for n =", n, "is", time.time() - start_time)
            print("The number of attempts taken for n =", n, "is", nqueens.num_attempts)
            print("The number of repairs taken for n =", n, "is", nqueens.num_steps)
        else:
            print("There is no solution for n equal to", n, end='')
            print(" or any other n less than or equal to 3.")
        print()
    # write_2d_list_to_file(results, output_file_name)


main()
