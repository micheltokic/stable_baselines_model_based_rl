import numpy as np

def nested_list_mean(two_d_array):
    """Average 2D array to 1D array with averaged columns, regardless of their dimension."""
    output = []
    maximum = 0
    # find max index of all nested lists
    for lst in two_d_array:
        maximum = max(maximum, len(lst))
    for index in range(maximum):
        temp = []
        for lst in two_d_array:
            if index < len(lst):
                temp.append(lst[index])
        output.append(np.nanmean(temp))
    return output
