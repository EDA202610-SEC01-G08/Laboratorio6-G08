import random
from DataStructures.List import array_list as al
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf


def new_map(num_elements, load_factor, prime=109345121):
    """
    Crea un nuevo mapa vacío.
    """
    capacity = mf.next_prime(int(num_elements // load_factor))
    scale = 1 # random.randint(1, prime - 1)
    shift = 0 # random.randint(0, prime - 1)

    table = al.new_list()
    for i in range(capacity):
        table = al.add_last(table, me.new_map_entry(None, None))
    size = 0
    new_map = {"prime": prime, 
               "capacity": capacity, 
               "scale": scale, 
               "shift": shift, 
               "table": table, 
               "current_factor": 0, 
               "limit_factor": load_factor, 
               "size": size}
    return new_map

def put(my_map, key, value):
    """
    Agrega un nuevo par llave-valor al mapa. Si la llave ya existe, se actualiza su valor.

    """
    hash = mf.hash_value(my_map, key)
    slot = find_slot(my_map, key, hash)
    if slot[0]:  # Si la llave ya existe, actualizamos su valor
        my_map["table"] = al.change_info(my_map["table"], slot[1] + 1, me.set_value(al.get_element(my_map["table"], slot[1] + 1), value))
    else:  # Si la llave no existe, la agregamos al mapa
        my_map["table"] = al.change_info(my_map["table"], slot[1] + 1, me.new_map_entry(key, value))
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        if my_map["current_factor"] > my_map["limit_factor"]:
            rehash(my_map)
    return my_map

def find_slot(my_map, key, hash_value):
    """
    Busca la posición en la tabla donde se debe insertar/encontrar una entrada con una llave dada. Retorna tupla (encontrado, posición).
    """
    for i in range(my_map["capacity"]):
        pos = (hash_value + i) % my_map["capacity"]
        if is_available(my_map["table"], pos):
            return (False, pos)
        elif me.get_key(al.get_element(my_map["table"], pos + 1)) == key:
            return (True, pos)
    return (False, -1)  # Si no se encuentra un slot disponible después de recorrer toda la tabla

def is_available(table, pos):
    return me.get_key(al.get_element(table, pos + 1)) is None or me.get_key(al.get_element(table, pos + 1)) == "__EMPTY__"

def rehash(my_map):
    """
    Realiza un rehash de la tabla de simbolos. Crea nueva tabla con capacity que es el siguiente primo mayor a 2*capacity, y reinsertar todas las entradas de la tabla antigua en la nueva tabla. Retorna la nueva tabla.
    """
    old_table = my_map["table"]
    new_capacity = mf.next_prime(2 * my_map["capacity"])
    new_table = al.new_list()
    for i in range(new_capacity):
        new_table = al.add_last(new_table, me.new_map_entry(None, None))
    my_map["capacity"] = new_capacity
    my_map["table"] = new_table
    my_map["size"] = 0
    for i in range(al.size(old_table)):
        entry = al.get_element(old_table, i + 1)
        if me.get_key(entry) is not None and me.get_key(entry) != "__EMPTY__":
            # Reinserting directly into the new table
            hash_value = mf.hash_value(my_map, me.get_key(entry))
            for j in range(my_map["capacity"]):
                pos = (hash_value + j) % my_map["capacity"]
                if is_available(my_map["table"], pos):
                    # Adjusting for 1-based indexing
                    my_map["table"] = al.change_info(my_map["table"], pos + 1, me.new_map_entry(me.get_key(entry), me.get_value(entry)))
                    my_map["size"] += 1
                    break
    return my_map

def default_compare(key, entry):
    if key == me.get_key(entry):
        return 0
    elif key < me.get_key(entry):
        return -1
    else:
        return 1
    
def contains(my_map, key):
    """
    Retorna True si la llave existe en el mapa, False en caso contrario.
    """
    hash = mf.hash_value(my_map, key)
    slot = find_slot(my_map, key, hash)
    return slot[0]

def remove(my_map, key):
    """
    Elimina la entrada con la llave dada del mapa. Reemplaza la entrada eliminada con una entrada vacía (key = "__EMPTY__", value = "__EMPTY__")
    Retorna la tabla actualizada.
    """
    hash = mf.hash_value(my_map, key)
    slot = find_slot(my_map, key, hash)
    if slot[0]:  # Si la llave existe, la eliminamos
        removed_entry = al.get_element(my_map["table"], slot[1] + 1)
        my_map["table"] = al.change_info(my_map["table"], slot[1] + 1, me.set_key(al.get_element(my_map["table"], slot[1] + 1), "__EMPTY__"))
        my_map["table"] = al.change_info(my_map["table"], slot[1] + 1, me.set_value(al.get_element(my_map["table"], slot[1] + 1), "__EMPTY__"))
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
    return my_map

def get(my_map, key):
    """
    Retorna el valor asociado a la llave dada. Si la llave no existe, retorna None.
    """
    hash = mf.hash_value(my_map, key)
    slot = find_slot(my_map, key, hash)
    if slot[0]:  # Si la llave existe, retornamos su valor
        return me.get_value(al.get_element(my_map["table"], slot[1] + 1))
    else:  # Si la llave no existe, retornamos None
        return None
    
def size(my_map):
    """
    Retorna el número de entradas en el mapa.
    """
    return my_map["size"]

def is_empty(my_map):
    """
    Retorna True si el mapa está vacío, False en caso contrario.
    """
    return my_map["size"] == 0

def key_set(my_map):
    """
    Retorna una lista con todas las llaves del mapa.
    """
    keys = al.new_list()
    for i in range(al.size(my_map["table"])):
        entry = al.get_element(my_map["table"], i + 1)
        if me.get_key(entry) is not None and me.get_key(entry) != "__EMPTY__":
            keys = al.add_last(keys, me.get_key(entry))
    return keys

def value_set(my_map):
    """
    Retorna una lista con todos los valores del mapa.
    """
    values = al.new_list()
    for i in range(al.size(my_map["table"])):
        entry = al.get_element(my_map["table"], i + 1)
        if me.get_key(entry) is not None and me.get_key(entry) != "__EMPTY__":
            values = al.add_last(values, me.get_value(entry))
    return values
