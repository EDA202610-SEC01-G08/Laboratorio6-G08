import random
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as slt
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf


def new_map(num_elements, load_factor, prime=109345121):
    """
    Crea una nueva tabla de hash con manejo de colisiones por Separate Chaining.
    Cada posición de la tabla contiene una single_linked_list donde se encadenan
    las entradas que colisionan en ese índice.
    La capacidad inicial es el primo siguiente a num_elements / load_factor.
    """
    capacity = mf.next_prime(int(num_elements / load_factor))

    my_table = {
        'prime': prime,
        'capacity': capacity,
        'scale': random.randint(1, prime - 1),
        'shift': random.randint(0, prime - 1),
        'table': None,
        'current_factor': 0,
        'limit_factor': load_factor,
        'size': 0
    }

    # Cada slot del array_list es una single_linked_list vacía
    table = lt.new_list()
    for _ in range(capacity):
        chain = slt.new_list()
        lt.add_last(table, chain)

    my_table['table'] = table
    return my_table


#  Función auxiliar de comparación

def default_compare(key, entry):
    """
    Compara key con la llave de entry.
    Retorna 0 si iguales, 1 si key > entry.key, -1 si key < entry.key.
    """
    entry_key = me.get_key(entry)
    if key == entry_key:
        return 0
    elif key > entry_key:
        return 1
    return -1


#  Operaciones principales del TAD Map

def put(my_map, key, value):
    """
    Inserta o actualiza la pareja key-value en la tabla.
    Si la llave ya existe en la cadena, actualiza su valor.
    Si no existe, agrega una nueva entrada al final de la cadena.
    Si current_factor supera limit_factor, hace rehash.
    """
    hash_val = mf.hash_value(my_map, key)
    chain = lt.get_element(my_map['table'], hash_val)

    # Buscar si la llave ya existe en la cadena
    current = chain['first']
    found = False
    while current is not None:
        entry = current['info']
        if default_compare(key, entry) == 0:
            # Actualizar el value existente
            me.set_value(entry, value)
            found = True
            break
        current = current['next']

    if not found:
        # Agregar nueva entrada al final de la cadena
        new_entry = me.new_map_entry(key, value)
        slt.add_last(chain, new_entry)
        my_map['size'] += 1
        my_map['current_factor'] = my_map['size'] / my_map['capacity']

    # Rehash si se supera el factor de carga límite
    if my_map['current_factor'] > my_map['limit_factor']:
        my_map = rehash(my_map)

    return my_map


def contains(my_map, key):
    """
    Retorna True si key existe en la tabla, False si no.
    """
    hash_val = mf.hash_value(my_map, key)
    chain = lt.get_element(my_map['table'], hash_val)

    current = chain['first']
    while current is not None:
        entry = current['info']
        if default_compare(key, entry) == 0:
            return True
        current = current['next']
    return False


def get(my_map, key):
    """
    Retorna el value asociado a key. Si no existe, retorna None.
    """
    hash_val = mf.hash_value(my_map, key)
    chain = lt.get_element(my_map['table'], hash_val)

    current = chain['first']
    while current is not None:
        entry = current['info']
        if default_compare(key, entry) == 0:
            return me.get_value(entry)
        current = current['next']
    return None


def remove(my_map, key):
    """
    Elimina la entrada asociada a key de la cadena correspondiente.
    Actualiza size y current_factor si la llave existía.
    """
    hash_val = mf.hash_value(my_map, key)
    chain = lt.get_element(my_map['table'], hash_val)

    # Recorrer la cadena buscando la llave
    pos = 1
    current = chain['first']
    while current is not None:
        entry = current['info']
        if default_compare(key, entry) == 0:
            slt.remove_element(chain, pos)
            my_map['size'] -= 1
            my_map['current_factor'] = my_map['size'] / my_map['capacity']
            break
        current = current['next']
        pos += 1

    return my_map


def size(my_map):
    """
    Retorna el número de parejas key-value en la tabla.
    """
    return my_map['size']


def is_empty(my_map):
    """
    Retorna True si la tabla está vacía.
    """
    return my_map['size'] == 0


def key_set(my_map):
    """
    Retorna un array_list con todas las llaves de la tabla.
    """
    keys = lt.new_list()
    capacity = my_map['capacity']
    for i in range(capacity):
        chain = lt.get_element(my_map['table'], i)
        current = chain['first']
        while current is not None:
            entry = current['info']
            lt.add_last(keys, me.get_key(entry))
            current = current['next']
    return keys


def value_set(my_map):
    """
    Retorna un array_list con todos los values de la tabla.
    """
    values = lt.new_list()
    capacity = my_map['capacity']
    for i in range(capacity):
        chain = lt.get_element(my_map['table'], i)
        current = chain['first']
        while current is not None:
            entry = current['info']
            lt.add_last(values, me.get_value(entry))
            current = current['next']
    return values


def rehash(my_map):
    """
    Crea una nueva tabla con capacidad = primo siguiente al doble de la actual
    y reinsertan todos los elementos existentes.
    Actualiza el mapa en su lugar para reflejar los cambios.
    """
    old_table = my_map['table']
    old_capacity = my_map['capacity']
    
    new_capacity = mf.next_prime(my_map['capacity'] * 2 + 1)
    
    # Crear nueva tabla vacía con la nueva capacidad
    new_table = lt.new_list()
    for _ in range(new_capacity):
        chain = slt.new_list()
        lt.add_last(new_table, chain)
    
    # Actualizar propiedades del mapa
    my_map['capacity'] = new_capacity
    my_map['table'] = new_table
    my_map['size'] = 0
    my_map['current_factor'] = 0
    
    # Reinsertar todos los elementos de cada cadena de la tabla vieja
    for i in range(old_capacity):
        chain = lt.get_element(old_table, i + 1)
        current = chain['first']
        while current is not None:
            entry = current['info']
            put(my_map, me.get_key(entry), me.get_value(entry))
            current = current['next']
    
    return my_map