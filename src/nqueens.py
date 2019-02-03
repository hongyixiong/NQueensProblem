import random
import time


def nqueens_min_conflicts_backtrack(n):
    # print(n)
    pass


def read_file_to_list(file_name):
    file = open(file_name, "r")
    input_data = [line.rstrip('\n') for line in file]
    file.close()
    return input_data


def write_2d_list_to_file(data, file_name):
    # todo: remove setting data created for testing purpose
    data = [[1, 2, 3, 4], ['a', 3, 'be', 5, 8], [], [4, 9, 1, 5, '2faf']]
    file = open(file_name, "w+")
    for row in range(0, len(data)):
        new_line = '[' + ''.join([(str(x) + ',') for x in data[row]]).rstrip(',') + ']'
        file.write(new_line + '\n')
    file.close()


def main():
    input_file_name = "nqueens.txt"
    output_file_name = "nqueens_out.txt"
    input_data = read_file_to_list(input_file_name)
    # print(input_data if len(input_data) < 100 else input_data[0:100])

    results = []
    for n in input_data:
        results.append(nqueens_min_conflicts_backtrack(n))

    write_2d_list_to_file(results, output_file_name)


main()
