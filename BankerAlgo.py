from functions import *
"""
Delete Statements appears throughout
the program to:
A) Help Debug
B) Free Obsolete/Unused Variables
"""


def main():
    matrix = [[]]
    line = 0

# Create data-matrix for data manipulation
    problem = open("Input Files\\" + file(), 'r')
    while line < problem.__sizeof__():
        matrix[line] = problem.readline().strip()

        if matrix[line].count('') == 1:
            del matrix[line]
            break
        else:
            matrix.append([])
        line += 1

    problem.close()
    del line, problem

    # Split lines into individuals
    for row in range(len(matrix)):
        matrix[row] = matrix[row].split()

    # Convert to numbers
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            matrix[row][col] = int(matrix[row][col])

    del row, col

    # Make Arrays for Structure
    processes = matrix[0][0]
    resource_types = matrix[1][0]
    available_resources = matrix[2]
    allocation_matrix = []
    request_matrix = []
    for x in range(3, processes + 3):
        allocation_matrix.append(matrix[x])

    for x in range(processes + 3, len(matrix)):
        request_matrix.append(matrix[x])

    del matrix

    # Pack dictionary full of usable data
    pack = [processes, resource_types, available_resources, allocation_matrix, request_matrix]
    packed = {
        "processes": processes,
        "resources": resource_types,
        "available": available_resources.copy(),
        "allocation": allocation_matrix.copy(),
        "max": request_matrix.copy()
    }

    del processes, resource_types, available_resources, allocation_matrix, request_matrix

    need_matrix = calcNeed(pack)  # Helper Function!
    pack.append(need_matrix)
    structure(pack)  # Helper Function!
    del pack

    packed.setdefault("need", need_matrix.copy())
    del need_matrix, x

    packed, order, missed = allocation(packed)

    del packed

    print("\nProcesses Can Complete by Running in the Order of: ", order)

    del order

    # Check if user wants to run again
    answer = input("Would you like to repeat? Y/N\n")
    if answer.lower() == 'y' or answer.lower() == 'yes':
        main()
    else:
        exit(0)


if __name__ == main():
    main()
