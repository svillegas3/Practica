import os
import ast
import re
import random

from usuario import Usuario
from libros import libros as LB
from termcolor import colored
from grafos_libreria_propia import G, explorar_grafo, mostrar_grafo
from popularidad import contar_popularidad_por_libro

def mostrar_pagina_A():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colored('Selecciona una opción:', 'yellow'))
        print(colored('1. Crear cuenta', 'green'))
        print(colored('2. Iniciar sesión', 'green'))
        print(colored('3. Salir', 'green'))
        opcion = input(colored('Input: ', 'yellow'))
        if opcion == '1':
            crear_cuenta()
        elif opcion == '2':
            iniciar_sesion()
        elif opcion == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            exit()
        else:
            print()
            print(colored('Error: Ingresa solo opciones del menú!', 'red'))
            input(colored('Presiona ENTER para continuar', 'red'))

def mostrar_pagina_B(usuario):
    while True:
        historial_nuevo = str(usuario.historial)
        libro_actual_nuevo = str(usuario.libro_actual)
        datos=[]
        file_path = 'datos.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            for linea in file:
                linea = linea.strip()
                datos.append(ast.literal_eval(linea))
        datos_nuevos = []
        for info in datos:
            if usuario.usuario != info[2]:
                datos_nuevos.append(info)
            else:
                temp = []
                temp.append(usuario.nombre)
                temp.append(usuario.apellido)
                temp.append(usuario.usuario)
                temp.append(usuario.contraseña)
                temp.append(historial_nuevo)
                temp.append(libro_actual_nuevo)
                datos_nuevos.append(temp)
        with open(file_path, 'w', encoding='utf-8') as file:
            for linea in datos_nuevos:
                file.write(f'{str(linea)}\n')
        datos=[]
        file_path = 'flag.txt'
        with open(file_path, 'r', encoding='utf-8') as file:
            for linea in file:
                linea = linea.strip()
                datos.append(ast.literal_eval(linea))
        datos_nuevos = []
        for info in datos:
            if usuario.usuario != info[2]:
                datos_nuevos.append(info)
            else:
                temp = []
                temp.append(usuario.nombre)
                temp.append(usuario.apellido)
                temp.append(usuario.usuario)
                temp.append(usuario.contraseña)
                temp.append(historial_nuevo)
                temp.append(libro_actual_nuevo)
                datos_nuevos.append(temp)
        with open(file_path, 'w', encoding='utf-8') as file:
            for linea in datos_nuevos:
                file.write(f'{str(linea)}\n')

        os.system('cls' if os.name == 'nt' else 'clear')
        print(colored(f'Bienvenid@, {usuario.nombre}', 'green')) 
        if usuario.libro_actual is not None:
            print(colored(f'Recuerda devolver este libro: {usuario.libro_actual}', 'red'))
        print(colored('Selecciona una opción:', 'yellow'))
        print(colored('1. Buscar libros', 'yellow'))
        print(colored('2. Devolver libro actual', 'yellow'))
        print(colored('3. Ver mi historial de libros', 'yellow'))
        print(colored('4. Salir', 'yellow'))
        print(colored('5. Cerrar Sesión', 'yellow'))
        opcion = input(colored('Input: ', 'green'))
        print()
        if opcion == '1':
            if usuario.libro_actual is not None:
                print(colored('Error: Devuelve el libro que tienes antes de pedir otro!', 'red'))
                input(colored('Presiona ENTER para continuar', 'red'))
                continue
            buscar_libros(usuario)
        elif opcion == '2':
            if usuario.libro_actual is None:
                print(colored('Error: No has pedido ningún libro!', 'red'))
                input(colored('Presiona ENTER para continuar', 'red'))
                continue
            devolver_libro(usuario)
        elif opcion == '3':
            ver_historial(usuario)
        elif opcion == '5':
            file_path = 'flag.txt'
            os.remove(file_path)
            mostrar_pagina_A()
        elif opcion == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            exit()
        else:
            print(colored('Error: Ingresa solo opciones del menú!', 'red'))
            input(colored('Presiona ENTER para continuar', 'red'))
            continue

def crear_cuenta():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colored('Completa este formulario, en el cual llenarás:', 'yellow'))
        print(colored(' - Nombre/s', 'yellow'))
        print(colored(' - Apellido/s', 'yellow'))
        print(colored(' - Usuario', 'yellow'))
        print(colored(' - Contraseña', 'yellow'))
        nombre = input(colored('Nombre: ', 'green'))
        apellido = input(colored('Apellido: ', 'green'))
        usuario = input(colored('Usuario: ', 'green'))
        contraseña = input(colored('Contraseña: ', 'green'))
        confirmar_contraseña = input(colored('Confirmar contraseña: ', 'green'))

        print()
        if contraseña != confirmar_contraseña:
            print(colored('Error detectado: Las contraseñas no coinciden!', 'red'))
            input(colored('Presiona ENTER para continuar', 'red'))
            continue
        file_path = 'datos.txt'
        if not os.path.exists(file_path):
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(f'["{nombre}", "{apellido}", "{usuario}", "{contraseña}", "{None}", "{None}"]\n')
        else:
            datos = []
            with open(file_path, 'r', encoding='utf-8') as file:
                for linea in file:
                    linea = linea.strip()
                    datos.append(ast.literal_eval(linea))
            usuario_existe = any(info[2] == usuario for info in datos)
            if usuario_existe:
                print(colored('Error detectado: Ese usuario ya esta registrado!', 'red'))
                input(colored('Presiona ENTER para continuar', 'red'))
                continue
            if not re.fullmatch(r'^.{3,40}$', contraseña):
                print(colored('Error detectado: La contraseña debe tener entre 3 y 40 caracteres!', 'red'))
                input(colored('Presiona ENTER para continuar', 'red'))
                continue
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(f'["{nombre}", "{apellido}", "{usuario}", "{contraseña}", "{None}", "{None}"]\n')
            print(colored('Tu cuenta ha sido creada exitósamente', 'green'))
            input(colored('Presiona ENTER para continuar', 'green'))
        break
    mostrar_pagina_A()

def iniciar_sesion():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colored('En este menú, puedes usar CTRL+C para volver a la pantalla anterior', 'red'))
        print(colored('Ingresarás los siguientes datos: ', 'yellow'))
        print(colored(' - Usuario ', 'yellow'))
        print(colored(' - Contraseña ', 'yellow'))
        try:
            usuario = input(colored('Usuario: ', 'green'))
            contraseña = input(colored('Contraseña: ', 'green'))
        except KeyboardInterrupt:
            mostrar_pagina_A()
        print()

        file_path = 'datos.txt'
        datos = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for linea in file:
                linea = linea.strip()
                datos.append(ast.literal_eval(linea))
        for info in datos:
            if usuario == info[2] and contraseña == info[3]:
                nombre = info[0]
                apellido = info[1]
                historial = info[4]
                libro_actual = info[5]
                file_path = 'flag.txt'
                with open(file_path, 'a', encoding='utf-8') as file:
                    file.write(f'["{nombre}", "{apellido}", "{usuario}", "{contraseña}", "{historial}", "{libro_actual}"]')

                if historial == 'None':
                    historial = []
                else:
                    historial = ast.literal_eval(historial)
                if libro_actual == 'None':
                    libro_actual = None
                else:
                    libro_actual = int(libro_actual)
                logear_usuario = Usuario(nombre, apellido, usuario, contraseña, historial, libro_actual)
                print(colored('Has iniciado sesión exitosamente', 'green'))
                input(colored('Presiona ENTER para continuar', 'green'))
                mostrar_pagina_B(logear_usuario)
        print(colored('Error: Usuario o contraseña incorrectos!', 'red'))
        input(colored('Presiona ENTER para continuar', 'red'))

def buscar_libros(usuario):
    id_libros_desactivados_actuales = []
    lista_popularidad = contar_popularidad_por_libro()

    with open('libros_desactivados.txt', 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            id_libros_desactivados_actuales.append(int(linea.strip()))
    os.system('cls' if os.name == 'nt' else 'clear')

    if usuario.libro_actual is None and usuario.historial != []:
        print(colored('Tu último libro leído es: ', 'yellow'))
        for libro in LB:
            if libro[0] == usuario.historial[-1]:
                print(colored(f'\tID: {libro[0]}, Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}', 'green'))

    if usuario.historial == []:
        print(colored('Veo que eres nuevo. Puedes probar algunos de estos libros: ', 'green'))
        lista_libros = LB
        for libro_popularidad in lista_popularidad:
            _, popularidad = libro_popularidad
            for libro in lista_libros:
                if libro[0] == libro_popularidad[0]:
                    if libro[0] not in id_libros_desactivados_actuales:
                        print(colored(f'    ID: {libro[0]}, Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}. Popularidad: {popularidad}', 'yellow'))

    elif usuario.historial is not None:
        print(colored('Libros recomendados: ', 'yellow'))
        tabla = explorar_grafo(G, usuario.historial[-1])
        for libro_objetivo in tabla:
            for libro in LB:
                if libro_objetivo == libro[0] and libro[0] not in id_libros_desactivados_actuales:
                    popularidad = None
                    for libro_popularidad in lista_popularidad:
                        id_asociada = libro_popularidad[0]
                        if libro_objetivo == id_asociada:
                            popularidad = libro_popularidad[1]
                            break
                    print(colored(f'    ID: {libro[0]}, Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}. Popularidad: {popularidad}', 'yellow'))
        for libro in LB:
            if libro[0] not in tabla and libro[0] not in id_libros_desactivados_actuales:
                popularidad = None
                for libro_popularidad in lista_popularidad:
                    id_asociada = libro_popularidad[0]
                    if libro_objetivo == id_asociada:
                        popularidad = libro_popularidad[1]
                        break
                print(colored(f'    ID: {libro[0]}, Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}. Popularidad: {popularidad}', 'yellow'))

    mostrar_grafo(G)
    respuesta = input(colored('¿Quiéres escoger un libro? (y/n): ', 'green')).lower()
    if respuesta == 'n':
        mostrar_pagina_B(usuario)
    elif respuesta != 'y':
        print()
        print(colored('Error: Ingresa solo opciones del menú!', 'red'))
        input(colored('Presiona ENTER para continuar', 'red'))
        buscar_libros(usuario)

    try:
        id_libro_escogido = int(input(colored("Ingresa la id del libro: ", 'green')))
        if id_libro_escogido <= 0 or id_libro_escogido > len(LB):
            print()
            print(colored('Error: Ingresa solo ids posibles/existentes!', 'red'))
            input(colored('Presiona ENTER para continuar', 'red'))
            buscar_libros(usuario)
        usuario.libro_actual = id_libro_escogido
        mostrar_pagina_B(usuario)
    except ValueError:
        print()
        print(colored('Error: Ingresa solo ids posibles/existentes!', 'red'))
        input(colored('Presiona ENTER para continuar', 'red'))
        buscar_libros(usuario)

def devolver_libro(usuario):
    if usuario.libro_actual is not None:
        usuario.historial.insert(len(usuario.historial), usuario.libro_actual)
        usuario.libro_actual = None

def ver_historial(usuario):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colored('Historial: ', 'green'))
    if usuario.historial is not None:
        for index, id_libro in enumerate(usuario.historial):
            for libro in LB:
                if id_libro == libro[0]:
                    print(colored(f'{"\t" * (index + 1)}Título: {libro[1]}. Autores: {libro[2]}, {libro[3]}, {libro[4]}. Año: {libro[5]}. Materia: {libro[6]}', 'yellow'))
    input(colored('Presiona ENTER para regresar', 'green'))

def main():

    os.system('cls' if os.name == 'nt' else 'clear')
    file_path = 'flag.txt'
    if not os.path.exists(file_path):
        mostrar_pagina_A()
    else:
        datos = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for linea in file:
                linea = linea.strip()
                datos.append(ast.literal_eval(linea))
        usuario_actual = datos[0]
        nombre = usuario_actual[0]
        apellido = usuario_actual[1]
        usuario = usuario_actual[2]
        contraseña = usuario_actual[3]
        historial = usuario_actual[4]
        libro_actual = usuario_actual[5]
        if historial == 'None':
            historial = []
        else:
            historial = ast.literal_eval(historial)
        if libro_actual == 'None':
            libro_actual = None
        else:
            libro_actual = int(libro_actual)
        logear_usuario = Usuario(nombre, apellido, usuario, contraseña, historial, libro_actual)
        mostrar_pagina_B(logear_usuario)





main()