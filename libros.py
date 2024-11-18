import os
from termcolor import colored

def leer_libros():
    os.system('cls' if os.name == 'nt' else 'clear')
    libros = []
    with open('libros.txt', 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip().replace('[', '').replace(']','').replace('\'','').split(', ')
            id, titulo, autor1, autor2, autor3, año, materia = linea
            id = int(id)
            año = int(año)
            libros.append([id, titulo, autor1, autor2, autor3, año, materia])
    return libros

def añadir_libro(titulo, autor1, autor2, autor3, año, materia):
    os.system('cls' if os.name == 'nt' else 'clear')
    libros = leer_libros()
    id = len(libros) + 1
    if isinstance(titulo, str) and isinstance(autor1, str) and isinstance(autor2, str) and isinstance(autor3, str) and isinstance(año, int) and isinstance(materia, str):
        with open('libros.txt', 'a', encoding='utf-8') as archivo:
            archivo.write(f"\n[{id}, '{titulo}', '{autor1}', '{autor2}', '{autor3}', {año}, '{materia}']")
        print(colored('El libro ha sido agregado exitósamente (+)', 'green'))
        input(colored('Presiona ENTER para continuar', 'green'))
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()
    else:
        print(colored('Error: Tipo de dato inválido en la operación! La operación ha sido cancelada', 'red'))
        input(colored('Presiona ENTER para continuar', 'red'))
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()

def desactivar_libro(id):
    libros = leer_libros()
    os.system('cls' if os.name == 'nt' else 'clear')
    if 1 <= int(id) <= len(libros):
        id_libros_desactivados_actuales = []
        with open('libros_desactivados.txt', 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                id_libros_desactivados_actuales.append(int(linea.strip()))
            for id_de_libro in id_libros_desactivados_actuales:
                if str(id) == str(id_de_libro):
                    print(colored(f'Error: El libro con id {str(id)} ya se encuentra desactivado! La operación ha sido cancelada', 'red'))
                    input(colored('Presiona ENTER para continuar', 'red'))
                    os.system('cls' if os.name == 'nt' else 'clear')
                    exit()
        with open('libros_desactivados.txt', 'a', encoding='utf-8') as archivo:
                archivo.write(f"{id}\n")
        print(colored(f'El libro con id {str(id)} ha sido desactivado exitósamente (-)', 'green'))
        input(colored('Presiona ENTER para continuar', 'green'))
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()
    else:
        print(colored(f'Error: No existe libro con id {str(id)} ! La operación ha sido cancelada', 'red'))
        input(colored('Presiona ENTER para continuar', 'red'))
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()

def reactivar_libro(id):
    libros = leer_libros()
    os.system('cls' if os.name == 'nt' else 'clear')
    if 1 <= int(id) <= len(libros):
        id_libros_desactivados_actuales = []
        with open('libros_desactivados.txt', 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                id_libros_desactivados_actuales.append(int(linea.strip()))
        actualizar_id_libros_desactivados = []
        for id_de_libro in id_libros_desactivados_actuales:
            if str(id) != str(id_de_libro):
                actualizar_id_libros_desactivados.append(int(id_de_libro))
        with open('libros_desactivados.txt', 'w', encoding='utf-8') as archivo:
            for id_libro in actualizar_id_libros_desactivados:
                archivo.write(f"{id_libro}\n")
        if str(id) in id_libros_desactivados_actuales:
            print(colored(f'El libro con id {str(id)} ha sido reactivado exitósamente (+)', 'green'))
            input(colored('Presiona ENTER para continuar', 'green'))
            os.system('cls' if os.name == 'nt' else 'clear')
            exit()
        else:
            print(colored(f'Error: El libro con id {str(id)} no se encuentra desactivado', 'red'))
            input(colored('Presiona ENTER para continuar', 'red'))
            os.system('cls' if os.name == 'nt' else 'clear')
            exit()
    else:
        print(colored(f'Error: No existe libro con id {str(id)}! La operación ha sido cancelada', 'red'))
        input(colored('Presiona ENTER para continuar', 'red'))
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()

libros = leer_libros()