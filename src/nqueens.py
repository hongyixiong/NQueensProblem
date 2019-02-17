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

        self.col_occurrences = [0 for x in range(n)]
        self.left_diagonal_occurrences = [0 for x in range((n - 1) * 2 + 1)]
        self.right_diagonal_occurrences = [0 for x in range((n - 1) * 2 + 1)]
        self.cols_left = [x for x in range(self.n)]

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
        max_iteration_number = 500
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

            queen_col = self.positions[queen_to_move]
            queens_left.remove(queen_to_move)
            destination_col = self.min_conflicts(queen_to_move)
            self.move_queen(queen_to_move, destination_col)

            if self.col_occurrences[queen_col] == 0:
                self.cols_left.append(queen_col)
            if self.col_occurrences[destination_col] == 1:
                self.cols_left.remove(destination_col)

            iteration_number += 1

        if self.is_solution():
            self.num_steps = iteration_number
            return self.positions
        else:
            self.num_attempts += 1
            print('Current number of attempts (caused by restarting) is', self.num_attempts)
            return self.nqueens_min_conflicts_iterative_repair()

    def reset_parameters(self):
        """
        Reset the parameters of the class in order to restart the search for a solution.
        """
        self.positions = []
        self.col_occurrences = [0 for x in range(self.n)]
        self.left_diagonal_occurrences = [0 for x in range((self.n - 1) * 2 + 1)]
        self.right_diagonal_occurrences = [0 for x in range((self.n - 1) * 2 + 1)]
        self.cols_left = [x for x in range(self.n)]

        self.num_steps = 0
        self.initialization_time_duration = 0

    def new_queens_left_set(self):
        """
        Create a new set for queens_left.

        :return: a set consists of numbers from 0 to n-1
        """
        return set(x for x in range(0, self.n))

    def is_solution(self):
        """
        Checks whether a solution is found.

        :return: a boolean indicating whether a solution is found.
        """
        for row in range(self.n):
            if self.get_num_conflicts_at_square_with_queen(row, self.positions[row]) != 0:
                return False
        return True

    def generate_initial_positions(self):
        """
        Populate self.positions with values representing queens columns.
        """
        random.shuffle(self.cols_left)

        for row in range(self.n):
            # todo: remove testing
            if row % 1000 == 0:
                print("Creating queen at row", row)
            destination_col = self.min_conflicts_row_initialization(row)
            self.positions.append(destination_col)
            self.update_occurrences(row, None, destination_col)
            # self.cols_left.remove(destination_col)
            self.remove_from_end(destination_col, self.cols_left)

    def min_conflicts_row_initialization(self, row):
        """
        Find a column from the 100 of the remaining columns that has the minimum conflict at the given row.
        :param row: the given row
        :return: the destination column
        """
        min_conflicts = self.n
        min_conflict_cols = []  # columns with the minimum number of conflicts
        # Iterate through 100 of the columns along the given row to save time
        for i in range(len(self.cols_left) - 1, max(-1, len(self.cols_left) - 101), -1):
            col = self.cols_left[i]
            num_conflicts = self.get_num_conflicts_at_square(row, col)
            if num_conflicts < min_conflicts:
                min_conflicts = num_conflicts
                min_conflict_cols = [col]
            elif num_conflicts == min_conflicts:
                min_conflict_cols.append(col)
        destination_col = self.select_random_element(min_conflict_cols)
        return destination_col

    def min_conflicts(self, row):
        """
        Find a square with minimum number of conflicts on the given row number.

        :param row: a row number of concern on the chess board.
        :return: the destination column number of where the queen should be moved to,
                 the list of row numbers where their conflict numbers need to be reduced by 1, and
                 the list of row numbers where their conflict numbers need to be increased by 1
        """
        # len(self.positions <= row if and only if the program is generating initial positions.
        if len(self.positions) <= row:
            col1 = None
        else:
            col1 = self.positions[row]

        min_conflict_cols = []  # columns with the minimum number of conflicts
        one_conflict_cols = []

        not_found = -1  # must be a number outside of range 0 to n-1 inclusive.
        destination_col = not_found

        # random.shuffle(self.cols_left)
        for col2 in self.cols_left:
            num_conflict = self.get_num_conflicts_at_square(row, col2)
            if col1 != col2 and num_conflict == 0:
                destination_col = col2
                # break
                min_conflict_cols.append(col2)
            elif num_conflict == 1:
                one_conflict_cols.append(col2)
        if len(min_conflict_cols) > 0:
            destination_col = self.select_random_element(min_conflict_cols)
        min_conflict_cols = []

        # if destination_col == not_found:
        #     found_one_conflict_col = False
        #     if len(one_conflict_cols) > 0:
        #         destination_col = random.choice(one_conflict_cols)
        #         found_one_conflict_col = True
        #     counter = 0
        #     max_num_tries = 100
        #     while not found_one_conflict_col and counter < max_num_tries:
        #         rand_col = random.randrange(0, self.n)
        #         if col1 != rand_col and self.get_num_conflicts_at_square(row, rand_col) == 1:
        #             destination_col = rand_col
        #             found_one_conflict_col = True
        #         counter = counter + 1

        # min_conflict is the current minimum number of conflicts at a column along the row.
        # Must be initialized to a number greater than the largest possible number of conflicts, i.e. self.n
        min_conflicts = 2
        if destination_col == not_found:
            # Iterate through all the columns along the given row.
            rand_start = random.randrange(0, self.n)
            for i in range(rand_start, self.n + rand_start):
                col2 = i % self.n
                if col2 != col1:
                    num_conflicts = self.get_num_conflicts_at_square(row, col2)
                    if num_conflicts >= 3:
                        pass
                    elif num_conflicts == min_conflicts:
                        min_conflict_cols.append(col2)
                    elif num_conflicts < min_conflicts:
                        min_conflicts = num_conflicts
                        min_conflict_cols = [col2]
                if len(min_conflict_cols) > 100:
                    break
            destination_col = self.select_random_element(min_conflict_cols)
        return destination_col

    def select_random_element(self, lis):
        """
        Randomly select an element from the given list.

        :param lis: a list
        :return: a random element in the list
        """
        index = random.randrange(0, len(lis))
        return lis[index]

    def move_queen(self, source_row, destination_col):
        """
        Moves a queen on the given row number to the destination column on the same row.
        The function also updates the num_conflicts list.

        :param source_row: the row number of the queen to be moved
        :param destination_col: the col number of the queen to be moved to on the source_row
        """
        self.update_occurrences(source_row, self.positions[source_row], destination_col)
        self.positions[source_row] = destination_col

    def update_occurrences(self, source_row, original_col, destination_col):
        """
        Update the number of conflicts for each queen.

        :param source_row: the row index of the queen in change
        :param original_col: the original column index of the queen
        :param destination_col: the destination column index of the queen
        """
        if original_col is not None:
            original_left_diagonal_index = self.get_left_diagonal_index(source_row, original_col)
            original_right_diagonal_index = self.get_right_diagonal_index(source_row, original_col)

            self.col_occurrences[original_col] = self.col_occurrences[original_col] - 1
            self.left_diagonal_occurrences[original_left_diagonal_index] = \
                self.left_diagonal_occurrences[original_left_diagonal_index] - 1
            self.right_diagonal_occurrences[original_right_diagonal_index] = \
                self.right_diagonal_occurrences[original_right_diagonal_index] - 1

        destination_left_diagonal_index = self.get_left_diagonal_index(source_row, destination_col)
        destination_right_diagonal_index = self.get_right_diagonal_index(source_row, destination_col)

        self.col_occurrences[destination_col] = self.col_occurrences[destination_col] + 1
        self.left_diagonal_occurrences[destination_left_diagonal_index] = \
            self.left_diagonal_occurrences[destination_left_diagonal_index] + 1
        self.right_diagonal_occurrences[destination_right_diagonal_index] = \
            self.right_diagonal_occurrences[destination_right_diagonal_index] + 1

        # print(source_row, original_col, destination_col, destination_left_diagonal_index, destination_right_diagonal_index)
        # print(self.col_occurrences)
        # print(self.left_diagonal_occurrences)
        # print(self.right_diagonal_occurrences)

    def find_max(self, queens_left):
        """
        Find the queen with the maximum number of conflicts that has been moved the least amount of times so far.
        If there are more than one queen that satisfies, then choose a queen randomly.

        :param queens_left: a list of row numbers for the queens that have been moved the least amount of times.
        :return: a row number representing the queen with maximum number of conflicts.
        """
        max_num_conflicts = -1
        max_conflict_queens = []

        for row in queens_left:
            num_conflict = self.get_num_conflicts_at_square_with_queen(row, self.positions[row])
            if num_conflict > max_num_conflicts:
                max_num_conflicts = num_conflict
                max_conflict_queens = [row]
            elif num_conflict == max_num_conflicts:
                max_conflict_queens.append(row)
        # return self.select_random_element(max_conflict_queens)

        return random.choice(max_conflict_queens)

    def get_num_conflicts_at_square(self, row, col):
        """
        Compute the number of conflicts at a given square.

        :param row: row index of square
        :param col: column index of square
        :return: the number of conflicts
        """
        return self.col_occurrences[col] \
               + self.left_diagonal_occurrences[self.get_left_diagonal_index(row, col)] \
               + self.right_diagonal_occurrences[self.get_right_diagonal_index(row, col)]

    def get_num_conflicts_at_square_with_queen(self, row, col):
        """
        Compute the number of conflicts at a given square where a queen is at.

        :param row: row index of square
        :param col: column index of square
        :return: the number of conflicts at the square with a queen.
        """
        # Minus three because the queen itself is counted 3 times for that square.
        return - 3 + self.col_occurrences[col] \
               + self.left_diagonal_occurrences[self.get_left_diagonal_index(row, col)] \
               + self.right_diagonal_occurrences[self.get_right_diagonal_index(row, col)]

    def get_left_diagonal_index(self, row, col):
        """
        Get a unique index key of the left diagonal of a square.

        :param row: row number of a square
        :param col: column number of a square
        :return: the index of the uniquely defined left diagonal for the square.
        """
        return row - col

    def get_right_diagonal_index(self, row, col):
        """
        Get a unique index key of the right diagonal of a square.

        :param row: row number of a square
        :param col: column number of a square
        :return: the index of the uniquely defined right diagonal for the square.
        """
        return row + col

    def remove_from_end(self, x, lis):
        i = -1
        while lis[i] != x:
            i -= 1
        while i < -1:
            lis[i] = lis[i + 1]
            i += 1
        # remove last element of list.
        lis.pop()


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
