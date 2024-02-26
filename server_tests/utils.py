def value_in_list_of_dicts(value_to_find, list_of_dicts):
    for d in list_of_dicts:
        if value_to_find in d.values():
            return True
    return False


def key_in_list_of_dicts(key_to_find, list_of_dicts):
    for d in list_of_dicts:
        if key_to_find in d:
            return True
    return False
