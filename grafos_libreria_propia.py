# Importo las librerías necesarias y también algunas variables de otros scripts
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from libros import libros
from gramatica import mapa_esp_ascii, articulos, preposiciones, pronombres, conjunciones, adverbios, interrogativas
from popularidad import contar_popularidad_por_libro, buscar_adyacentes

# Creamos el grafo no dirigido
G = nx.MultiGraph()

# Añadimos los nodos al grafo
V = set()
for libro in libros:
    id_libro = libro[0]
    V.add(id_libro)
    G.add_node(id_libro)

# Clasificación 1 (Rojo): Crear un 'camino' (relación) entre dos libros si son de la misma materia
E1 = []
for i in range(len(libros)):
    for j in range(i + 1, len(libros)):
        id_libro1 = libros[i][0]
        id_libro2 = libros[j][0]
        materia_libro1 = libros[i][6]
        materia_libro2 = libros[j][6]
        if materia_libro1 == materia_libro2:
            E1.append((id_libro1, id_libro2))
            G.add_edge(id_libro1, id_libro2, color='red')

# Clasificación 2 (Azul): Crear un 'camino' (relación) entre dos libros, uno para cada autor que compartan en común
E2 = []
for i in range(len(libros)):
    for j in range(i + 1, len(libros)):
        id_libro1 = libros[i][0]
        id_libro2 = libros[j][0]
        autores_libro1 = set(libros[i][2:5])
        autores_libro2 = set(libros[j][2:5])
        interseccion_autores = autores_libro1 & autores_libro2
        for autores in interseccion_autores:
            E2.append((id_libro1, id_libro2))
            G.add_edge(id_libro1, id_libro2, color='blue')

# ***********************************************************************************************************************************************************************************************
# ***********************************************************************************************************************************************************************************************
# Antes de realizar la clasificación 3, quitamos las palabras irrelevantes de los títulos de los libros en una nueva lista de libros. Voy a explicar el paso a paso porque esta parte es compleja
libros_con_titulos_modificados = []
for libro in libros:
    id_libro = libro[0]
    titulo_original = libro[1]

    # Modificamos el título por primera vez (en este caso quitamos carácteres del Español y lo convertimos a ASCII)
    titulo_modificado = []
    for caracter in titulo_original:
        nuevo_caracter = mapa_esp_ascii.get(caracter, caracter)
        titulo_modificado.append(nuevo_caracter)
    # Si 'Hólá prófÉ' fuera un título, entonces hasta este momento tendríamos una lista titulo_modificado = ['H','o','l','a',' ','p','r','o','f','E']
    titulo_modificado = ''.join(titulo_modificado) # Esta función junta los elementos de la lista anterior, por lo que el título modificado quedaría en una cadena, en este ejemplo, 'Hola profE'
 
    # Modificamos el título por segunda vez (en este caso convertimos las mayúsculas en minúsculas)
    titulo_modificado = titulo_modificado.lower() # Esta función hace que los carácteres estén en minúscula, por ejemplo, 'Hola profE' -> 'hola profe'
    palabras = titulo_modificado.split() # Esta función separa, por ejemplo, 'hola profe', en ['hola', 'profe']
    
    # Modificamos el título por tercera vez (en este caso quitamos artículos y preposiciones)
    palabras_relevantes = []
    for palabra in palabras:
        if (palabra not in articulos) and (palabra not in preposiciones) and (palabra not in pronombres) and (palabra not in conjunciones) and (palabra not in adverbios) and (palabra not in interrogativas):
            palabras_relevantes.append(palabra) # Omitimos palabras que sean artículos y preposiciones, por ejemplo, ['la', 'casa', 'de', 'antioquia'] -> ['casa', 'antioquia']
    titulo_modificado = ' '.join(palabras_relevantes) # Juntamos los elementos de la lista anterior con un espacio (' ') de por medio en una cadena, por ejemplo ['casa', 'antioquia'] -> 'casa antioquia'
    libros_con_titulos_modificados.append((id_libro, titulo_modificado, *libro[2:]))
# ***********************************************************************************************************************************************************************************************
# ***********************************************************************************************************************************************************************************************

# Clasificación 3 (Verde): Crear un 'camino' (relación) entre dos libros por palabras similares en el título
E3 = []
for i in range(len(libros_con_titulos_modificados)):
    for j in range(i + 1, len(libros_con_titulos_modificados)):
        id_libro1 = libros_con_titulos_modificados[i][0]
        id_libro2 = libros_con_titulos_modificados[j][0]
        titulo1 = set(libros_con_titulos_modificados[i][1].split())
        titulo2 = set(libros_con_titulos_modificados[j][1].split())
        interseccion_palabras_en_titulos = titulo1 & titulo2
        for palabra in interseccion_palabras_en_titulos:
            E3.append((id_libro1, id_libro2))
            G.add_edge(id_libro1, id_libro2, color='green')

# Con estas dos funciones exploramos el grafo. Esto nos devuelve un string que reenzambla que recorrido se hizo y con qué prioridad en base a (1) cercanía y (2) número de caminos.
def explorar_grafo(G, nodo_inicial):
    explorado = []
    a_explorar = []
    orden_exploracion = []

    def explorar_nodo(nodo):
        explorado.append(nodo)

        if nodo in explorado and a_explorar:
            del a_explorar[0]
        
        vecinos = list(G.neighbors(nodo))
        vecinos_contar_caminos = {}
        for vecino in vecinos:
            key_caminos = list(G[nodo][vecino].keys())
            if key_caminos:
                vecinos_contar_caminos[vecino] = max(key_caminos)

        vecinos_ordenados = sorted(vecinos_contar_caminos, key=lambda x: (-vecinos_contar_caminos[x], np.random.rand()))

        vecinos_nuevos = []
        for vecino in vecinos_ordenados:
            if (vecino not in explorado) and (vecino not in a_explorar):
                vecinos_nuevos.append(vecino)

        if vecinos_nuevos:
            for i in vecinos_nuevos:
                orden_exploracion.append(i)
            a_explorar.extend(vecino for vecino in vecinos_nuevos)

        if len(a_explorar) == 0:
            return

        explorar_nodo(a_explorar[0])

    explorar_nodo(nodo_inicial)
    return orden_exploracion

# Clasificación 4 (Naranja y Negro): Crear un 'camino' (relación) entre dos libros si sus popularidades asociadas son adyacentes (negro == misma popularidad, naranja == cercana en 1 grado)
# los libros que son '1 grado' cercano a otro se refiere a que al ordenar los libros por su popularidad, este se encuentra adyacente a este
E4 = []
lista_popularidad = contar_popularidad_por_libro()
for i in range(len(libros)):
    for j in range(i + 1, len(libros)):
        id_libro1 = libros[i][0]
        id_libro2 = libros[j][0]
        # buscar
        for libro_popularidad in lista_popularidad:
            id_asociada = libro_popularidad[0]
            if id_asociada == id_libro1:
                popularidad_libro1 = libro_popularidad[1]
                break
        for libro_popularidad in lista_popularidad:
            id_asociada = libro_popularidad[0]
            if id_asociada == id_libro2:
                popularidad_libro2 = libro_popularidad[1]
                break
        adyacentes_tipoA = buscar_adyacentes(lista_popularidad, id_libro1, 'A')
        if id_libro2 in adyacentes_tipoA:
            E4.append((id_libro1, id_libro2))
            G.add_edge(id_libro1, id_libro2, color='black')

        adyacentes_tipoB = buscar_adyacentes(lista_popularidad, id_libro1, 'B')
        if id_libro2 in adyacentes_tipoB:
            E4.append((id_libro1, id_libro2))
            G.add_edge(id_libro1, id_libro2, color='orange')

# *****************************************************************************************************************************************************************************************
# *****************************************************************************************************************************************************************************************
# Este pedazo de código se encarga de formatear y mostrar el grafo. Cabe resaltar que yo hice el pseudocódigo de esta sección, pero le pedí a ChatGPT que me lo escribiera en Python
# ya que no sabía que frases como 'nx.get_edge_attributes()' eran válidas dentro de la librería de NetworkX.
#
# El pseudocódigo es el siguiente:
# 1. Para cada arista ((u,v), key) (key es un identificador para cada arista que existe entre 2 mismos nodos, va de 0 hasta (num de caminos-1)
# 2. Obtener el valor maximo que puede tener key (si por ejemplo hay 8 caminos, pues el valor maximo será 7) (n caminos <--> toca sumarle 1 al valor maximo de key para que no cuente desde 0)
#
# 3. Para cada arista (u,v) con n caminos, Dividimos el intervalo [-0.1, 0.1] en n partes usando (0.1-(-0.1))/(key+1)
# 4. Obtenemos las posiciones de u y v
# 5. Para que las aristas no se solapen entre sí, para cada arista que existe en el mismo par (u, v) se curva la arista. Para hacer esto:
# 6.    Se usa la ecuación paramétrica de un segmento de recta (r = P + tPV) y se descompone en cartesianas (x = (1-t)x1 + tx2)
# 7.    Para curvar la arista, añadimos un término adicional offset * sin(t*pi). Esto debería curvar la arista solo un poco, ya que |offset*sin(t*pi)| <= offset, y pues
#       el valor máximo de offset es max([-0.1, 0.1]) = 0.1. Entonces nos queda un error acotado superiormente por |offset*sin(t*pi)| <= 0.1 (creo que 0.1 es alrededor de 108 pixeles en 1080p 24'')
# 8. Mostrar el grafo ya con aristas separadas por colores (clasficación, etc)
def mostrar_grafo(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightgrey')
    
    max_keys = {}
    for u, v, key, data in G.edges(keys=True, data=True):
        if (u, v) not in max_keys:
            max_keys[(u, v)] = key
        else:
            max_keys[(u, v)] = max(max_keys[(u, v)], key)
    
    for (u, v), tamaño in max_keys.items():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        num_points = 100
        t = np.linspace(0, 1, num_points)
        num_iterations = tamaño + 1
        interval_width = 0.2 / num_iterations
        for key, i in enumerate(range(1, num_iterations + 1)):
            offset = -0.1 + i * interval_width
            curve_x = (1 - t) * x1 + t * x2 + offset * np.sin(t * np.pi)
            curve_y = (1 - t) * y1 + t * y2 + offset * np.sin(t * np.pi)
            plt.plot(curve_x, curve_y, color=G[u][v][key]['color'], alpha=0.5)
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(color='red', label='C1: por misma materia'),
        Patch(color='blue', label='C2: por autor común'),
        Patch(color='green', label='C3: por palabras comunes'),
        Patch(color='black', label='C4: por misma popularidad'),
        Patch(color='orange', label='C5: por cercanía en popularidad', hatch='//')
    ]
    plt.legend(handles=legend_elements, loc='best')

    nx.draw_networkx_labels(G, pos)
    plt.title("Grafo de relaciones entre libros")
    plt.axis('off')
    plt.show()
# *****************************************************************************************************************************************************************************************
# *****************************************************************************************************************************************************************************************