import time


def read_file_to_list(file_name):
    file = open(file_name, 'r')
    input_data = (file.readline().rstrip(']\n')).lstrip('[').split(',')
    for i in range(len(input_data)):
        input_data[i] = int(input_data[i])
    file.close()
    return input_data


def test_is_solution():
    """
    Test whether the output.txt is an actual solution.

    :return: True if it is a solution, False if it is not.
    """
    output_file_name = 'nqueens_out.txt'
    data = read_file_to_list(output_file_name)
    print("Length of solution is", len(data))
    # print(data[3])
    # data[3] = 71  # if any number changed this should no longer be a solution
    is_solution = True
    for row in range(len(data)):
        if get_num_conflict_at_square(row, data[row], data) != 0:
            is_solution = False
    print("Is this a solution:", is_solution)
    return is_solution


def get_num_conflict_at_square(row1, col1, solution):
    num_conflict_at_square = 0
    for row2 in range(0, len(solution)):
        if row1 != row2:
            col2 = solution[row2]
            if has_conflict(row1, col1, row2, col2):
                num_conflict_at_square += 1
    return num_conflict_at_square


def has_conflict(row1, col1, row2, col2):
    return (row1 == row2) or (col1 == col2) or (row1 - col1 == row2 - col2) or (row1 + col1 == row2 + col2)


def main():
    test_is_solution()


main()
