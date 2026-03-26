def new_list():
    newlist = {
        'first': None,
        'last': None,
        'size': 0
    }
    return newlist

def get_elemet(my_list, pos):
    searchpos = 0
    node = my_list['first']
    while searchpos < pos:
        node = node['next']
        searchpos += 1
    return node["info"]

def is_present(my_list, element, cmp_function):
    is_in_array = False
    temp = my_list['first']
    count = 0
    while not is_in_array and temp is not None:
        if cmp_function(element, temp['info']) == 0:
            is_in_array = True
        else:
            temp = temp['next']
            count += 1
    if not is_in_array:
        count = -1
    return count

def add_first(my_list, element):
    new_node = {'info': element, 'next': None}
    if my_list['first'] is None:
        my_list['first'] = new_node
        my_list['last'] = new_node
    else:
        new_node['next'] = my_list['first']
        my_list['first'] = new_node
    my_list['size'] += 1
    return my_list

def add_last(my_list, element):
    new_node = {'info': element, 'next': None}
    if my_list['first'] is None:
        my_list['first'] = new_node
        my_list['last'] = new_node
    else:
        my_list['last']['next'] = new_node
        my_list['last'] = new_node
    my_list['size'] += 1
    return my_list

def size(my_list):
    return my_list['size']

def first_element(my_list):
    return my_list['first']['info']

def is_empty(my_list):
    return my_list['size'] == 0

def last_element(my_list):
    return my_list['last']['info']

def get_element(my_list, pos):
    searchpos = 0
    node = my_list['first']
    while searchpos < pos:
        node = node['next']
        searchpos += 1
    return node["info"]

def remove_first(my_list):
    if my_list['size'] > 0:
        removed_element = my_list['first']['info']
        my_list['first'] = my_list['first']['next']
        my_list['size'] -= 1
        if my_list['size'] == 0:
            my_list['last'] = None
        return removed_element
    else:
        raise IndexError("List is empty")

def remove_last(my_list):
    if my_list['size'] > 0:
        removed_element = my_list['last']['info']
        if my_list['size'] == 1:
            my_list['first'] = None
            my_list['last'] = None
        else:
            current_node = my_list['first']
            while current_node['next'] != my_list['last']:
                current_node = current_node['next']
            current_node['next'] = None
            my_list['last'] = current_node
        my_list['size'] -= 1
        return removed_element
    else:
        raise IndexError("List is empty")

def insert_element(my_list, element, index):
    if index < 0 or index >= my_list['size'] + 1:
        raise IndexError("Index out of bounds")
    new_node = {'info': element, 'next': None}
    if index == 0:
        new_node['next'] = my_list['first']
        my_list['first'] = new_node
        if my_list['size'] == 0:
            my_list['last'] = new_node
    else:
        current_node = my_list['first']
        for _ in range(1, index - 1):
            current_node = current_node['next']
        new_node['next'] = current_node['next']
        current_node['next'] = new_node
        if new_node['next'] is None:
            my_list['last'] = new_node
    my_list['size'] += 1
    return my_list

def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list['size']:
        raise IndexError("Index out of bounds")
    if pos == 0:
        removed_element = my_list['first']['info']
        my_list['first'] = my_list['first']['next']
        if my_list['size'] == 1:
            my_list['last'] = None
    else:
        current_node = my_list['first']
        for _ in range(1, pos):
            current_node = current_node['next']
        removed_element = current_node['next']['info']
        current_node['next'] = current_node['next']['next']
        if current_node['next'] is None:
            my_list['last'] = current_node
    my_list['size'] -= 1
    return my_list

def change_info(my_list, pos, new_element):
    if pos < 0 or pos >= my_list['size']:
        raise IndexError("Index out of bounds")
    current_node = my_list['first']
    for _ in range(pos):
        current_node = current_node['next']
    current_node['info'] = new_element
    return my_list

def exchange(my_list, pos_1, pos_2):
    if pos_1 < 0 or pos_1 >= my_list['size'] or pos_2 < 0 or pos_2 >= my_list['size']:
        raise IndexError("Index out of bounds")
    if pos_1 == pos_2:
        return my_list
    node1 = my_list['first']
    for _ in range(pos_1):
        node1 = node1['next']
    node2 = my_list['first']
    for _ in range(pos_2):
        node2 = node2['next']
    node1['info'], node2['info'] = node2['info'], node1['info']
    return my_list

def sub_list(my_list,pos_i, num_elem):
    if pos_i < 0 or pos_i >= my_list['size'] or num_elem < 0 or (pos_i + num_elem) > my_list['size']:
        raise IndexError("Index out of bounds")
    sublist = new_list()
    current_node = my_list['first']
    for _ in range(pos_i):
        current_node = current_node['next']
    for _ in range(num_elem):
        add_last(sublist, current_node['info'])
        current_node = current_node['next']
    return sublist