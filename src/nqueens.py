"""
AI Assignment 1
Group 10
"""
import time
import random

class NQueens:
    def __init__(self, n):
        self.n = n
        self.positions = []
        self.num_conflicts = []
        self.num_attempts = 1

    def nqueens_min_conflicts_iterative_repair(self):
        """
        Uses iterative repair method along with the min-conflicts heuristic to find a solution to the N-Queens problem.

        :return: a list representing a solution to the N-Queens problem
        """
        self.reset_parameters()
        self.generate_initial_positions()
        queens_left = self.new_queens_left_set()
        iteration_number = 0
        max_iteration_number = self.n * 10
        while iteration_number < max_iteration_number:
            if self.is_solution():
                return self.positions
            if len(queens_left) == 0:
                queens_left = self.new_queens_left_set()

            queen_to_move = self.find_max(queens_left)
            queens_left.remove(queen_to_move)
            destination_col, conflicts_decrement_list, conflicts_increment_list = self.min_conflicts(queen_to_move)
            self.move_queen(queen_to_move, destination_col, conflicts_decrement_list, conflicts_increment_list)

        if self.is_solution():
            return self.positions
        else:
            self.num_attempts += 1
            self.nqueens_min_conflicts_iterative_repair()

    def reset_parameters(self):
        """
        Reset the paramemters of the class in order to restart the search for a solution.
        """
        self.positions = []
        self.num_conflicts = []

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

    def min_conflicts(self, row):
        """
        Find a square with minimum number of conflicts on the given row number.

        :param row:
        :return: the destination column number of where the queen should be moved to,
                  the list of row numbers where their conflict numbers need to be reduced by 1, and
                  the list of row numbers where their conflict numbers need to be increased by 1.
        """
        destination_col = 0  # todo: to be replaced
        conflicts_decrement_list = []
        conflicts_increment_list = []

        return destination_col, conflicts_decrement_list, conflicts_increment_list

    def has_conflict(self, row1, col1, row2, col2):
        """
        Determines whether two queens on the given row numbers and column numbers will have a conflict.

        :param row1: row number of first square
        :param col1: column number of first square
        :param row2: row number of second square
        :param col2: column number of second square
        :return: a boolean indicating whether queens on these two squares will have a conflict
        """
        return True

    def generate_initial_positions(self):
        """
        Populate self.positions with values representing queens columns.
        """
        pass

    def move_queen(self, source_row, destination_col, delete_list, update_list):
        """
        Moves a queen on the given row number to the destination column on the same row.
        The function also updates the num_conflicts list.

        :param source_row: the row number of the queen to be moved
        :param destination_col: the col number of the queen to be moved to on the source_row
        :param delete_list: the list of row numbers where their conflict numbers need to be reduced by 1
        :param update_list: the list of row numbers where their conflict numbers need to be increased by 1
        """
        pass

    def find_max(self, queens_left):
        """
        Find the queen with the maximum number of conflicts that has been moved the least amount of times so far.
        If there are more than one queen that satisfies, then choose a queen randomly.

        :param queens_left: a list of row numbers for the queens that have been moved the least amount of times.
        :return: a row number representing the queen
        """
        return -1


def read_file_to_list(file_name):
    file = open(file_name, 'r')
    input_data = [int(line.rstrip('\n')) for line in file]
    file.close()
    return input_data


def write_2d_list_to_file(data, file_name):
    file = open(file_name, 'w+')
    for row in range(0, len(data)):
        # todo: might need to add 1 to x because row and column numbers on a chess board
        # are 1 higher than Python list indices.
        # That is:
        # new_line = '[' + ''.join([(str(x+1) + ',') for x in data[row]]).rstrip(',') + ']'
        new_line = '[' + ''.join([(str(x) + ',') for x in data[row]]).rstrip(',') + ']'
        file.write(new_line + '\n')
    file.close()


def main():
    input_file_name = 'nqueens.txt'
    output_file_name = 'nqueens_out.txt'
    input_data = read_file_to_list(input_file_name)
    # print(input_data if len(input_data) < 100 else input_data[0:100])

    results = []
    for n in input_data:
        nqueens = NQueens(n)
        results.append(nqueens.nqueens_min_conflicts_iterative_repair())

    write_2d_list_to_file(results, output_file_name)


main()
