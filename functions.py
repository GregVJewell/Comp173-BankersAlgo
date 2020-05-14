from os import listdir


# Gets file from user
def file():
    while 1:
        print(listdir("Input Files"))
        f = input("Please Select a File: ")

        if f in listdir("Input Files"):
            return f
        else:
            print("Please select one of the listed files")


# Used to print/verify file contents
def structure(arr):
    print("Number of Processes: ", arr[0])
    print("Number of Resource Types: ", arr[1])
    print("Available Resources: ", arr[2])
    if len(arr) == 6:
        print("Allocation Matrix:\t\tRequest Matrix:\t\tNeed Matrix:")
        for index in range(len(arr[3])):
            print('\t%s\t\t\t\t%s\t\t\t%s' % (arr[3][index], arr[4][index], arr[5][index]))
    else:
        print("Allocation Matrix:\t\t Request Matrix:")
        for index in range(len(arr[3])):
            print('\t%s\t\t\t\t%s' % (arr[3][index], arr[4][index]))


# Calculates need-matrix
def calcNeed(arr):
    need = [[]]
    maximum = arr[4]
    allocated = arr[3]
    for row in range(0, arr[0]):
        need.append([])
        for col in range(0, arr[1]):
            need[row].append(maximum[row][col] - allocated[row][col])

    del need[len(need)-1]

    # print("\nNeed Matrix:")
    # for x in range(len(need)):
    #     print('\t', need[x])

    return need


# Work-Horse, all math done here
def allocation(dictionary):
    stop = False
    missed = []
    order = []

    new_available = dictionary.get("available").copy()

# First Pass for Deadlock detection
    for x in range(dictionary.get("processes") + 1):
        if stop is True:
            break
        print("Checking Process: %d" % x)
        dictionary.update({"available": new_available.copy()})
        if x == dictionary.get("processes"):
            print("Final Available: ", dictionary.get("available"))
            break
        else:
            print("-> Current Available: ", dictionary.get("available"))

        for y in range(dictionary.get("resources")):
            print("\tCheck %s <= %s" % (dictionary.get("need")[x][y], dictionary.get("available")[y]))
            if dictionary.get("need")[x][y] > dictionary.get("available")[y]:
                # Break = True
                print("----Process %d Failed to Allocate----" % x)
                new_available = dictionary.get("available")
                missed.append(x)
                break
            else:
                new_available[y] = dictionary.get("available")[y] + dictionary.get("allocation")[x][y]
        order.append(x)

# Just to create first pass process order
    if len(missed) > 0:
        index = 0
        while index < len(missed):
            value = missed[index]
            for x in order:
                if x == value:
                    order.remove(x)
            index += 1
        del index, value

# Next passes to determine if missed process is deadlocked, or can be
# re-allocated later in program
        for x in missed:
            print("Re-Checking Process: %d" % x)
            dictionary.update({"available": new_available.copy()})
            print("-> Current Available: ", dictionary.get("available"))
            for y in range(dictionary.get("resources")):
                print("\tCheck %s <= %s" % (dictionary.get("need")[x][y], dictionary.get("available")[y]))
                if dictionary.get("need")[x][y] > dictionary.get("available")[y]:
                    print("Deadlock has been found at process: ", x)
                    exit(1)
                else:
                    new_available[y] = dictionary.get("available")[y] + dictionary.get("allocation")[x][y]

            order.append(x)
            dictionary.update({"available": new_available.copy()})

    return dictionary, order, missed
