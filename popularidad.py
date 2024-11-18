import ast
from libros import libros

def contar_popularidad_por_libro():
    lista_usuarios_no_formateada = []
    with open('datos.txt', 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()
            lista_usuarios_no_formateada.append(ast.literal_eval(linea))

    union_historiales_sistema = []
    for usuario in lista_usuarios_no_formateada:
        historial = usuario[4]
        if historial == 'None':
            historial = [None]
        else:
            historial = ast.literal_eval(historial)
        union_historiales_sistema = union_historiales_sistema + historial

    popularidad_por_libro = {}
    for i in range(1, len(libros) + 1):
        popularidad_por_libro[i] = union_historiales_sistema.count(i)

    lista_popularidad = list(popularidad_por_libro.items())
    for i in range(len(lista_popularidad)):
        for j in range(0, len(lista_popularidad) - 1 - i):
            if lista_popularidad[j][1] < lista_popularidad[j + 1][1]:
                lista_popularidad[j], lista_popularidad[j + 1] = lista_popularidad[j + 1], lista_popularidad[j]
    return lista_popularidad

# Tipo A: Misma popularidad
# Tipo B: Cercanía en popularidad
def buscar_adyacentes(lista, id_objetivo, tipo):
    popularidad_objetivo = None
    for tupla in lista:
        id_libro = tupla[0]
        if id_libro == id_objetivo:
            popularidad_objetivo = tupla[1]
    indice_objetivo = lista.index((id_objetivo, popularidad_objetivo))
    indice_menos_a_la_izquierda = None
    popularidad_maxima = None
    for i in range(indice_objetivo, -1, -1):
        if lista[i][1] != popularidad_objetivo and lista[i][1]:
            indice_menos_a_la_izquierda = i
            popularidad_maxima = lista[indice_menos_a_la_izquierda][1]
            break
    indice_menos_a_la_derecha = None
    popularidad_minima = None
    for i in range(indice_objetivo, len(lista)):
        if lista[i][1] != popularidad_objetivo and lista[i][1]:
            indice_menos_a_la_derecha = i
            popularidad_minima = lista[indice_menos_a_la_derecha][1]
            break
    adyacentes = []
    for tupla in lista:
        id_libro = tupla[0]
        popularidad = tupla[1]
        if popularidad == popularidad_objetivo and id_libro != id_objetivo and tipo == 'A':
            adyacentes.append(id_libro)
        elif indice_menos_a_la_izquierda is not None:
            if popularidad == popularidad_maxima and tipo == 'B':
                adyacentes.append(id_libro)
                continue
            if popularidad == popularidad_minima and tipo == 'B':
                adyacentes.append(id_libro)
                continue
    return adyacentes
