
def main():

    grid =  [
            [1, 2, 3, 0, 0, 4, 6, 8, 5],    # # # # # # # # #
            [1, 2, 3, 0, 0, 4, 6, 8, 5],    #       j       #
            [1, 2, 3, 0, 0, 4, 6, 8, 5],    #               #
            [1, 2, 3, 0, 0, 4, 6, 8, 5],    #               #
            [1, 2, 3, 0, 0, 4, 6, 8, 5],    # i           i #
            [1, 2, 3, 0, 0, 4, 6, 8, 5],    #               #
            [1, 2, 3, 0, 0, 4, 6, 8, 5],    #               #
            [1, 2, 3, 0, 0, 4, 6, 8, 5],    #       j       #
            [1, 2, 3, 0, 0, 4, 6, 8, 5]     # # # # # # # # #
            ]
    valid, missing_numbers = check_list(list)
    print(valid)
    print(missing_numbers)
    new_list = fill_in_list(list, missing_numbers)
    print(new_list)







def check_list(list):
    missing_numbers = []
    valid = True
    for i in range(1, 10):
        count = list.count(i)
        if count > 1:
            valid = False
        elif count == 0:
            valid = False
            missing_numbers.append(i)
    return valid, missing_numbers

def fill_in_list(list, missing_numbers):
    for missing in missing_numbers:
        for i in range(len(list)):
            if list[i] == 0:
                list[i] = missing
                break
    return list


if __name__ == "__main__":
    main()
