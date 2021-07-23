import numpy as np
import sys


def read_args():
    return sys.argv[2], sys.argv[4]


def read_array(file_name):
    with open(file_name, "r") as file:
        array = [line.split() for line in file.readlines()[1:]]
        try:
            return np.array(array).astype(float)
        except ValueError:
            return np.array(array).astype(complex)


def save_results(file_name, results):
    with open(file_name, "w") as file:
        if type(results) == str:
            file.write(results)
        else:
            file.write("\n".join(results.astype(str)))


def gauss_elimination(array):
    rows, cols = array.shape
    print(array)

    for col in range(cols):
        for row in range(rows):
            val = array[row, col]
            if row == col:
                if val == 0:
                    swap_array = array[row:, col:-1]
                    nonzero_col, nonzero_row = swap_array.T.nonzero()
                    if len(nonzero_row) < 1:
                        continue
                    nonzero_row = nonzero_row[0] + row
                    nonzero_col = nonzero_col[0] + col
                    array[[row, nonzero_row]] = array[[nonzero_row, row]]
                    array[:, [col, nonzero_col]] = array[:, [nonzero_col, col]]
                    val = array[row, col]
                    print("R", row, "<->", "R", nonzero_row)
                    print("C", col, "<->", "C", nonzero_col)
                if val != 1:
                    array[row] /= val
                    print("R", row, "/", val, "-> R", row)
            elif row > col and val != 0:
                array[row] -= array[col] * val
                print("R", row, "-", "R", col, "*", val, "-> R", row)

    for col in range(cols - 1, -1, -1):
        for row in range(rows - 1, -1, -1):
            val = array[row, col]
            if val == 0:
                continue
            elif row < col < rows:
                array[row] -= array[col] * val
                print("R", row, "-", "R", col, "*", val, "-> R", row)

    for row in range(rows - 1, -1, -1):
        if not array[row].any():
            array = np.delete(array, row, 0)

    if not array[-1, :-1].any() and array[-1, -1] != 0:
        return "No solutions"
    if np.count_nonzero(array[-1, :-1]) > 1 or array[-1, -2] != 1:
        return "Infinitely many solutions"

    return array


def read_results(results):
    if type(results) == str:
        return results
    return results[:, -1]


def execute():
    infile, outfile = read_args()
    input_array = read_array(infile)
    input_array = gauss_elimination(input_array)
    results = read_results(input_array)
    save_results(outfile, results)


execute()