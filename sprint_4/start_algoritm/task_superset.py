def list_superset(list_set_1, list_set_2):
    check_1_in_2 = check_lists(list_set_1, list_set_2)
    check_2_in_1 = check_lists(list_set_2, list_set_1)

    if check_1_in_2 and not check_2_in_1:
        return f'Набор {list_set_2} - супермножество.'
    elif check_2_in_1 and not check_1_in_2:
        return f'Набор {list_set_1} - супермножество.'
    elif check_1_in_2 and check_2_in_1:
        return 'Наборы равны.'
    else:
        return 'Супермножество не обнаружено.'


def check_lists(list1, list2):
    return True if all(item in list2 for item in list1) else False


list_set_1 = [1, 3, 5, 7]
list_set_2 = [3, 5]
list_set_3 = [5, 3, 7, 1]
list_set_4 = [5, 6]

print(list_superset(list_set_1, list_set_2))
print(list_superset(list_set_2, list_set_3))
print(list_superset(list_set_1, list_set_3))
print(list_superset(list_set_2, list_set_4))
