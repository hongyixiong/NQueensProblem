"""
AI Assignment 1
N-Queens Problem
Group 10
"""
import time
import random


class NQueens:
    def __init__(self, n):
        self.n = n
        self.positions = []
        self.num_conflicts = [0 for x in range(n)]
        self.col_to_occurrence = dict()
        # todo: remove testing
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
        # print("Starting to generate initial positions")
        self.generate_initial_positions()
        self.initialization_time_duration = time.time() - self.start_time
        # print("Ended to generate initial positions")
        queens_left = self.new_queens_left_set()
        iteration_number = 0
        max_iteration_number = self.n * 100
        while iteration_number < max_iteration_number:
            # todo: remove testing
            if iteration_number % 50 == 0:
                print('iteration_number is', iteration_number)
            if self.is_solution():
                self.num_steps = self.num_steps + iteration_number + 1
                return self.positions
            if len(queens_left) == 0:
                queens_left = self.new_queens_left_set()

            queen_to_move = self.find_max(queens_left)
            queens_left.remove(queen_to_move)
            destination_col, conflicts_decrement_list, conflicts_increment_list = self.min_conflicts(queen_to_move)
            self.move_queen(queen_to_move, destination_col, conflicts_decrement_list, conflicts_increment_list)
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

    def new_queens_left_set(self):
        """
        Create a new set for queens_left.
        :return: a set consists of numbers from 0 to n-1
        """
        return set([x for x in range(0, self.n)])

    def is_solution(self):
        """
        Checks whether a solution is found, that is, whether all elements in the num_conflicts list is 0.

        :return: a boolean indicating whether num_conflicts has size n and all elements of the num_conflicts is 0.
        """
        return len(self.num_conflicts) == self.n and not any(self.num_conflicts)

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

        if len(self.positions) <= row:
            col1 = None
        else:
            col1 = self.positions[row]

        not_found = -1  # must be a number outside of range 0 to n-1 inclusive.
        destination_col = not_found
        for col2 in self.col_to_occurrence:
            if self.col_to_occurrence[col2] == 0:
                if self.is_num_conflict_at_square_zero(row, col2):
                    destination_col = col2
                    break
        #             min_conflict_cols.append(col2)
        # if len(min_conflict_cols) > 0:
        #     destination_col = self.select_random_element(min_conflict_cols)
        if destination_col == not_found:
            found_one_conflict_col = False
            counter = 0
            max_num_tries = 100
            while not found_one_conflict_col and counter < max_num_tries:
                rand_col = random.randrange(0, self.n)
                if self.is_num_conflict_at_square_one(row, rand_col) == 1:
                    destination_col = rand_col
                    found_one_conflict_col = True

        if destination_col == not_found:
            # Iterate through all the columns along the given row.
            for col2 in range(0, self.n):
                if col2 != col1:
                    num = self.get_num_conflict_at_square(row, col2)  # O(n)
                    if num < min_conflict:
                        min_conflict = num
                        min_conflict_cols = [col2]
                    elif num == min_conflict:
                        min_conflict_cols.append(col2)
            destination_col = self.select_random_element(min_conflict_cols)

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
        for row2 in range(0, len(self.positions)):
            if row1 != row2:
                col2 = self.positions[row2]
                if self.has_conflict(row1, col1, row2, col2):
                    return False
        return True

    def is_num_conflict_at_square_one(self, row1, col1):
        """
        Checks whehter the number of conflicts at the given square is 1.

        :param row1: the row index of the square
        :param col1: the column index of the square
        :return: a boolean indicating whether the number of conflict is 1 at the given square.
        """
        num_conflict_at_square = 0
        for row2 in range(0, len(self.positions)):
            if row1 != row2:
                col2 = self.positions[row2]
                if self.has_conflict(row1, col1, row2, col2):
                    num_conflict_at_square = num_conflict_at_square + 1
                    if num_conflict_at_square == 2:
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
        for row2 in range(0, len(self.positions)):
            if row1 != row2:
                col2 = self.positions[row2]
                if self.has_conflict(row1, col1, row2, col2):
                    conflicting_positions.append(row2)
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
        max = -1
        max_conflict_row_index = -1
        for row in queens_left:
            num_conflict = self.num_conflicts[row]
            if num_conflict > max:
                max = num_conflict
                max_conflict_row_index = row
        return max_conflict_row_index


def read_file_to_list(file_name):
    file = open(file_name, 'r')
    input_data = [int(line.rstrip('\n')) for line in file]
    file.close()
    return input_data


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
    input_data = read_file_to_list(input_file_name)
    # print(input_data if len(input_data) < 100 else input_data[0:100])

    results = []
    for n in input_data:
        if n >= 4:
            print("Finding a solution for n =", n)
            nqueens = NQueens(n)
            start_time = time.time()
            results.append(nqueens.nqueens_min_conflicts_iterative_repair())
            print("The time duration for initialization is", nqueens.initialization_time_duration)
            print("The time used for n =", n, "is", time.time() - start_time)
            print("The number of attempts taken for n =", n, "is", nqueens.num_attempts)
            print("The number of steps taken for n =", n, "is", nqueens.num_steps)
        else:
            print("There is no solution for n less than or equal to 3.")

    write_2d_list_to_file(results, output_file_name)


main()
