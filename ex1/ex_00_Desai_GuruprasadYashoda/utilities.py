def sum_nested_list(list):

    sum = 0
    for i in range(len(list)):
        for j in range(len(list[i])):
                       sum += list[i][j]


    return sum
