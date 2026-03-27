"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones
 *
 * Dario Correal
 """

import sys
import App.logic as logic
# TODO Realice la importación del mapa linear probing
from DataStructures import map as mp
# TODO Realice la importación de ArrayList como estructura de datos auxiliar para sus requerimientos
from DataStructures import arraylist as al

"""
La vista se encarga de la interacción con el usuario
Presenta el menú de opciones y por cada selección
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
#  -------------------------------------------------------------
# Funciones para la carga de datos
#  -------------------------------------------------------------

def new_logic():
    """
    Se crea una instancia del controlador
    """
    control = logic.new_logic()
    return control

# TODO Incluir las mediciones de tiempo y uso de memoria en la ejecución de la consulta.
def load_data(control):
    """
    Solicita a la controlador que cargue los datos
    """
    delta_time, delta_memory, (books, authors, tags, book_tags) = logic.load_data(control)
    print(f"Tiempo de carga: {delta_time:.2f} ms")
    print(f"Memoria utilizada: {delta_memory:.2f} kB")
    return books, authors, tags, book_tags

#  -------------------------------------------------------------
# Funciones para la correcta impresión de los datos
#  -------------------------------------------------------------

def print_menu():
    """
    Menu de usuario
    """
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar la información de un libro según su id")
    print("3- Consultar los libros de un autor")
    print("4- Consultar los libros según un género dado")
    print("5- Consultar los libros de un autor para un año de publicación especifico")
    print("8- Salir")

def print_book_info(book):
    """
    Imprime los mejores libros solicitados
    """
    if book:
        print('Titulo: ' + book['title'] + '  ISBN: ' +
                  book['isbn'] + ' Rating: ' + book['average_rating'] +
                    ' Work text reviews count : ' + book['work_text_reviews_count'])
    else:
        print('No se encontraron libros')

def print_books_by_author(author, books_by_author):
    """
    Recorre la lista de libros de un autor, imprimiendo
    la información solicitada.
    """
    if books_by_author:
        print(f"Para el autor {author} se encontraron los siguientes libros: " )
        for book_pos in range(0, al.size(books_by_author)):
            book = al.get_element(books_by_author, book_pos)
            print('Titulo: ' + book['title'] + '  ISBN: ' +
                  book['isbn'] + ' Rating: ' + book['average_rating'] +
                    ' Work text reviews count : ' + book['work_text_reviews_count'])
    else:
        print("No se encontró el autor")

def print_books_by_tag(tag_name, books_by_tag):
    """
    Recorre la lista de libros asociados a un tag, imprimiendo
    la información solicitada.
    """
    if books_by_tag:
        print("Tag encontrado: " + tag_name)
        for book_pos in range(0, al.size(books_by_tag)):
            book = al.get_element(books_by_tag, book_pos)
            print('Titulo: ' + book['title'] + '  ISBN: ' +
                  book['isbn'] + ' Rating: ' + book['average_rating'] +
                    ' Work text reviews count : ' + book['work_text_reviews_count'])
    else:
        print("No se encontró el tag") 
        
def print_books_by_auth_year(author, pub_year, books_by_author_year, tiempo_transcurrido, memoria_usada):
    """
    Recorre la lista de libros de un autor para un año de publicación específico, 
    imprimiendo la información solicitada junto con las métricas de rendimiento.
    """
    if books_by_author_year:
        print(f"Para el autor {author}, se encontraron los siguientes libros publicados en el año {pub_year}:")
        for book_pos in range(0, al.size(books_by_author_year)):
            book = al.get_element(books_by_author_year, book_pos)
            print(f"Titulo: {book['title']}  ISBN: {book['isbn']}  Rating: {book['average_rating']}  "
                  f"Work text reviews count: {book['work_text_reviews_count']}")
    else:
        print("No se encontró el autor o el tag")
    
    # Imprimir métricas de rendimiento
    print(f"\nTiempo transcurrido: {tiempo_transcurrido:.2f} ms")
    print(f"Memoria utilizada: {memoria_usada:.2f} kB\n")

     
exit_opt_lt = ("s", "S", "1", True, "true", "True", "si", "Si", "SI")


# main del ejercicio
def main():
    """
    Menú principal
    """
    # bandera para controlar el ciclo del menu
    working = True
    control = new_logic()


    # ciclo del menu
    while working:
        print_menu()
        inputs = input("Seleccione una opción para continuar\n")
        # TODO agregar tiempo de ejecución y consumo de memoria
        if int(inputs[0]) == 1:
            print("Cargando información de los archivos ....")
            bk, at, tg, bktg = load_data(control)
            print('Libros cargados: ' + str(bk))
            print('Autores cargados: ' + str(at))
            print('Géneros cargados: ' + str(tg))
            print('Asociación de Géneros a Libros cargados: ' +
                  str(bktg))

        elif int(inputs[0]) == 2:
            number = input("Ingrese el id del libro (good_read_book_id) que desea buscar: ")
            book = logic.get_book_info_by_book_id(control, number)
            print_book_info(book)

        elif int(inputs[0]) == 3:
            authorname = input("Nombre del autor a buscar: ")
            author, author_book_list = logic.get_books_by_author(control, authorname)
            print_books_by_author(author,author_book_list)

        elif int(inputs[0]) == 4:
            label = input("Etiqueta a buscar: ")
            book_list_by_tag = logic.get_books_by_tag(control, label)
            print_books_by_tag(label, book_list_by_tag)
                 
        elif int(inputs[0]) == 5:
            author_name = input("Ingrese el nombre del autor que desea buscar:\n")
            pub_year = input("Ingrese la fecha de publicación que desea buscar:\n") 

            books_by_author_pub_year, tiempo_transcurrido, memoria_usada = logic.get_books_by_author_pub_year(control, author_name, pub_year)

            print_books_by_auth_year(author_name, pub_year, books_by_author_pub_year, tiempo_transcurrido, memoria_usada)

            
        elif int(inputs[0]) == 8:
            # confirmar salida del programa
            end_str = "¿Desea salir del programa? (s/n): "
            opt_usr = input(end_str)
            # diferentes opciones de salida
            if opt_usr in exit_opt_lt:
                working = False
                print("\nGracias por utilizar el programa.")

        else:
            continue
    sys.exit(0)