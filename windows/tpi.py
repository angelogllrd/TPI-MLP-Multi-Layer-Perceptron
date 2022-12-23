# -*- coding: utf-8 -*-

# Lista de widgets disponible en Formulario -> View Python Code, del Designer
from PyQt5.QtWidgets import QMainWindow, QAbstractSpinBox, QApplication, QDoubleSpinBox, QFormLayout, QGraphicsView, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLayout, QLineEdit, QMainWindow, QPlainTextEdit, QPushButton, QRadioButton, QSizePolicy, QSlider, QSpinBox, QStatusBar, QTabWidget, QVBoxLayout, QWidget, QFileDialog, QDesktopWidget, QDialog, QMessageBox
from PyQt5.QtGui import QTextCursor, QIcon # Para moverme hasta arriba en los QPlainTextEdit donde se muestran la red y datasets
from PyQt5 import uic
from PyQt5 import QtCore # Para usar expresiones regulares con QRegularExpression
from PyQt5 import QtTest # Para generar delays

import sys, os, random

from math import exp, floor, ceil

from time import sleep

import json

import matplotlib.pyplot as plt
import numpy as np



# Para no tener problemas con las rutas en la conversión a .exe 
# https://nitratine.net/blog/post/issues-when-using-auto-py-to-exe/#the-one-file-resource-wrapper
def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




# ***********************************************************
# FUNCIONES PARA CREACIÓN E IMPRESIÓN DE PATRONES Y DATASETS
# ***********************************************************


def inicializarPatrones():
    """Devuelve los patrones de las 3 letras, en forma de listas de 100 elementos con 1 y 0."""
    b, d, f = [], [], []
    for pos in range(100):
        if pos in posb:
            b.append(1)
        else: 
            b.append(0)
        if pos in posd:
            d.append(1)
        else: 
            d.append(0)
        if pos in posf:
            f.append(1)
        else: 
            f.append(0)
    return b, d, f


def imprimirMatriz(patron):
    """Recibe un patrón e imprime la matriz de pixeles con * en cada pixel pintado. Se la usa solamente para pruebas."""
    print(' __________ ')
    for f in range(10):
        fila = '|'
        for c in range(10):
            if patron[f*10+c] == 0: # f*10+c transforma una posición fila-columna a una posición 0-99 del patrón
                fila += ' '
            else:
                fila += '*'
        print(fila+'|')
    print(' ¯¯¯¯¯¯¯¯¯¯ ')


def generarDistorsion(patron, porc):
    """Distorsiona el patrón pasado un porc% (cambia "porc" veces 0 por 1, y 1 por 0)."""
    pos_anterior = []
    for pixel in range(porc):
        while True:
            pos = random.randint(0,99)
            if pos not in pos_anterior: # Solamente distorsiono pixeles que todavia no distorsioné
                break
        pos_anterior.append(pos) # Guardo posición para no volver a distorsionarla
        if patron[pos] == 0:
            patron[pos] = 1
        else:
            patron[pos] = 0


def generarDataset(ejemplos):
    """
    * Genera un dataset con el nro de ejemplos pasado, cumpliendo 10% sin distorsión, y el resto distorsionado 1%-30%. 
      El dataset es una lista de listas, donde cada sublista es un patrón de entrada o fila del dataset. 
      Para asegurar que los conjuntos de test y validación sean representativos, se genera de la siguiente manera,
      quedando 4 porciones de cada tipo de ejemplo:
             ____________________ _
            | 10% sin distorsion | --> Contiene las 3 letras agregadas de manera "cíclica", comenzando por una al azar
            |--------------------|-
            |  30% distorsionado | --> Contiene letras aleatorias con distorsiones aleatorias entre 1% y 10% 
            |      del 1-10%     | 
            |--------------------|-
            |  30% distorsionado | --> Contiene letras aleatorias con distorsiones aleatorias entre 11% y 20%
            |      del 11-20%    |
            |--------------------|-
            |  30% distorsionado | --> Contiene letras aleatorias con distorsiones aleatorias entre 21% y 30%
            |      del 21-30%    |
            `--------------------´-
      
    * Los datasets de test y validación se crean incluyendo ejemplos de cada porción, lo mas similares posibles en cantidad.    
    * Retorna el dataset completo, y los conjuntos de entrenamiento, test, y validación.
    """
    
    dataset = []

    porc_test = 0.08 # Debe ser un porcentaje que haga divisible por 4 (4 porciones representativas) el número de ejemplos de test para 100, 500 y 1000.
                     # Con 12% para test, los restantes ejemplos NO alcanzan para conseguir formar conjuntos de validación representativos.
                     # Tomar el 8% SI permite formar todos los conjuntos de validación representativos para los 3 datasets (segun cálculos).
    
    sin_dist = int(ejemplos * 0.10) # Cantidad de ejemplos sin distorsión
    con_dist_por_rango = int((ejemplos-sin_dist)/3) # Cantidad de ejemplos para los rangos de distorsión (1-10%, 11-20% y 21-30%)

    letras = [['b',patronb,[1,0,0]], ['d',patrond,[0,1,0]], ['f',patronf,[0,0,1]]] 
    random.shuffle(letras) # Para que la porción sin distorsión no comience siempre por "b", porque el 10% de 100, 500 y 1000 no es divisible por 3 y nunca queda igual cantidad de cada letra
    ind = 0 # Para recorrer "letras" en forma cíclica

    # GENERO EL DATASET PRINCIPAL
    for ejemplo in range(ejemplos):
        # Sin distorsión
        if ejemplo < sin_dist:
            letra = letras[ind][0]
            patron = letras[ind][1].copy()
            clases = letras[ind][2]
            if ind < 2:
                ind += 1
            else: 
                ind = 0
        else:
            # Con distorsión por rangos
            letra_aleatoria = random.choice(letras) # Cuando hay distorsión, selecciono letra al azar
            letra = letra_aleatoria[0]
            patron = letra_aleatoria[1].copy() # Copio el patron sin distorsionar de la letra
            clases = letra_aleatoria[2]
            if ejemplo < sin_dist+con_dist_por_rango:
                distorsión_aleatoria = random.randint(1, 10) # Distorsión aleatoria del 1-10%
            elif ejemplo < sin_dist+con_dist_por_rango*2:
                distorsión_aleatoria = random.randint(11, 20) # Distorsión aleatoria del 11-20%
            elif ejemplo < ejemplos:
                distorsión_aleatoria = random.randint(21, 30) # Distorsión aleatoria del 21-30%
            generarDistorsion(patron, distorsión_aleatoria) # Distorsiono el patrón
        dataset.append(patron+clases) # Lo agrego al dataset principal

        # # Esto imprime las matrices, junto con la letra y la distorsión a medida que las genera (solamente para probar)
        # imprimirMatriz(patron)
        # print('Ejemplo:', ejemplo+1)
        # print('Letra:', letra)
        # print('Distorsion: ', end='')
        # if ejemplo < sin_dist:
        #   print('Sin distorsionar')
        # else:
        #   print(distorsión_aleatoria,'%')

    # HAGO SLICING DEL DATASET EN SUS PORCIONES PARA FACILITAR EL TRABAJO
    parte_sin_dist = dataset[0:sin_dist]
    parte_dist_1_10 = dataset[sin_dist:sin_dist+con_dist_por_rango]
    parte_dist_11_20 = dataset[sin_dist+con_dist_por_rango:sin_dist+con_dist_por_rango*2]
    parte_dist_21_30 = dataset[sin_dist+con_dist_por_rango*2:ejemplos]

    # GENERO EL DATASET DE TEST
    et = int(ejemplos * porc_test) # et = ejemplos_test
    etpp = int(et/4) # etpp = ejemplos_test_por_porcion
    dataset_test = parte_sin_dist[:etpp] + parte_dist_1_10[:etpp] + parte_dist_11_20[:etpp] + parte_dist_21_30[:etpp]

    # QUITO DE LAS PORCIONES LOS EJEMPLOS QUE CARGUÉ EN EL DATASET DE TEST, Y FORMO DATASET DE ENTRENAMIENTO
    parte_sin_dist = parte_sin_dist[etpp:]
    parte_dist_1_10 = parte_dist_1_10[etpp:]
    parte_dist_11_20 = parte_dist_11_20[etpp:]
    parte_dist_21_30 = parte_dist_21_30[etpp:]
    dataset_entr = parte_sin_dist + parte_dist_1_10 + parte_dist_11_20 + parte_dist_21_30 

    # GENERO LOS CONJUNTOS DE VALIDACIÓN
    for porc_valid in [0.1, 0.2, 0.3]:
        # Genero el conjunto de acuerdo al porcentaje
        ev = int(ejemplos * porc_valid) # ev = ejemplos_validacion
        if (ev % 4) == 0: # Cantidad de ejemplos del conjunto de validación es divisible por 4, porciones iguales
            evpp = int(ev/4)  # evpp = ejemplos_validacion_por_porcion
            conj = parte_sin_dist[:evpp] + parte_dist_1_10[:evpp] + parte_dist_11_20[:evpp] + parte_dist_21_30[:evpp]
        else: # Cantidad de ejemplos del conjunto de validación NO divisible por 4, porciones distintas
            evpp1 = floor(ev/4) 
            evpp2 = evpp1 + 1
            l_evpp = [evpp1, evpp1, evpp2, evpp2] # Decido aleatoriamente cuánto tomo de cada porción (Ejemplos de validación = evpp1*2 + evpp2*2)
            random.shuffle(l_evpp) # Para que los ejemplos que tomo de cada porción no sean siempre los mismos
            conj = parte_sin_dist[:l_evpp[0]] + parte_dist_1_10[:l_evpp[1]] + parte_dist_11_20[:l_evpp[2]] + parte_dist_21_30[:l_evpp[3]]
        
        # # Para probar
        # print('Cantidad de ejemplos del conjunto de validacion de', int(porc_valid*100),'%:', len(conj))

        # Asigno el conjunto en su correspondiente variable
        if porc_valid == 0.1:
            conj_val10 = conj
        elif porc_valid == 0.2:
            conj_val20 = conj
        else:
            conj_val30 = conj

    return dataset, dataset_entr, dataset_test, conj_val10, conj_val20, conj_val30


# def generarDataset(ejemplos):   
#     """Lo mismo que la anterior, pero hace la selección de los ejemplos de los conjuntos de test y validación
#        de manera ALEATORIA, es decir, no asegura que tengan la misma cantidad de cada una de las 4 porciones."""
    
#     dataset = []
#     sin_distorsionar = ejemplos * 0.10
#     porc_test = 0.2 # A diferencia del anterior generarDataset(), podemos poner diferentes porcentajes

#     # GENERO EL DATASET PRINCIPAL
#     for ejemplo in range(ejemplos):
#         letra = random.choice(['b','d','f'])
#         if letra == 'b':
#             patron = patronb.copy()
#             clases = [1,0,0]
#         elif letra == 'd':
#             patron = patrond.copy()
#             clases = [0,1,0]
#         else:
#             patron = patronf.copy()
#             clases = [0,0,1]
        
#         if ejemplo >= sin_distorsionar: # Si ya generé más del 10% de ejemplos, distorsiono entre 1% y 30%
#             distorsión_aleatoria = random.randint(1, 30)
#             generarDistorsion(patron, distorsión_aleatoria)
#         dataset.append(patron+clases)
        
#         # # Esto imprime las matrices, junto con la letra y la distorsión a medida que las genera (solamente para probar)
#         # imprimirMatriz(patron)
#         # print('Ejemplo:',ejemplo+1)
#         # print('Letra:', letra)
#         # print('Distorsion: ', end='')
#         # if ejemplo < sin_distorsionar:
#         #   print('Sin distorsionar')
#         # else:
#         #   print(distorsión_aleatoria,'%')

#     dataset_entr = dataset.copy()
#     random.shuffle(dataset_entr) # Mezclo aleatoriamente los patrones

#     # GENERO EL DATASET DE TEST
#     et = int(ejemplos * porc_test) # et = ejemplos_test
#     dataset_test = dataset_entr[:et]

#     # QUITO LOS EJEMPLOS CARGADOS EN EL DATASET DE TEST (EL DATASET RESULTANTE ES EL DE ENTRENAMIENTO)
#     dataset_entr = dataset_entr[et:]

#     # GENERO LOS CONJUNTOS DE VALIDACIÓN
#     for porc_valid in [0.1, 0.2, 0.3]:
#         ev = int(ejemplos * porc_valid) # ev = ejemplos_validacion
#         conj = dataset_entr[:ev]

#         if porc_valid == 0.1:
#             conj_val10 = conj
#         elif porc_valid == 0.2:
#             conj_val20 = conj
#         else:
#             conj_val30 = conj

#     return dataset, dataset_entr, dataset_test, conj_val10, conj_val20, conj_val30


def cargarDataset(dataset):
    """Se usa en la 1ra pestaña, con el botón "Cargar". Toma un dataset "full" (con los 100, 500 o 1000 ejemplos, sin mezclar, 
       sin repartir en test, validación, etc) y extrae los demás datasets usando la misma lógica que el primer generarDataset()."""

    ejemplos = len(dataset)
    porc_test = 0.08
    
    sin_dist = int(ejemplos * 0.10) # Cantidad de ejemplos sin distorsión
    con_dist_por_rango = int((ejemplos-sin_dist)/3) # Cantidad de ejemplos para los rangos de distorsión (1-10%, 11-20% y 21-30%)

    letras = [['b',patronb,[1,0,0]], ['d',patrond,[0,1,0]], ['f',patronf,[0,0,1]]] 
    random.shuffle(letras) 
    ind = 0 

    # HAGO SLICING DEL DATASET EN SUS PORCIONES PARA FACILITAR EL TRABAJO
    parte_sin_dist = dataset[0:sin_dist]
    parte_dist_1_10 = dataset[sin_dist:sin_dist+con_dist_por_rango]
    parte_dist_11_20 = dataset[sin_dist+con_dist_por_rango:sin_dist+con_dist_por_rango*2]
    parte_dist_21_30 = dataset[sin_dist+con_dist_por_rango*2:ejemplos]

    # GENERO EL DATASET DE TEST
    et = int(ejemplos * porc_test) # et = ejemplos_test
    etpp = int(et/4) # etpp = ejemplos_test_por_porcion
    dataset_test = parte_sin_dist[:etpp] + parte_dist_1_10[:etpp] + parte_dist_11_20[:etpp] + parte_dist_21_30[:etpp]

    # QUITO DE LAS PORCIONES LOS EJEMPLOS QUE CARGUÉ EN EL DATASET DE TEST, Y FORMO DATASET DE ENTRENAMIENTO
    parte_sin_dist = parte_sin_dist[etpp:]
    parte_dist_1_10 = parte_dist_1_10[etpp:]
    parte_dist_11_20 = parte_dist_11_20[etpp:]
    parte_dist_21_30 = parte_dist_21_30[etpp:]
    dataset_entr = parte_sin_dist + parte_dist_1_10 + parte_dist_11_20 + parte_dist_21_30 

    # GENERO LOS CONJUNTOS DE VALIDACIÓN
    for porc_valid in [0.1, 0.2, 0.3]:
        # Genero el conjunto de acuerdo al porcentaje
        ev = int(ejemplos * porc_valid) # ev = ejemplos_validacion
        if (ev % 4) == 0: # Cantidad de ejemplos del conjunto de validación es divisible por 4, porciones iguales
            evpp = int(ev/4)  # evpp = ejemplos_validacion_por_porcion
            conj = parte_sin_dist[:evpp] + parte_dist_1_10[:evpp] + parte_dist_11_20[:evpp] + parte_dist_21_30[:evpp]
        else: # Cantidad de ejemplos del conjunto de validación NO divisible por 4, porciones distintas
            evpp1 = floor(ev/4) 
            evpp2 = evpp1 + 1
            l_evpp = [evpp1, evpp1, evpp2, evpp2] # Ejemplos de validación = evpp1*2 + evpp2*2
            random.shuffle(l_evpp) # Para que los ejemplos que tomo de cada porción no sean siempre los mismos
            conj = parte_sin_dist[:l_evpp[0]] + parte_dist_1_10[:l_evpp[1]] + parte_dist_11_20[:l_evpp[2]] + parte_dist_21_30[:l_evpp[3]]

        # Asigno el conjunto en su correspondiente variable
        if porc_valid == 0.1:
            conj_val10 = conj
        elif porc_valid == 0.2:
            conj_val20 = conj
        else:
            conj_val30 = conj

    return dataset_entr, dataset_test, conj_val10, conj_val20, conj_val30


# def convertirStringADataset(string):
#     """NO SE USA MÁS, REEMPLAZADO POR json.loads(). Convierte una string de lista de listas a una estructura de lista de 
#        listas. Se usa cuando se carga un dataset desde un .txt"""
#     pos = -1
#     dataset = []
#     while True:
#         fila= []
#         for i in range(103):
#             pos += 3
#             #print(pos, string[pos], i)
#             fila.append(int(string[pos]))
#         dataset.append(fila)
#         if string[pos+2] == ']':
#             break
#         else:
#             pos += 2
#     return dataset


def imprimirDatasetGraficoConAsteriscos(dataset):
    """Imprime el dataset en forma gráfica (matrices de los patrones) con * en cada pixel pintado, dispuesto en "cant_filas" 
       filas de "patrones_por_fila" patrones."""
    
    dataset_copia = dataset[:]
    str_total = '' # String que contendrá todo lo que se muestra
    patrones_por_fila = 10
    cant_filas = ceil(len(dataset_copia)/patrones_por_fila)
    nro_patron = 1 # Contador para poner números a las matrices
    
    for i in range(cant_filas):
        patrones_de_fila = dataset_copia[:patrones_por_fila]
        for nro in range(len(patrones_de_fila)):
            if nro_patron < 10:
                str_total += '     ' + str(nro_patron) + '     '
            elif nro_patron < 100:
                str_total += '     ' + str(nro_patron) + '    '
            else:
                str_total += '     ' + str(nro_patron) + '   '
            nro_patron += 1
        str_total += '\n'
        str_total += ' __________' * len(patrones_de_fila) + '\n'
        for f in range(10):
            for patron in range(len(patrones_de_fila)):
                fila = '|'
                for c in range(10):
                    if patrones_de_fila[patron][f*10+c] == 0: # f*10+c transforma una posición fila-columna a una posición 0-99 del patrón
                        fila += ' '
                    else:
                        fila += '*'
                if patron == len(patrones_de_fila)-1:
                    str_total += fila+'|' + '\n'
                else:
                    str_total += fila
        str_total += ' ¯¯¯¯¯¯¯¯¯¯' * len(patrones_de_fila) + '\n'
        dataset_copia = dataset_copia[patrones_por_fila:]
    UIWindow.window_dataset.plainTextEdit_grafico.appendPlainText(str_total)


def imprimirDatasetGraficoConPosiciones(dataset):
    """Imprime el dataset en forma gráfica (matrices de los patrones) con la posición en cada pixel pintado, dispuesto en 
       "cant_filas" filas de "patrones_por_fila" patrones."""
    
    dataset_copia = dataset[:]
    str_total = '' # String que contendrá todo lo que se muestra
    patrones_por_fila = 5
    cant_filas = ceil(len(dataset_copia)/patrones_por_fila)
    nro_patron = 1 # Contador para poner números a las matrices
    
    for i in range(cant_filas):
        patrones_de_fila = dataset_copia[:patrones_por_fila]
        for nro in range(len(patrones_de_fila)):
            if nro_patron < 10:
                str_total += '          ' + str(nro_patron) + '          '
            elif nro_patron < 100:
                str_total += '          ' + str(nro_patron) + '         '
            else:
                str_total += '          ' + str(nro_patron) + '        '
            nro_patron += 1
        str_total += '\n'
        str_total += ' ____________________' * len(patrones_de_fila) + '\n'
        for f in range(10):
            for patron in range(len(patrones_de_fila)):
                fila = '|'
                for c in range(10):
                    if patrones_de_fila[patron][f*10+c] == 0: # f*10+c transforma una posición fila-columna a una posición 0-99 del patrón
                        fila += '  '
                    else:
                        if f == 0:
                            fila += str(f*10+c) + ' '
                        else:
                            fila += str(f*10+c)
                if patron == len(patrones_de_fila)-1:
                    str_total += fila+'|' + '\n'
                else:
                    str_total += fila
        str_total += ' ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯' * len(patrones_de_fila) + '\n'
        dataset_copia = dataset_copia[patrones_por_fila:]
    UIWindow.window_dataset.plainTextEdit_grafico.appendPlainText(str_total)


def imprimirDatasetTabular(dataset):
    """Imprime el dataset en forma tabular."""
    str_total = '' # String que contendrá todo lo que se muestra
    nombres_col1 = '     '
    for i in range(10):
        nombres_col1 += str(i)+'         '
    str_total += nombres_col1 + '\n'
    nombres_col2 = '     ' + '0123456789'*10 + ' yb yd yf'
    str_total += nombres_col2 + '\n'
    str_total += '     ' + '-'*109 + '\n'
    
    for fila in range(len(dataset)):
        if fila+1 < 10:
            espacio = '    '
        elif fila+1 < 100:
            espacio = '   '
        elif fila+1 < 1000:
            espacio = '  '
        else:
            espacio = ' '
        str_fila = str(fila+1) + espacio
        for pixel in range(len(dataset[fila])-3):
            str_fila += str(dataset[fila][pixel])
        str_fila += '  ' + str(dataset[fila][-3]) + '  ' + str(dataset[fila][-2]) + '  ' + str(dataset[fila][-1])
        str_total += str_fila + '\n'
    UIWindow.window_dataset.plainTextEdit_tabular.appendPlainText(str_total)


def restarDatasets(aEste, restaleEste):
    """Quita de un dataset filas de otro. Se lo usa para restar al conjunto de entrenamiento los de validación."""
    aEste2 = aEste[:] # Para no modificar la lista "aEste" original, la copio en una nueva y elimino lo que quiero de la copia
    for fila in restaleEste:
        aEste2.remove(fila) # No hace falta comprobar que "fila" este en "aEste" porque son filas extraidas originalmente de "aEste"
    return aEste2



# ***********************************************************
# CREACIÓN DE LA RED Y DE FUNCIONES PARA EL ALGORITMO
# ***********************************************************


def crearRed(neuronasDeEntrada, nroCapasOcultas, neuronasPorCapaOculta, neuronasDeSalida):
    """Crea la estructura de la red, con las neuronas de cada capa."""
    red = []
    for capa in range(nroCapasOcultas+2):
        c = []
        for neurona in range(([neuronasDeEntrada]+neuronasPorCapaOculta+[neuronasDeSalida])[capa]):
            if capa == 0: # Creo neurona de capa de entrada
                n = { 
                    'salida': 0
                }
            elif capa == nroCapasOcultas+1: # Creo neurona de capa de salida
                n = {
                    'pesos': [], # Pesos de conexiones de unidades de la capa anterior con esta unidad
                    'cambiosPeso': [], # Para cálculo del término momento
                    'net': 0,
                    'salida': 0,
                    'salidaDeseada': 0,
                    'delta': 0
                }
            else: # Creo neurona de capa oculta
                n = {
                    'pesos': [], # Pesos de conexiones de unidades de la capa anterior con esta unidad
                    'cambiosPeso': [], # Para cálculo del término momento
                    'net': 0,
                    'salida': 0,
                    'delta': 0
                }
            c.append(n)
        red.append(c)
    return red


def imprimirRed(red):
    """Muestra el contenido de la red en su estado actual, por cada capa."""
    str_total = ''
    tam_titulo = 113
    for capa in range(len(red)):
        if capa == 0:
            str_total += dibujarTituloCapa('CAPA DE ENTRADA', tam_titulo)
        elif capa == len(red)-1:
            str_total += dibujarTituloCapa('CAPA DE SALIDA', tam_titulo)
        else:
            str_total += dibujarTituloCapa('CAPA OCULTA ' + str(capa), tam_titulo)
        if capa == 0: # Dibujo capa de entrada, con neuronas una al lado de la otra, y 6 neuronas por fila
            sub_str1 = sub_str2 = sub_str3 = '     '
            for neurona in range(len(red[capa])):
                if neurona+1 > 9:
                    subray = '¯¯¯¯¯¯¯¯¯¯       '
                    espacio = ''
                else:
                    subray = '¯¯¯¯¯¯¯¯¯       '
                    espacio = ' '
                sub_str1 += 'Neurona ' + str(neurona+1) + espacio + '       '
                sub_str2 += subray + espacio 
                sub_str3 += '* salida: ' + str(red[capa][neurona]['salida']) + '      '
                if (neurona+1) % 6 == 0 or (neurona+1) == 100: # Si terminé de imprimir las 6 neuronas de la fila o es la última fila, imprimo 
                    str_total += '\n' + sub_str1 + '\n' + sub_str2 + '\n' + sub_str3 + '\n'
                    sub_str1 = sub_str2 = sub_str3 = '     '
        else: # Dibujo capa oculta o de salida
            for neurona in range(len(red[capa])):
                if neurona+1 > 9:
                    subray = '     ¯¯¯¯¯¯¯¯¯¯'
                else:
                    subray = '     ¯¯¯¯¯¯¯¯¯'                
                str_total += '\n     Neurona ' + str(neurona+1) + '\n'
                str_total += subray + '\n'
                for contenido in range(len(red[capa][neurona])):
                    str_total += '     ' + '* ' + list(red[capa][neurona].keys())[contenido] + ': ' + str(list(red[capa][neurona].values())[contenido]) + '\n'
    UIWindow.window_red.plainTextEdit_red.appendPlainText(str_total)


def dibujarTituloCapa(nombre_capa, tam_titulo):
    """Devuelve un string con el titulo de la capa recuadrado."""
    str_total = '\n ' + '_'*tam_titulo + '\n'
    esp_inicio = floor((tam_titulo-len(nombre_capa))/2)
    esp_fin = tam_titulo - esp_inicio - len(nombre_capa)
    str_total += '|' + ' '*esp_inicio + nombre_capa + ' '*esp_fin + '|\n '
    str_total += '¯'*tam_titulo + '\n'
    return str_total


def inicializarPesos(red):
    """Paso 1: Inicializar los pesos de la red con valores pequeños aleatorios."""
    for capa in range(1,len(red)):
        for neuronaActual in red[capa]:
            for neuronaAnterior in range(len(red[capa-1])):
                 neuronaActual['pesos'].append(random.uniform(-0.5,0.5)) # Siguiendo la recomendación del libro para valores iniciales de pesos (+-0.5)
                 neuronaActual['cambiosPeso'].append(0) # Los cambios de peso sirven para el cálculo del termino mómento


def aplicarPatronDeEntrada(patron, red):
    """Paso 2: Presentar un patrón de entrada del dataset."""
    
    # Verifico que el nro de neuronas de entrada coindida con el nro de entradas del patrón (comprobación por motivos de test)
    if len(red[0]) != len(patron[:-3]):
        print('Número de entradas no coincide con número de neuronas en capa de entrada')
    else:
        for i in range(len(red[0])): # Cargo valores de entrada del patrón en neuronas de entrada
            red[0][i]['salida'] = patron[i]
        for salida in range(len(red[-1])): # Guardo valores de salida (clases) del patrón en neuronas de salida
            red[-1][salida]['salidaDeseada'] = patron[len(red[0])+salida]


def calcularSalidasRed(fActSalida, fActOculta, red):
    """Paso 3: Propagar las entradas y calcular las salidas de la red."""
    for capa in range(1,len(red)):
        for neuronaActual in red[capa]:
            # Paso 3.1: Calculo los net (de neuronas ocultas y de salida)
            neuronaActual['net'] = calcularNetNeurona(neuronaActual['pesos'], capa-1, red)
            # Paso 3.2: Calculo las salidas (de neuronas ocultas y de salida)
            neuronaActual['salida'] = calcularSalidaNeurona(neuronaActual['net'], capa, fActSalida, fActOculta, red)

    
def calcularNetNeurona(pesosNeurona, capaAnterior, red):
    """Paso 3.1"""
    net = 0
    for i in range(len(red[capaAnterior])): # o bien for i in range(len(pesosNeurona))
        net += pesosNeurona[i] * red[capaAnterior][i]['salida']
    return net


def calcularSalidaNeurona(net, capa, fActSalida, fActOculta, red):
    """Paso 3.2"""
    if capa == len(red)-1: # Capa de salida
        if fActSalida == 'lineal':
            return funcionLineal(net)
        else:
            return funcionSigmoidal(net)
    else: # Capa oculta
        if fActOculta == 'lineal':
            return funcionLineal(net)
        else:
            return funcionSigmoidal(net)


def funcionLineal(x):
    return x


def funcionSigmoidal(x):
    """
    * La constante "e" elevada a un número mayor a 709.78271 resulta en un número extremadamente grande que supera la 
      representación en coma flotante: 1.7976931348623157e+308, y devuelve un error de OverflowError. 
    * Por la forma de la función sigmoidal, esto pasa cuando le pasamos un x menor a -709.78271 (que eleva "e" a un 
      número mayor a 709.78271). 
    * Si se pudiera representar, el resultado de la función sigmoidal en este caso, sería un número con más de 309 
      ceros adelante (prácticamente 0). 
    * Por eso, para evitar el OverflowError cuando se presenta este caso, se reemplaza la potencia de "e" con la 
      constante inf (infinito positivo de punto flotante), que se representa con float('inf') o math.inf, y que hace 
      que la función devuelva directamente 0.
    """
    
    try:
        potencia = exp(-x) # math.exp(x) retorna "e" elevado a la x potencia
    except OverflowError:
        potencia = float('inf') # o math.inf
    
    # # O también:
    # if x < -709.78271:
    #   potencia = float('inf')
    # else:
    #   potencia = exp(-x)

    return 1/(1+potencia)


def calcularTerminosErrorRed(fActSalida, fActOculta, red):
    """Paso 4: Se calculan los términos de error para neuronas de salida y ocultas, comenzando por las de salida 
       (propagación de errores hacia atrás)."""
    for capa in reversed(range(1,len(red))): # Recorro las capas hacia atrás
        for nroNeurona in range(len(red[capa])):
            neuronaActual = red[capa][nroNeurona]
            neuronaActual['delta'] = calcularTerminoError(capa, neuronaActual, nroNeurona, fActSalida, fActOculta, red)


def derivadaFuncionSigmoidal(salida):
    return salida*(1-salida)


def calcularTerminoError(capa, neuronaActual, nroNeurona, fActSalida, fActOculta, red):
    """Determina un término de error en base a la capa actual, la neurona actual, y el número de esa neurona.
       El número de la neurona es usado para el cálculo del delta en neuronas ocultas."""
    delta = 0
    if capa == len(red)-1: # Estoy en capa de salida, calculo delta para neuronas de salida
        if fActSalida == 'lineal':
            delta = neuronaActual['salidaDeseada'] - neuronaActual['salida']
        else:
            delta = (neuronaActual['salidaDeseada'] - neuronaActual['salida']) * derivadaFuncionSigmoidal(neuronaActual['salida'])
    else: # Estoy en una capa oculta, calculo delta de neuronas ocultas
        sumatoria = 0
        for neuronaCapaSiguiente in red[capa+1]:
            sumatoria += neuronaCapaSiguiente['delta'] * neuronaCapaSiguiente['pesos'][nroNeurona] # Acumulo la sumatoria del producto del delta de cada neurona de la capa siguiente por el peso que almacena en la posición de la neurona actual
        if fActOculta == 'lineal':
            delta = sumatoria
        else:
            delta = derivadaFuncionSigmoidal(neuronaActual['salida']) * sumatoria
    return delta


def actualizarPesosRed(alfa, beta, red):
    """Paso 5: Actualización de los pesos de la red."""
    for capa in reversed(range(1,len(red))): # Recorro las capas hacia atrás (podría hacerlo hacia adelante)
        for neuronaActual in red[capa]: 
            for peso in range(len(red[capa-1])):
                pesoViejo = neuronaActual['pesos'][peso]
                pesoNuevo = pesoViejo + alfa * neuronaActual['delta'] * red[capa-1][peso]['salida'] + beta * neuronaActual['cambiosPeso'][peso]
                cambioPeso = pesoNuevo - pesoViejo
                neuronaActual['pesos'][peso] = pesoNuevo
                neuronaActual['cambiosPeso'][peso] = cambioPeso


def calcularMSE(red):
    """Paso 6: Calcula el error cuadrático medio entre la salida obtenida y la deseada."""
    sumatoria = 0
    for neuronaSalida in red[-1]:
        delta = neuronaSalida['salidaDeseada'] - neuronaSalida['salida']
        delta_cuad = delta**2
        sumatoria += delta_cuad
    mse = 0.5 * sumatoria
    return mse



# ***********************************************************
# OTRAS FUNCIONES
# ***********************************************************


def convertirErrorAString(error):
    """
    * Convierte un float a string, considerando que puede estar en notación científica.
    * Se usa para tener el string de un error hasta N cifras decimales.
    * No se usa f'{num:.Nf}' (u otra forma de formatear strings) porque dependiendo de las cifras 
      decimales siguientes (a la N-esima en este caso), la última cifra puede quedar redondeada.
    * Ej: f'{0.123456789:.8f}' quedaría '0.12345679', cuando debería ser '0.12345678'. 
    """
    str_error = str(error)
    pos = str_error.find('e')
    if pos != -1: # Error con notación científica
        if str_error[pos+1] == '-':
            str_error = '0.' + '0'*(int(str_error[pos+2:])-1) + str_error[0] + str_error[2:pos]
        else:
            exp = int(str_error[pos+2:])
            sin_punto = str_error[0] + str_error[2:pos]
            nros_desp_coma = len(sin_punto)-1
            if exp == nros_desp_coma:
                str_error = sin_punto # Ej: 1.234e+3 = 1234
            elif exp > nros_desp_coma:
                str_error = sin_punto + '0'*(nros_desp_coma-exp) # Ej: 1.234e+5 = 123400
            else:
                str_error = str_error[:exp+1] + '.' + str_error[exp+1:] # Ej: 1.234e+2 = 123.4
    else: # Error sin notación científica
        str_error = str(error)

    # print(error == float(str_error))
    return str_error



# ***********************************************************
# UI, DEFINICIÓN DE CLASES, ATRIBUTOS Y MÉTODOS
# ***********************************************************


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Cargamos el archivo .ui
        uic.loadUi(resource_path("ui\\uitpi.ui"), self)

        # Hacemos inicializaciones
        self.initUI()


        # ATRIBUTOS, ACCIONES DISPARADAS, INICIALIZACIONES, DESACTIVACIONES
        # -----------------------------------------------------------------


        # Labels
        self.labels_matriz1 = self.findChildren(QLabel, QtCore.QRegularExpression ("^label_\d\d$")) # Creo una lista con los QLabels que forman el 1er gráfico de matriz de patrón, usando una expresión regular para matchear los nombres (https://doc.qt.io/qtforpython-5/PySide2/QtCore/QRegExp.html)
        self.labels_matriz2 = self.findChildren(QLabel, QtCore.QRegularExpression ("^label_1\d\d$")) # Lo mismo para los labels de la segunda matriz
        def ordenarLabels(label): return label.objectName() # Para ordenar los QLabels por nombre (porque los devuelve desordenados)
        self.labels_matriz1.sort(key = ordenarLabels) # Ordeno los QLabels (el orden es importante para pintar la matriz)
        self.labels_matriz2.sort(key = ordenarLabels) # Ordeno los QLabels (el orden es importante para pintar la matriz)
        
        # # Para probar si lista y ordena correctamente los labels
        # print(len(self.labels_matriz1))
        # print(len(self.labels_matriz2))
        # for label in self.labels_matriz2:
        #     print(label.objectName())

        # Acciones disparadas por pushbuttons
        self.pushButton_generar.clicked.connect(self.generarDataset)
        self.pushButton_guardar.clicked.connect(self.guardarDataset)
        self.pushButton_cargar.clicked.connect(self.cargarDataset)
        self.pushButton_crearred.clicked.connect(self.crearRed)
        self.pushButton_entrenar.clicked.connect(self.entrenarRed)
        self.pushButton_guardarredesentrenadas.clicked.connect(self.guardarRedesEntrenadas)
        self.pushButton_hacertest.clicked.connect(self.hacerTest)
        self.pushButton_letraB.clicked.connect(lambda: self.tratarLetra(patronb,'b'))
        self.pushButton_letraD.clicked.connect(lambda: self.tratarLetra(patrond,'d'))
        self.pushButton_letraF.clicked.connect(lambda: self.tratarLetra(patronf,'f'))
        self.pushButton_distorsionar.clicked.connect(self.generarDistorsion)
        self.pushButton_clasificar.clicked.connect(lambda: self.clasificarPatron(self.patronDistorsionado, self.label_clasificacion1, False))
        self.pushButton_probarpatrones.clicked.connect(self.probarPatrones)
        self.pushButton_verentr.clicked.connect(lambda: self.verDataset(self.dataset_entr))
        self.pushButton_vertest.clicked.connect(lambda: self.verDataset(self.dataset_test))
        self.pushButton_verval10.clicked.connect(lambda: self.verDataset(self.conjunto_val_10))
        self.pushButton_verval20.clicked.connect(lambda: self.verDataset(self.conjunto_val_20))
        self.pushButton_verval30.clicked.connect(lambda: self.verDataset(self.conjunto_val_30))
        self.pushButton_verred.clicked.connect(self.verRed)

        # Acciones disparadas por spinboxes
        self.spinBox_capasOcultas.valueChanged.connect(self.tratarCambioParametrosArq)
        self.spinBox_tamCapaOc1.valueChanged.connect(self.tratarCambioParametrosArq)
        self.spinBox_tamCapaOc2.valueChanged.connect(self.tratarCambioParametrosArq)
        self.doubleSpinBox_alfa.valueChanged.connect(self.tratarCambioParametrosArq)
        self.doubleSpinBox_beta.valueChanged.connect(self.tratarCambioParametrosArq)

        # Acciones disparadas por radiobuttons
        self.radioButton_100.toggled.connect(lambda: self.activarEsto((self.pushButton_generar,)))
        self.radioButton_100.toggled.connect(lambda: self.animarEsto((self.frame_generar,)))
        self.radioButton_500.toggled.connect(lambda: self.activarEsto((self.pushButton_generar,)))
        self.radioButton_500.toggled.connect(lambda: self.animarEsto((self.frame_generar,)))
        self.radioButton_1000.toggled.connect(lambda: self.activarEsto((self.pushButton_generar,)))
        self.radioButton_1000.toggled.connect(lambda: self.animarEsto((self.frame_generar,)))
        self.radioButton_erroracep.toggled.connect(lambda: self.activarEsto((self.pushButton_entrenar, self.progressBar_entrenamiento, self.label_entrresult, self.label_entrepocas, self.label_entrmseentr, self.label_entrmseval, self.label_entr10, self.label_entr20, self.label_entr30, self.lineEdit_nroepocas10, self.lineEdit_nroepocas20, self.lineEdit_nroepocas30, self.lineEdit_mseentr10, self.lineEdit_mseentr20, self.lineEdit_mseentr30, self.lineEdit_msevalid10, self.lineEdit_msevalid20, self.lineEdit_msevalid30)))
        self.radioButton_erroracep.toggled.connect(lambda: self.animarEsto((self.frame_entrenamiento2,)))
        self.radioButton_iteraciones.toggled.connect(lambda: self.activarEsto((self.pushButton_entrenar, self.progressBar_entrenamiento, self.label_entrresult, self.label_entrepocas, self.label_entrmseentr, self.label_entrmseval, self.label_entr10, self.label_entr20, self.label_entr30, self.lineEdit_nroepocas10, self.lineEdit_nroepocas20, self.lineEdit_nroepocas30, self.lineEdit_mseentr10, self.lineEdit_mseentr20, self.lineEdit_mseentr30, self.lineEdit_msevalid10, self.lineEdit_msevalid20, self.lineEdit_msevalid30)))
        self.radioButton_iteraciones.toggled.connect(lambda: self.animarEsto((self.frame_entrenamiento2,)))

        # Acciones disparadas por sliders
        self.horizontalSlider_probar1patron.valueChanged.connect(self.tratarLineEditSlider)

        # Acciones disparadas por comboboxes
        self.comboBox_arquitectura.activated.connect(self.tratarArquitecturaPredefinida)
        self.comboBox_funcion.activated.connect(self.tratarCambioParametrosArq)
        self.comboBox_test.activated.connect(self.tratarComboboxTest)
        self.comboBox_probarpatron.activated.connect(self.tratarComboboxProbarpatron)
        self.comboBox_tipomodelotest.activated.connect(lambda: self.tratarComboboxTipoModelo(self.comboBox_tipomodelotest, self.comboBox_test))
        self.comboBox_tipomodeloprobar.activated.connect(lambda: self.tratarComboboxTipoModelo(self.comboBox_tipomodeloprobar, self.comboBox_probarpatron))

        # Desactivaciones iniciales de sección "Arquitectura de la red"
        self.desactivarEsto((self.spinBox_tamCapaOc2, self.label_arquired5))

        # Desactivaciones iniciales de sección "Entrenamiento"
        self.desactivarEsto((self.pushButton_entrenar, self.progressBar_entrenamiento, self.label_entrresult, self.label_entrepocas, self.label_entrmseentr, self.label_entrmseval, self.label_entr10, self.label_entr20, self.label_entr30, self.lineEdit_nroepocas10, self.lineEdit_nroepocas20, self.lineEdit_nroepocas30, self.lineEdit_mseentr10, self.lineEdit_mseentr20, self.lineEdit_mseentr30, self.lineEdit_msevalid10, self.lineEdit_msevalid20, self.lineEdit_msevalid30, self.pushButton_guardarredesentrenadas))

        # Desactivaciones iniciales de sección "Test"
        self.desactivarEsto((self.pushButton_hacertest, self.label_testresult, self.label_testcorrectas, self.label_testtotal, self.label_testprec, self.lineEdit_testcorrectas, self.lineEdit_testtotal, self.lineEdit_testprec))

        # Desactivación inicial del label y botones para mostrar red y datasets
        self.desactivarEsto((self.pushButton_verred, self.pushButton_verentr, self.pushButton_vertest, self.pushButton_verval10, self.pushButton_verval20, self.pushButton_verval30, self.label_verreddataset))

        # Desactivaciones iniciales de la segunda pestaña
        self.desactivarEsto((self.label_salida_clasif, self.pushButton_clasificar, self.label_yb, self.lineEdit_yb, self.label_yd, self.lineEdit_yd, self.label_yf, self.lineEdit_yf))
        self.label_clasificacion1.setStyleSheet('background-color: rgb(255, 255, 255);border-width: 1px;border-style: solid;border-color: rgb(208, 208, 208);')
        self.label_clasificacion2.setStyleSheet('background-color: rgb(255, 255, 255);border-width: 1px;border-style: solid;border-color: rgb(208, 208, 208);')
        self.graphicsView.setStyleSheet('border: 1px solid rgb(208, 208, 208);')
        self.graphicsView_2.setStyleSheet('border: 1px solid rgb(208, 208, 208);')

        # Inicializaciónes varias
        self.funcionDeActivacionSal = 'sigmoidal'
        self.letraIngresada = ''
        self.listaRedesEntrenadas = []
        self.listaRedesPrecargadas = []

        # Definición de arquitecturas predefinidas
        self.arquitecturasPredefinidas = ({'capasOcultas': 1, 'neurOcultas': (5,), 'funcTransf': 'Lineal', 'alfa': 0.5, 'beta': 0.5},
                                          {'capasOcultas': 1, 'neurOcultas': (5,), 'funcTransf': 'Lineal', 'alfa': 0.5, 'beta': 0.9},
                                          {'capasOcultas': 1, 'neurOcultas': (10,), 'funcTransf': 'Lineal', 'alfa': 0.5, 'beta': 0.5},
                                          {'capasOcultas': 1, 'neurOcultas': (10,), 'funcTransf': 'Lineal', 'alfa': 0.5, 'beta': 0.9},
                                          {'capasOcultas': 2, 'neurOcultas': (5, 5), 'funcTransf': 'Lineal', 'alfa': 0.5, 'beta': 0.5},
                                          {'capasOcultas': 2, 'neurOcultas': (5, 5), 'funcTransf': 'Lineal', 'alfa': 0.5, 'beta': 0.9},
                                          {'capasOcultas': 2, 'neurOcultas': (10, 10), 'funcTransf': 'Lineal', 'alfa': 0.5, 'beta': 0.5},
                                          {'capasOcultas': 2, 'neurOcultas': (10, 10), 'funcTransf': 'Lineal', 'alfa': 0.5, 'beta': 0.9})

        # Inicialización de combobox de arquitecturas predefinidas
        for arq in range(len(self.arquitecturasPredefinidas)):
            self.comboBox_arquitectura.setItemData(arq, self.arquitecturasPredefinidas[arq])

        # Inicialización de lista de redes precargadas
        directorio = resource_path('redes_precargadas')
        for nombrearchivo in os.listdir(directorio):
            if nombrearchivo.endswith('.json'):
                path = os.path.join(directorio, nombrearchivo)
                f = open(path, "r")
                cosas_red = f.read()
                f.close()
                cosas_red = json.loads(cosas_red) # cosas_red contiene  
                item = (nombrearchivo[:-5], cosas_red)
                self.listaRedesPrecargadas.append(item)

        # Carga de redes precargadas
        self.tratarComboboxTipoModelo(self.comboBox_tipomodelotest, self.comboBox_test)
        self.tratarComboboxTipoModelo(self.comboBox_tipomodeloprobar, self.comboBox_probarpatron) 

       

    # MÉTODOS DE CLASE
    # ----------------
                

    def initUI(self):
        self.setWindowTitle('TPI MLP 2022 - Inteligencia Artificial - UTN FRRe') # Título de la ventana
        self.center() # Centramos ventana
        self.mostrarPorConsola('>>Hola! Para comenzar puede:\n  * Crear o cargar un dataset\n  * Seleccionar un modelo precargado') # Instrucción inicial
        self.setWindowIcon(QIcon(resource_path('icons\\icon.ico'))) # Ícono de la ventana
        self.show() # Mostramos la app


    def center(self):
        """Hace que la ventana aparezca centrada."""
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


    def mostrarPorConsola(self, texto):
        """Muestra un texto en la parte derecha de la aplicación."""
        self.consola.appendPlainText('\n'+texto)
        self.consola.moveCursor(QTextCursor.End)


    def desactivarEsto(self, cosas):
        """Recibe una tupla de cosas de la interfaz para desactivar."""
        for cosa in cosas:
            cosa.setEnabled(False)


    def activarEsto(self, cosas):
        """Recibe una tupla de cosas de la interfaz para activar."""
        for cosa in cosas:
            if not cosa.isEnabled():
                cosa.setEnabled(True)


    def generarAlerta(self, error, repetidas):
        """Muestra una alerta preguntando si seguir o no con un entrenamiento cuando el mismo no converge, o lo hace muy lento."""
        alerta = QMessageBox(self)
        alerta.setWindowTitle("Acción requerida")
        alerta.setIcon(QMessageBox.Warning)
        alerta.setText('El error no baja, o baja muy lentamente')
        alerta.setInformativeText('Las últimas ' + str(repetidas) + ' épocas arrojaron un error (considerando los primeros 8 decimales) de ' + error + '.\n\n¿Desea PARAR o SEGUIR con este entrenamiento?')
        botonParar = alerta.addButton('Parar', QMessageBox.AcceptRole)
        botonSeguir = alerta.addButton('Seguir', QMessageBox.RejectRole)
        alerta.setDefaultButton(botonParar)
        alerta.exec()
        if alerta.clickedButton() == botonParar:
            return 'parar'
        elif alerta.clickedButton() == botonSeguir:
            return 'seguir'


    def animarEsto(self, cosas):
        """Muestra una animación cuando se activa una nueva función."""
        for cosa in cosas:
            if not cosa.isEnabled():
                alfa = 255
                for tiempo in (70,60,50,40,30,20,10):
                    # cosa.setStyleSheet('background-color: rgba(140, 140, 140, 255);')
                    cosa.setStyleSheet('background-color: rgba(255, 26, 26, ' + str(alfa) + ');')
                    alfa -= 42.5
                    QtTest.QTest.qWait(tiempo)
                cosa.setEnabled(True)



    # MÉTODOS PARA LA PRIMERA PESTAÑA

 
    def generarDataset(self):
        """Genera los datasets de entrenamiento, test y validación en función del radiobutton seleccionado."""
        
        # Compruebo qué radiobutton está seleccionado y genero los dataset en base a ese tamaño
        rb100 = self.radioButton_100.isChecked() 
        rb500 = self.radioButton_500.isChecked() 
        rb1000 = self.radioButton_1000.isChecked()
        if rb100:
            self.dataset_full, self.dataset_entr, self.dataset_test, self.conjunto_val_10, self.conjunto_val_20, self.conjunto_val_30 = generarDataset(100)
        elif rb500:
            self.dataset_full, self.dataset_entr, self.dataset_test, self.conjunto_val_10, self.conjunto_val_20, self.conjunto_val_30 = generarDataset(500)
        elif rb1000:
            self.dataset_full, self.dataset_entr, self.dataset_test, self.conjunto_val_10, self.conjunto_val_20, self.conjunto_val_30 = generarDataset(1000)
        self.mostrarPorConsola('>>Datasets de entrenamiento, test y validación creados correctamente')

        # Activo nuevas funciones
        self.activarEsto((self.groupBox_arquitectura, self.pushButton_verentr, self.pushButton_vertest, self.pushButton_verval10, self.pushButton_verval20, self.pushButton_verval30, self.label_verreddataset, self.pushButton_guardar))
        self.animarEsto((self.frame_arquitectura, self.frame_guardar, self.frame_validacion10, self.frame_botonesvarios))


    def guardarDataset(self):
        """Guarda en la ruta del ejecutable el dataset completo generado."""
        try:
            os.mkdir('datasets')
        except:
            pass
        tam = len(self.dataset_full) # Determino el tamaño del dataset actual
        f = open(f'datasets\\dataset_de_{tam}.txt', 'w') # Creo el archivo .txt
        f.write(str(self.dataset_full)) # Escribo el archivo
        f.close()
        path = os.path.dirname(__file__) # Obtengo el path del ejecutable
        self.mostrarPorConsola(f'>>Dataset guardado correctamente en {path}\\datasets')


    def cargarDataset(self):
        """Carga un dataset desde un .txt (debería ser un "dataset_full" guardado previamente, con los 100, 500 o 1000 ejemplos)
           y extrae los demás conjuntos."""
        fname = QFileDialog.getOpenFileName(self, 'Open File', '', "*.txt") # Abrimos un cuadro de diálogo
        if not fname[0] == '': # fname[0] devuelve '' cuando cancelamos en el cuadro de diálogo
            path = fname[0] # Obtengo el path del arhivo seleccionado
            f = open(path, "r")
            dataset_string = f.read()
            f.close()
            dataset = json.loads(dataset_string) # Convierto el string del dataset a una estructura de lista de patrones
            self.dataset_full = dataset
            self.dataset_entr, self.dataset_test, self.conjunto_val_10, self.conjunto_val_20, self.conjunto_val_30 = cargarDataset(dataset)
            self.mostrarPorConsola('>>Dataset cargado correctamente desde ' + path)
            self.mostrarPorConsola('>>Datasets de entrenamiento, test y validación creados correctamente')
            
            # Activo nuevas funciones
            self.activarEsto((self.groupBox_arquitectura, self.pushButton_verentr, self.pushButton_vertest, self.pushButton_verval10, self.pushButton_verval20, self.pushButton_verval30, self.label_verreddataset, self.pushButton_guardar))
            self.animarEsto((self.frame_arquitectura, self.frame_guardar, self.frame_validacion10, self.frame_botonesvarios))

            # # Para probar
            # print('Tamaño dataset full:', len(self.dataset_full))
            # print('Tamaño dataset test', len(self.dataset_test))
            # print('Tamaño dataset entrenamiento:', len(self.dataset_entr))
            # print('Tamaño conjunto val 10:', len(self.conjunto_val_10))
            # print('Tamaño conjunto val 20:', len(self.conjunto_val_20))
            # print('Tamaño conjunto val 30:', len(self.conjunto_val_30))


    def desactivarSeñales(self, valor):
        """Bloquea las señales producidas por cambios de valores en parámetros.
           (https://stackoverflow.com/questions/26358945/qt-find-out-if-qspinbox-was-changed-by-user)"""
        self.spinBox_capasOcultas.blockSignals(valor)
        self.spinBox_tamCapaOc1.blockSignals(valor)
        self.spinBox_tamCapaOc2.blockSignals(valor)
        self.comboBox_funcion.blockSignals(valor)
        self.doubleSpinBox_alfa.blockSignals(valor)
        self.doubleSpinBox_beta.blockSignals(valor)


    def tratarArquitecturaPredefinida(self):
        """Carga automáticamente los parámetros de la arquitectura predefinida seleccionada en el combobox."""
        
        # Desactivo señales disparadas con el cambio de valores para evitar que estos cambios disparen tratarCambioParametrosArg()
        # Esto hace que las señales se disparen solo por cambios manuales de valores (de otra forma, hay resultados no deseados)
        self.desactivarSeñales(True)

        # Cargo valores de arquitectura predefinida
        self.spinBox_capasOcultas.setValue(self.comboBox_arquitectura.currentData()['capasOcultas'])
        self.spinBox_tamCapaOc1.setValue(self.comboBox_arquitectura.currentData()['neurOcultas'][0])
        if self.comboBox_arquitectura.currentData()['capasOcultas'] == 2:
            self.spinBox_tamCapaOc2.setValue(self.comboBox_arquitectura.currentData()['neurOcultas'][1])
        self.comboBox_funcion.setCurrentText(self.comboBox_arquitectura.currentData()['funcTransf'])
        self.doubleSpinBox_alfa.setValue(self.comboBox_arquitectura.currentData()['alfa'])
        self.doubleSpinBox_beta.setValue(self.comboBox_arquitectura.currentData()['beta'])

        # Trato spin box de tamaño de capa oculta 2 y su label
        self.tratarSpinBoxCapaOculta2()

        # Vuelvo a activar las señales
        self.desactivarSeñales(False)


    def tratarCambioParametrosArq(self):
        """Por un lado comprueba, ante un cambio de parámetro, si los parametros coinciden con los de una arquitectura predefinida, y la selecciona.
           Por el otro, activa o desactiva el spinbox de tamaño de capa oculta 2 y su label, dependiendo del valor del número de capas ocultas."""

        # Si selecciono 1 capa oculta, no debe tener en cuenta las neuronas de la 2da. capa. Si seleccione 2, si.
        if self.spinBox_capasOcultas.value() == 1:
            neurOcultas = (self.spinBox_tamCapaOc1.value(),)
        else:
            neurOcultas = (self.spinBox_tamCapaOc1.value(), self.spinBox_tamCapaOc2.value())

        # Formo la arquitectura de los parámetros actuales
        arq_actual = {'capasOcultas': self.spinBox_capasOcultas.value(), 
                      'neurOcultas': neurOcultas, 
                      'funcTransf': self.comboBox_funcion.currentText(), 
                      'alfa': round(self.doubleSpinBox_alfa.value(), 1), 
                      'beta': round(self.doubleSpinBox_beta.value(), 1)}

        # Compruebo si coincide con una predefinida, y la selecciono en el combo box
        if arq_actual not in self.arquitecturasPredefinidas:
            self.comboBox_arquitectura.setCurrentIndex(-1) # No muestro ninguna arquitectura predefinida en el combo box
        else:
            ind = self.arquitecturasPredefinidas.index(arq_actual) # Busco la posición de la coincidencia
            self.comboBox_arquitectura.setCurrentIndex(ind) # Muestro en el combobox la arquitectura de esa posición

        # Trato spinbox de tamaño de capa oculta 2 y su label (porque desactivé la señal más arriba)
        self.tratarSpinBoxCapaOculta2()


    def tratarSpinBoxCapaOculta2(self):
        """Activa o desactiva el spinbox de tamaño de capa oculta 2 y su label, dependiendo del valor del número de capas ocultas."""
        if self.spinBox_capasOcultas.value() == 2:
            self.activarEsto((self.spinBox_tamCapaOc2, self.label_arquired5))
        else:
            self.desactivarEsto((self.spinBox_tamCapaOc2, self.label_arquired5))


    def crearRed(self):
        # Cargo características de la red
        self.tamCapaEnt = int(self.lineEdit_tamCapaEnt.text())
        self.tamCapaSal = int(self.lineEdit_tamCapaSal.text())
        self.capasOcultas = self.spinBox_capasOcultas.value()
        hay_2 = self.capasOcultas == 2
        self.neuronasPorCapa = [self.spinBox_tamCapaOc1.value()]
        if hay_2: self.neuronasPorCapa.append(self.spinBox_tamCapaOc2.value())
        if self.comboBox_funcion.currentText().lower() == 'lineal':
            self.funcionDeActivacionOc = 'lineal'
        else:
            self.funcionDeActivacionOc = 'sigmoidal'
        self.alfa = round(self.doubleSpinBox_alfa.value(), 1)
        self.beta = round(self.doubleSpinBox_beta.value(), 1)

        # Creo atributos auxiliares en base a las características
        self.nroCapas = self.capasOcultas + 2 # Capas ocultas + capa de entrada + capa de salida
        self.capaEnt = 0
        self.capaSal = self.capasOcultas + 1
        self.capaOc1 = 1
        self.tamCapaOc1 = self.neuronasPorCapa[0]
        if hay_2: 
            self.capaOc2 = 2
            self.tamCapaOc2 = self.neuronasPorCapa[1]

        # # Para probar
        # print('Nro total de capas:', self.nroCapas)
        # print('Tamaño de capa de entrada:',self.tamCapaEnt)
        # print('Tamaño de capa de salida:',self.tamCapaSal)
        # print('Capas ocultas:',self.capasOcultas)
        # print('Tamaño de capas ocultas:', self.neuronasPorCapa)
        # print('Tamaño capa oculta 1:', self.tamCapaOc1)
        # if hay_2:
        #     print('Tamaño capa oculta 2:', self.tamCapaOc2)
        # print('Funcion de activacion capas ocultas:', self.funcionDeActivacionOc)
        # print('Funcion de activacion capa salida:', self.funcionDeActivacionSal)
        # print('Alfa:', self.alfa)
        # print('Beta:', self.beta)
        # print('Nro capa entrada:', self.capaEnt)
        # print('Nro capa salida:', self.capaSal)
        # print('Nro capa oculta 1:', self.capaOc1)
        # if hay_2:
        #     print('Nro capa oculta 2:', self.capaOc2)

        # Creo la red
        self.red = crearRed(self.tamCapaEnt, self.capasOcultas, self.neuronasPorCapa, self.tamCapaSal)
        # # Para probar
        # imprimirRed(self.red)

        # Habilito el entrenamiento y botón para ver red
        self.activarEsto((self.groupBox_entrenamiento, self.pushButton_verred))
        self.animarEsto((self.frame_entrenamiento1, self.frame_verred))

        # Muestro mensaje por consola con información de la red creada
        if hay_2:
            cap_oc_2 = '\n*Tamaño capa oculta 2: ' + str(self.tamCapaOc2)
        else:
            cap_oc_2 = ''
        self.mostrarPorConsola('>>Red creada correctamente\n*Nro. total de capas: '+str(self.nroCapas)+'\n*Tamaño capa de entrada: '
                                +str(self.tamCapaEnt)+'\n*Tamaño capa oculta 1: '+str(self.tamCapaOc1)+'%s' %(cap_oc_2)
                                +'\n*Tamaño capa de salida: '+str(self.tamCapaSal)+'\n*Función de transf. de capa oculta: '
                                +self.funcionDeActivacionOc+'\n*Función de transf. de capa de salida: '+self.funcionDeActivacionSal
                                +'\n*Coeficiente de aprendizaje (α): '+str(round(self.alfa,1))+'\n*Término momento (β): '
                                +str(round(self.beta,1)))
        self.mostrarPorConsola('>>Red actual actualizada')


    def entrenarRed(self):
        """Hace el entrenamiento hasta obtener MSE por debajo de un error aceptable, o bien repitiendo por una cantidad de épocas ingresadas."""
        
        error = self.radioButton_erroracep.isChecked()
        epocas = self.radioButton_iteraciones.isChecked()
        
        if error: # Se seleccionó el combobox de error aceptable
            try: # Compruebo que el error aceptable ingresado tenga un formato correcto
                errorAcep = float(self.lineEdit_erroracep.text())
            except:
                self.mostrarPorConsola('>>El error aceptable debe ser un número positivo o cero')
            else:
                if errorAcep < 0:
                    self.mostrarPorConsola('>>El error aceptable debe ser un número positivo o cero')
                else: # El error tiene un formato correcto
                    conjuntoActual = 0
                    self.redesParaExportar = []
                    # Hago un entrenamiento por cada conjunto de validación
                    for conjunto_val in (self.conjunto_val_10, self.conjunto_val_20, self.conjunto_val_30):
                        errorNoAceptable = True # Bandera que me informa si algún patrón dio un error mayor al aceptable
                        dataset_entr_actual = restarDatasets(self.dataset_entr, conjunto_val) # Resto al de entrenamiento el conjunto de validación
                        self.vaciarRed() # Dejo la red vacía para iniciar un nuevo entrenamiento
                        nroEpocas = 0 # Contador de épocas
                        listaErroresEntrEpoca = [] # Para el gráfico de MSE vs épocas
                        listaErroresValEpoca = [] # Para el gráfico de MSE vs épocas
                        contErrorRepetido = 0 # Contador de errores repetidos
                        maxErrorRepetido = 20 # Número de errores repetidos seguidos a detectar
                        cifrasDecimales = 8 # Número de cifras decimales consideradas para verificar repetición en errores
                        conjuntoActual += 10

                        self.mostrarPorConsola('>>Entrenamiento con conjunto de validación de ' + str(conjuntoActual) + ' comenzado')
                        self.mostrarPorConsola('  Errores de entrenamiento:\n' + '  ' + '¯'*25)
                        
                        inicializarPesos(self.red)
                        # Si algún patrón tuvo error por encima del aceptable, comienzo una nueva época
                        while errorNoAceptable:
                            nroEpocas += 1
                            # if nroEpocas > 200: # Cuido que el entrenamiento termine en algún momento si no está convergiendo
                            #     self.mostrarPorConsola('>>Mas de 200 épocas...')
                            #     self.mostrarPorConsola('>>La red no se establizó')
                            #     nroEpocas -= 1
                            #     break
                            errorNoAceptable = False                      
                            sumErrorEntr = 0 # Acumula los errores de entrenamiento de 1 época
                            contFilas = 0 # Para graficar el progreso
                            
                            # Itero cada patrón del dataset_entr_actual
                            for fila in dataset_entr_actual:
                                contFilas += 1
                                aplicarPatronDeEntrada(fila, self.red)
                                calcularSalidasRed(self.funcionDeActivacionSal, self.funcionDeActivacionOc, self.red)
                                calcularTerminosErrorRed(self.funcionDeActivacionSal, self.funcionDeActivacionOc, self.red)
                                actualizarPesosRed(self.alfa, self.beta, self.red)
                                errorEntr = calcularMSE(self.red)
                                sumErrorEntr += errorEntr

                                # # Uso esto cuando el error aceptable es para cada patrón del dataset (como el algoritmo del libro)
                                # if errorEntr > errorAcep:
                                #     errorNoAceptable = True
                                #     # print('Epoca ' + str(nroEpocas))
                                #     # print('Error que superó:', errorEntr)

                                # No se cuántas épocas me llevará el entrenamiento, por lo que muestro el progreso por cada época
                                prog = ceil(contFilas*100/len(dataset_entr_actual))
                                self.progressBar_entrenamiento.setValue(prog)

                            # Terminé una época, calculo y guardo errores de entrenamiento y validación de la época
                            errorEntrEpoca = sumErrorEntr / len(dataset_entr_actual)
                            listaErroresEntrEpoca.append(errorEntrEpoca)
                            errorValEpoca = self.probarDataset(conjunto_val)[3]
                            listaErroresValEpoca.append(errorValEpoca)

                            # Uso esto cuando el error aceptable es para toda la época (error global)
                            if errorEntrEpoca > errorAcep:
                                errorNoAceptable = True
                                # print('Epoca ' + str(nroEpocas))
                                # print('Error que superó:', errorEntrEpoca)
                            
                            # Muestro por consola el error de entrenamiento de esta epoca
                            self.mostrarErrorEpoca(nroEpocas, errorEntrEpoca)
                            
                            # Controlo errores parecidos para generar alerta de parada de entrenamiento
                            if nroEpocas > 1:
                                # Formo los strings de los últimos 2 errores, hasta la "cifrasDecimales"-esima cifra decimal
                                errorAnterior = convertirErrorAString(listaErroresEntrEpoca[-2])[:cifrasDecimales+2] # +2 por la cifra entera y el punto
                                errorActual = convertirErrorAString(listaErroresEntrEpoca[-1])[:cifrasDecimales+2] # +2 por la cifra entera y el punto
                                # Comparo ambos trings e incremento el contador si hay coincidencia
                                if errorAnterior == errorActual:
                                    contErrorRepetido += 1
                                    # print(errorAnterior, errorActual, contErrorRepetido)
                                    if contErrorRepetido == maxErrorRepetido-1: # -1 porque el primer repetido no suma al contador
                                        contErrorRepetido = 0
                                        resp = self.generarAlerta(errorActual, maxErrorRepetido)
                                        if resp == 'parar':
                                            break # Salgo del entrenamiento si hubo "maxErrorRepetido" repeticiones del error
                                else:
                                    contErrorRepetido = 0

                        # Terminé entrenamiento para el conjunto de validación actual. Guardo listas de errores y muestro resultados
                        if conjuntoActual == 10:
                            # Guardo lista de errores para graficar
                            listaErroresEntrEpoca10 = listaErroresEntrEpoca
                            listaErroresValEpoca10 = listaErroresValEpoca
                            # Muestro resultados
                            self.lineEdit_nroepocas10.setText(str(nroEpocas)) # Número de épocas que llevó el entrenamiento
                            self.lineEdit_mseentr10.setText(f'{listaErroresEntrEpoca[-1]:.8f}') # Muestro error de entrenamiento de última época
                            self.lineEdit_msevalid10.setText(f'{listaErroresValEpoca[-1]:.8f}') # Muestro error de validación de última época
                            self.mostrarPorConsola('>>Entrenamiento con conjunto de validación de 10 terminado')
                        elif conjuntoActual == 20:
                            listaErroresEntrEpoca20 = listaErroresEntrEpoca
                            listaErroresValEpoca20 = listaErroresValEpoca
                            self.lineEdit_nroepocas20.setText(str(nroEpocas))
                            self.lineEdit_mseentr20.setText(f'{listaErroresEntrEpoca[-1]:.8f}') 
                            self.lineEdit_msevalid20.setText(f'{listaErroresValEpoca[-1]:.8f}') 
                            self.mostrarPorConsola('>>Entrenamiento con conjunto de validación de 20 terminado')
                        else:
                            listaErroresEntrEpoca30 = listaErroresEntrEpoca
                            listaErroresValEpoca30 = listaErroresValEpoca
                            self.lineEdit_nroepocas30.setText(str(nroEpocas))
                            self.lineEdit_mseentr30.setText(f'{listaErroresEntrEpoca[-1]:.8f}') 
                            self.lineEdit_msevalid30.setText(f'{listaErroresValEpoca[-1]:.8f}') 
                            self.mostrarPorConsola('>>Entrenamiento con conjunto de validación de 30 terminado')

                        # Guardo la red entrenada para poder usarla en la etapa de test o para probar patrones distorsionados
                        self.guardarRedEntrenada(conjuntoActual)

                    # Activo nuevas funciones disponibles por haber entrenado
                    self.finalizarEntrenamiento()

                    # Grafico errores de entrenamiento y validación vs épocas        
                    self.graficarErrores(listaErroresEntrEpoca10, listaErroresEntrEpoca20, listaErroresEntrEpoca30, listaErroresValEpoca10, listaErroresValEpoca20, listaErroresValEpoca30)                    
        
        else: # Se seleccionó el combo box de número fijo de iteraciones
            # Tomo el número de iteraciones ingresado
            nroEpocas = self.spinBox_iteraciones.value()

            conjuntoActual = 0
            self.redesParaExportar = []
            # Hago un entrenamiento por cada conjunto de validación
            for conjunto_val in (self.conjunto_val_10, self.conjunto_val_20, self.conjunto_val_30):
                dataset_entr_actual = restarDatasets(self.dataset_entr, conjunto_val) # Resto al de entrenamiento el conjunto de validacion
                self.vaciarRed() # Dejo la red vacia para iniciar un nuevo entrenamiento
                listaErroresEntrEpoca = [] # Para el gráfico de MSE vs épocas
                listaErroresValEpoca = [] # Para el gráfico de MSE vs épocas
                conjuntoActual += 10
                
                self.mostrarPorConsola('>>Entrenamiento con conjunto de validación de ' + str(conjuntoActual) + ' comenzado')
                self.mostrarPorConsola('  Errores de entrenamiento:\n' + '  ' + '¯'*25)
                
                inicializarPesos(self.red)
                # Itero "nroEpocas" veces el dataset_entr_actual
                for epoca in range(nroEpocas):
                    if nroEpocas > 1:
                        prog = ceil((epoca+1)*100/nroEpocas)
                        self.progressBar_entrenamiento.setValue(prog)
                    else: # Si se ingresa 1 sola época, se pausa la barra de progreso 0.02 seg para no hacerlo tan rápido
                        self.progressBar_entrenamiento.reset()
                        self.progressBar_entrenamiento.setValue(50)
                        sleep(0.02)
                        self.progressBar_entrenamiento.setValue(100)
                    sumErrorEntr = 0 # Acumula los errores de entrenamiento de 1 época

                    # Itero cada patrón del dataset_entr_actual
                    for fila in dataset_entr_actual:
                        aplicarPatronDeEntrada(fila, self.red)
                        calcularSalidasRed(self.funcionDeActivacionSal, self.funcionDeActivacionOc, self.red)
                        calcularTerminosErrorRed(self.funcionDeActivacionSal, self.funcionDeActivacionOc, self.red)
                        actualizarPesosRed(self.alfa, self.beta, self.red)
                        errorEntr = calcularMSE(self.red)
                        sumErrorEntr += errorEntr
                    
                    # Terminé una epoca, calculo y guardo errores de entrenamiento y validación de la época
                    errorEntrEpoca = sumErrorEntr / len(dataset_entr_actual)
                    listaErroresEntrEpoca.append(errorEntrEpoca)
                    errorValEpoca = self.probarDataset(conjunto_val)[3]
                    listaErroresValEpoca.append(errorValEpoca)

                    # Muestro por consola el error de entrenamiento de esta epoca
                    self.mostrarErrorEpoca(epoca+1, errorEntrEpoca)
                                    
                # Terminé entrenamiento para el conjunto de validación actual
                if conjuntoActual == 10:
                    # Guardo lista de errores para graficar
                    listaErroresEntrEpoca10 = listaErroresEntrEpoca
                    listaErroresValEpoca10 = listaErroresValEpoca
                    # Muestro resultados
                    self.lineEdit_nroepocas10.setText(str(nroEpocas)) # Número de épocas que llevó el entrenamiento
                    self.lineEdit_mseentr10.setText(f'{listaErroresEntrEpoca[-1]:.8f}') # Muestro error de entrenamiento de última época
                    self.lineEdit_msevalid10.setText(f'{listaErroresValEpoca[-1]:.8f}') # Muestro error de validación de última época
                    self.mostrarPorConsola('>>Entrenamiento con conjunto de validación de 10 terminado')
                elif conjuntoActual == 20:
                    listaErroresEntrEpoca20 = listaErroresEntrEpoca
                    listaErroresValEpoca20 = listaErroresValEpoca
                    self.lineEdit_nroepocas20.setText(str(nroEpocas))
                    self.lineEdit_mseentr20.setText(f'{listaErroresEntrEpoca[-1]:.8f}') 
                    self.lineEdit_msevalid20.setText(f'{listaErroresValEpoca[-1]:.8f}') 
                    self.mostrarPorConsola('>>Entrenamiento con conjunto de validación de 20 terminado')
                else:
                    listaErroresEntrEpoca30 = listaErroresEntrEpoca
                    listaErroresValEpoca30 = listaErroresValEpoca
                    self.lineEdit_nroepocas30.setText(str(nroEpocas))
                    self.lineEdit_mseentr30.setText(f'{listaErroresEntrEpoca[-1]:.8f}') 
                    self.lineEdit_msevalid30.setText(f'{listaErroresValEpoca[-1]:.8f}') 
                    self.mostrarPorConsola('>>Entrenamiento con conjunto de validación de 30 terminado')

                # Guardo la red entrenada para poder usarla en la etapa de test o para probar patrones distorsionados
                self.guardarRedEntrenada(conjuntoActual)

            # Activo nuevas funciones disponibles por haber entrenado
            self.finalizarEntrenamiento()

            # Grafico errores de entrenamiento y validación vs épocas
            self.graficarErrores(listaErroresEntrEpoca10, listaErroresEntrEpoca20, listaErroresEntrEpoca30, listaErroresValEpoca10, listaErroresValEpoca20, listaErroresValEpoca30)


    def mostrarErrorEpoca(self, nroEpocas, errorEntrEpoca):
        """Muestra por consola el error de entrenamiento de una época."""
        if nroEpocas < 10:
            espacio = 2
        elif nroEpocas < 100:
            espacio = 1
        else:
            espacio = 0
        self.consola.appendPlainText('  Época ' + str(nroEpocas) + ': ' + ' '*espacio + str(errorEntrEpoca))
        self.consola.moveCursor(QTextCursor.End)


    def guardarRedEntrenada(self, conj_val):
        """
        * Guarda una red entrenada para poder usarla en la etapa de test o para probar patrones distorsionados, y la lista.
        * Para listarla, comprueba si tiene una arquitectura predefinida. Si la tiene, busca el ítem de dicha arquitectura 
          en el combobox de "Arquitectura de la red" y obtiene el texto que la describe. Si no, forma la descripción. 
        * Además de la red, guarda su estructura (para actualizar atributos de clase cuando la cargo), el dataset de test, de 
          entrenamiento y el conjunto de validación correspondiente al entrenamiento, de manera de poder usarlos en cualquier 
          momento.
        """

        descrip, arq_actual = self.esArquitecturaPredefinida()
        if descrip == '': # La red actual no tiene una arquitectura predefinida, formo su descripción
            if self.capasOcultas == 1:
                str_N = str(self.neuronasPorCapa[0])
            else:
                str_N = str(self.neuronasPorCapa[0]) + ' y ' + str(self.neuronasPorCapa[1])
            descrip = 'CO = ' + str(self.capasOcultas) + '; N = ' + str_N + '; FT = ' + self.funcionDeActivacionOc.capitalize() + '; α = ' + str(self.alfa) + '; β = ' + str(self.beta)
        
        # Agrego el tamaño del dataset
        tamañoDatasetActual = str(len(self.dataset_entr) + len(self.dataset_test))
        descrip += ' (Dat ' + tamañoDatasetActual

        # Agrego el conjunto de validación que se usó
        if conj_val == 10:
            descrip += '; Val 10)'
            conjunto_usado = self.conjunto_val_10
        elif conj_val == 20:
            descrip += '; Val 20)'
            conjunto_usado = self.conjunto_val_20
        else:
            descrip += '; Val 30)'
            conjunto_usado = self.conjunto_val_30

        # Creo el ítem a listar
        item = (descrip, (self.red, arq_actual, self.dataset_test, self.dataset_entr, conjunto_usado))

        # Compruebo si una arquitectura idéntica ya está listada. Si ya existe una, la sobreescribo
        ind = -1
        for i in range(len(self.listaRedesEntrenadas)):
            if descrip in self.listaRedesEntrenadas[i]:
                ind = i
        if ind == -1: # No hay listada una arquitectura similar
            self.listaRedesEntrenadas.append(item)
            self.mostrarPorConsola('>>Se guardó una red nueva')
        else: # Ya hay listada una arquitectura similar
            self.listaRedesEntrenadas.pop(ind) # Remuevo la que ya existe
            self.listaRedesEntrenadas.insert(ind, item) # Inserto la nueva en la misma posición
            self.mostrarPorConsola('>>Se sobreescribió una red guardada previamente')

        # Guardo la red, su texto descriptivo y datasets asociados para poder exportarlos como archivo
        self.redesParaExportar.append(item)

        
    def tratarComboboxTipoModelo(self, combobox1, combobox2):
        """Carga la lista de redes precargadas o recién entrenadas en 'combobox2' de acuerdo a lo seleccionado en 
           'combobox1'. Ambos comboboxes pueden ser el par de la sección 'Test' o de la pestaña 'Probar patrón'."""

        # Limpio el combobox que lista las redes entrenadas/precargadas
        combobox2.clear()
        # Muestro la lista de redes precargadas o recién entrenadas, según lo seleccionado en el otro combobox
        if combobox1.currentIndex() == 1: # Se seleccionó la lista de redes recién entrenadas
            for item in self.listaRedesEntrenadas:
                combobox2.addItem(item[0], item[1])
        else: # Se seleccionó la lista de redes precargadas
            for item in self.listaRedesPrecargadas:
                combobox2.addItem(item[0], item[1])


    def esArquitecturaPredefinida(self):
        """Comprueba si la red actual tiene una arquitectura predefinida. Si la tiene, retorna el string que la describe, tal como está
           en el combobox de la sección "Arquitectura de la red". Si no, retorna string vacío. En ambos casos, retorna en segundo lugar
           la estructura de la arquitectura (necesaria par actualizar atributos al cargar una red)."""

        if self.capasOcultas == 1:
            neurOcultas = (self.neuronasPorCapa[0],)
        else:
            neurOcultas = (self.neuronasPorCapa[0], self.neuronasPorCapa[1])

        # Formo la arquitectura de los parámetros actuales
        arq_actual = {'capasOcultas': self.capasOcultas, 
                      'neurOcultas': neurOcultas, 
                      'funcTransf': self.funcionDeActivacionOc.capitalize(), 
                      'alfa': self.alfa, 
                      'beta': self.beta}

        # Compruebo si coincide con una predefinida, y la busco en el combobox para usar el texto que la describe
        if arq_actual not in self.arquitecturasPredefinidas:
            return '', arq_actual
        else:
            ind = self.arquitecturasPredefinidas.index(arq_actual) # Busco la posición de la coincidencia
            texto = self.comboBox_arquitectura.itemText(ind) # Guardo el texto del ítem de esa posición en el combobox
            return texto, arq_actual


    def finalizarEntrenamiento(self):
        """Lo que se hace al terminar el entrenamiento por cualquiera de las condiciones de fin."""
        if self.comboBox_tipomodelotest.currentIndex() == 1:
            self.tratarComboboxTipoModelo(self.comboBox_tipomodelotest, self.comboBox_test) # Para que actualice la lista de redes entrenadas
        if self.comboBox_tipomodeloprobar.currentIndex() == 1:
            self.tratarComboboxTipoModelo(self.comboBox_tipomodeloprobar, self.comboBox_probarpatron) # Para que actualice la lista de redes entrenadas
        self.mostrarPorConsola('>>Etapa de entrenamiento finalizada')
        self.activarEsto((self.groupBox_test, self.label_comboprobarpatron, self.comboBox_probarpatron, self.pushButton_guardarredesentrenadas))
        self.animarEsto((self.frame_entrenamiento3,))


    def guardarRedesEntrenadas(self):
        """Guarda las últimas redes entrenadas y datasets de entrenamiento, test y validación asociados en archivos .json"""

        # Creo la carpeta para guardar las redes
        try:
            os.mkdir('redes_entrenadas')
        except:
            pass
        # Creo los .json para las 3 redes entrenadas (1 por cada conjunto de validación)
        for red_entrenada in self.redesParaExportar:
            descrip = red_entrenada[0]
            f = open(f'redes_entrenadas\\{descrip}.json', 'w') # Creo el archivo .txt
            f.write(json.dumps(red_entrenada[1])) # Escribo el archivo
            f.close()
        # Muestro por consola confirmación de redes guardadas
        path = os.path.dirname(__file__) # Obtengo el path del ejecutable
        self.mostrarPorConsola(f'>>Redes entrenadas guardadas correctamente en {path}\\redes_entrenadas')


    def vaciarRed(self):
        """Asigna al atributo "red" una estructura de red vacía. Se usa para resetear la red en cada entrenamiento."""
        self.red = crearRed(self.tamCapaEnt, self.capasOcultas, self.neuronasPorCapa, self.tamCapaSal)
    

    def probarDataset(self, dataset):
        """Calcula la precisión de la clasificación con un dataset, y el MSE promedio al probarlo."""
        
        clasifCorrectas = 0
        sumError = 0
        listaErrores = []

        for fila in dataset:
            clasifCorrecta, error = self.probarPatron(fila)[0:2] # probarPatron() retorna en 1er. lugar 1 o 0 según la clasificación haya sido correcta, y en 2do. lugar el MSE del patrón
            clasifCorrectas += clasifCorrecta
            sumError += error
            listaErrores.append(error)
        
        precision = clasifCorrectas / len(dataset)
        errorPromedio = sumError / len(dataset)
        # print('Clasificaciones correctas:',clasifCorrectas)
        # print('Casos de prueba:',len(dataset))
        return precision, clasifCorrectas, listaErrores, errorPromedio


    def probarPatron(self, patron):
        """Presenta un patrón a la red, calcula la salida y el error, comprueba si la salida obtenida es igual a la deseada, y devuelve 1
           o 0 dependiendo de la coincidencia, el error, la salida obtenida convertida a binaria y sin convertir."""

        aplicarPatronDeEntrada(patron, self.red)
        calcularSalidasRed(self.funcionDeActivacionSal, self.funcionDeActivacionOc, self.red)
        error = calcularMSE(self.red)

        so1_float = self.red[-1][0]['salida'] # so1 = salida obtenida 1
        so2_float = self.red[-1][1]['salida'] # so2 = salida obtenida 2
        so3_float = self.red[-1][2]['salida'] # so3 = salida obtenida 3
        sd1 = self.red[-1][0]['salidaDeseada'] # sd1 = salida deseada1
        sd2 = self.red[-1][1]['salidaDeseada'] # sd2 = salida deseada2
        sd3 = self.red[-1][2]['salidaDeseada'] # sd3 = salida deseada3

        # Convierto la salida obtenida a binaria (para poder comparar con la deseada)
        mayor = max(so1_float, so2_float, so3_float)
        if mayor == so1_float:
            so1_bin, so2_bin, so3_bin = 1, 0, 0
        elif mayor == so2_float:
            so1_bin, so2_bin, so3_bin = 0, 1, 0
        else:
            so1_bin, so2_bin, so3_bin = 0, 0, 1
        
        # Compruebo si la salida obtenida es igual a la salida deseada
        if so1_bin == sd1 and so2_bin == sd2 and so3_bin == sd3:
            clasifCorrecta = 1
        else:
            clasifCorrecta = 0

        return clasifCorrecta, error, so1_bin, so2_bin, so3_bin, so1_float, so2_float, so3_float


    def graficarErrores(self, lErroresEntr10, lErroresEntr20, lErroresEntr30, lErroresVal10, lErroresVal20, lErroresVal30):
        """Genera 3 gráficos, comparando en cada uno los MSE promedio (de entrenamiento y validación) contra las épocas."""

        # Gráfico 1
        yEntr = np.array(lErroresEntr10)
        yVal = np.array(lErroresVal10)
        plt.subplot(3, 1, 1)
        plt.plot(yEntr, label="Error de entrenamiento")
        plt.plot(yVal, label="Error de validación 10")
        plt.ylabel("MSE promedio", fontsize=9)
        plt.tick_params(axis='both', labelsize=8)
        plt.legend(fontsize=8)

        # Gráfico 2
        yEntr = np.array(lErroresEntr20)
        yVal = np.array(lErroresVal20)
        plt.subplot(3, 1, 2)
        plt.plot(yEntr, label="Error de entrenamiento")
        plt.plot(yVal, label="Error de validación 20")
        plt.ylabel("MSE promedio", fontsize=9)
        plt.tick_params(axis='both', labelsize=8)
        plt.legend(fontsize=8)

        # Gráfico 3
        yEntr = np.array(lErroresEntr30)
        yVal = np.array(lErroresVal30)
        plt.subplot(3, 1, 3)
        plt.plot(yEntr, label="Error de entrenamiento")
        plt.plot(yVal, label="Error de validación 30")
        plt.xlabel("Épocas", fontsize=9)
        plt.ylabel("MSE promedio", fontsize=9)
        plt.tick_params(axis='both', labelsize=8)
        plt.legend(fontsize=8)

        plt.show()


    def hacerTest(self):
        """Toma del combobox la red guardada seleccionada, prueba el dataset de test en ella, muestra resultados de precisión 
           y el gráfico de error de test."""

        # Actualizo red actual y sus atributos en base a la red seleccionada, y guardo el dataset de test correspondiente a su entrenamiento
        dataset_test = self.dataset_test_resg

        # Pruebo y calculo resultados
        precision, correctas, listaErrores = self.probarDataset(dataset_test)[0:3]
        self.lineEdit_testcorrectas.setText(str(correctas))
        self.lineEdit_testtotal.setText(str(len(dataset_test)))
        self.lineEdit_testprec.setText(f'{precision:.2%}')
        self.mostrarPorConsola('>>Etapa de test finalizada')

        # Grafico el error de test
        ypoints  = np.array(listaErrores)
        plt.plot(ypoints, label="Error de test")
        plt.xlabel("Patrones", fontsize=9)
        plt.ylabel("MSE", fontsize=9)
        plt.tick_params(axis='both', labelsize=8)
        plt.legend(fontsize=8)
        plt.show()


    def tratarComboboxTest(self):
        """Activa el resto de la sección "Test", carga como red actual la red seleccionada en el combobox, y resguarda el dataset de test
           correspondiente al entrenamiento de la red cargada para poder usarlo en la etapa de test."""
        
        # Activo el resto de la sección "Test"
        self.activarEsto((self.pushButton_hacertest, self.label_testresult, self.label_testcorrectas, self.label_testtotal, self.label_testprec, self.lineEdit_testcorrectas, self.lineEdit_testtotal, self.lineEdit_testprec, self.pushButton_verred))
        self.animarEsto((self.frame_test, self.frame_verred))
        
        # Cargo como red actual la red seleccionada, y resguardo el dataset de test
        self.dataset_test_resg = self.cargarRedSeleccionada(self.comboBox_test)[0]


    def cargarRedSeleccionada(self, combobox):
        """Carga en la red actual la red seleccionada en el combobox pasado, y retorna los datasets de entrenamiento, test
           y validación usados en el entrenamiento de la red cargada."""

        # Tomo la red seleccionada en el combobox, su arquitectura, y el dataset de test correspondiente a su entrenamiento
        red, arquitectura, dataset_test, dataset_entr, conj_val = combobox.currentData()

        # Actualizo la red actual y sus atributos
        self.red = red
        self.capasOcultas = arquitectura['capasOcultas']
        self.neuronasPorCapa = list(arquitectura['neurOcultas'])
        self.funcionDeActivacionOc = arquitectura['funcTransf'].lower()
        self.alfa = arquitectura['alfa']
        self.beta = arquitectura['beta']
        self.mostrarPorConsola('>>Red actual actualizada')

        return dataset_test, dataset_entr, conj_val



    # MÉTODOS PARA LA SEGUNDA PESTAÑA


    def tratarComboboxProbarpatron(self):
        """Activa nuevas funciones de la pestaña "Probar patrón", y carga como red actual la red seleccionada en el combobox."""

        # Activo nuevas funciones
        self.activarEsto((self.groupBox_probar1patron, self.groupBox_probarmasde1, self.pushButton_verred))
        self.animarEsto((self.frame_probarpatron1, self.frame_probarpatrones))
        self.graphicsView.setStyleSheet('border: 1px solid black;')
        self.graphicsView_2.setStyleSheet('border: 1px solid black;')
        self.label_clasificacion2.setStyleSheet('background-color: rgb(255, 255, 255);border-width: 1px;border-style: solid;border-color: black;')

        # Cargo como red actual la red seleccionada, y resguardo los datasets de entrenamiento y validación usados en su entrenamiento
        self.dataset_entr_resg, self.conj_val_resg = self.cargarRedSeleccionada(self.comboBox_probarpatron)[1:]


    def tratarLineEditSlider(self, value):
        """Traslada valor del slider al lineedit."""
        self.lineEdit_sliderprobar1.setText(str(value))


    def tratarLetra(self, patron, letra):
        """Se llama cuando se presiona el botón de una letra."""
        self.mostrarPorConsola('>>Letra "' + letra + '" seleccionada')
        self.setLetraIngresada(letra)
        self.mostrarLetra(patron, self.labels_matriz1)


    def setLetraIngresada(self, letra):
        self.letraIngresada = letra


    def getLetraIngresada(self):
        return self.letraIngresada


    def mostrarLetra(self, patron, matriz):
        """Pinta la matriz de pixeles de acuerdo al patrón pasado."""
        self.borrarLetra(matriz)        
        labels = matriz
        for i in range(len(patron)):
            if patron[i] == 1:
                labels[i].setStyleSheet("background-color:black")
                # print(labels[i].objectName()) # Por si quiero ver qué labels modifica


    def borrarLetra(self, matriz):
        """Pone en blanco la matriz de pixeles."""
        labels = matriz
        for label in labels:
            label.setStyleSheet("background-color:white")


    def generarDistorsion(self):
        """Se llama cuando presiono el botón "Distorsionar". Muestra la letra distorsionada en la 1ra matriz de la 2da pestaña."""
        if self.letraIngresada == '':
            self.mostrarPorConsola('>>Debe seleccionar una letra!')
        else:
            letra = self.getLetraIngresada()
            patron = self.copiarPatron(letra)
            distorsion = int(self.lineEdit_sliderprobar1.text())
            generarDistorsion(patron, distorsion)
            self.guardarPatronDistorsionado(patron)
            self.mostrarLetra(patron, self.labels_matriz1)
            if distorsion == 0:
                self.mostrarPorConsola(">>No hubo distorsión")
            else:    
                self.mostrarPorConsola('>>Letra "' + letra + '" distorsionada un ' + str(distorsion) + '%')        
            usado = self.comprobarPatron(patron, letra) # Compruebo si el patrón fue usado para entrenar
            if usado:
                self.lineEdit_usado.setText('Si')
            else:
                self.lineEdit_usado.setText('No')

            # Activo la parte de clasificación (a la derecha de la 1ra matriz de pixeles)
            self.activarEsto((self.label_salida_clasif, self.pushButton_clasificar, self.label_yb, self.lineEdit_yb, self.label_yd, self.lineEdit_yd, self.label_yf, self.lineEdit_yf))
            self.animarEsto((self.frame_probarpatron2,))
            self.label_clasificacion1.setStyleSheet('background-color: rgb(255, 255, 255);border-width: 1px;border-style: solid;border-color: black;')


    def copiarPatron(self, letra):
        """Devuelve una copia del patrón sin distorsionar de la letra pasada."""
        if letra == 'b':
            patron = patronb.copy() 
        elif letra == 'd':
            patron = patrond.copy()
        else:
            patron = patronf.copy()
        return patron


    def guardarPatronDistorsionado(self, patron):
        self.patronDistorsionado = patron.copy()


    def comprobarPatron(self, patron, letra):
        """Comprueba si un patrón fue usado para el entrenamiento."""
        
        # Obtengo los ejemplos usados en el entrenamiento de la red actual
        resta = restarDatasets(self.dataset_entr_resg, self.conj_val_resg)

        if letra == 'b':
            patron_con_clases = patron + [1,0,0]
        elif letra == 'd':
            patron_con_clases = patron + [0,1,0]
        else:
            patron_con_clases = patron + [0,0,1]
        
        if patron_con_clases in resta:
            return True
        else:
            return False


    def clasificarPatron(self, patron, label, probarPatrones):
        """Presenta un patrón a la red y muestra la letra que representa la salida de la misma."""

        # Agrego 3 valores de clase cualquiera para que funcione correctamente aplicarPatronDeEntrada()
        patron_de_prueba = patron.copy()
        patron_de_prueba += [0,0,0] 

        so1_bin, so2_bin, so3_bin, so1_float, so2_float, so3_float = self.probarPatron(patron_de_prueba)[2:] # probarPatron() retorna, desde la posición 2, la salida en forma binaria y decimal de la red al aplicar un patrón

        if so1_bin == 1:
            label.setText('b')
        elif so2_bin == 1:
            label.setText('d')
        else:
            label.setText('f')
        if not probarPatrones: # Solamente cuando no estoy probando patrones (matrices de pixeles de abajo), muestro las salidas obtenidas
            # print('yb:', so1_float, 'yd:', so2_float, 'yf:', so3_float)
            self.lineEdit_yb.setText(f'{so1_float:.2%}')
            self.lineEdit_yd.setText(f'{so2_float:.2%}')
            self.lineEdit_yf.setText(f'{so3_float:.2%}')
            self.mostrarPorConsola('>>Patrón clasificado')


    def probarPatrones(self):
        """Clasifica un número dado de patrones aleatorios y muestra la precisión."""

        nroPatrones = self.spinBox_pataprobar.value()
        dataset = []

        # Genero un dataset con la cantidad de patrones aleatorios del spinbox, sin patrones usados para entrenar
        i = 1
        while i <= nroPatrones:
            letra = random.choice(['b','d','f'])
            distorsion = random.randint(0, 30)
            patron = self.copiarPatron(letra)
            generarDistorsion(patron, distorsion)
            usado = self.comprobarPatron(patron, letra)
            if usado:
                continue
            if letra == 'b':
                clases = [1,0,0]
            elif letra == 'd':
                clases = [0,1,0]
            else:
                clases = [0,0,1]
            patron += clases
            dataset.append(patron)
            i += 1

        # Grafico patrones distorsionados y clasificación, uno detrás de otro, con algunos mseg de pausa entre cada uno
        contFilas = 0 # Para graficar el progreso
        for patron in dataset:
            contFilas += 1
            self.mostrarLetra(patron[:-3], self.labels_matriz2) # Muestro la letra en 2da matriz de pixeles
            self.clasificarPatron(patron[:-3], self.label_clasificacion2, True) # Muestro clasificación de la letra
            prog = ceil(contFilas*100/len(dataset)) # Calculo progreso
            self.progressBar_probarpatrones.setValue(prog) # Grafico progreso
            QtTest.QTest.qWait(100) # Genero delay para animar la graficación de la matriz de pixeles
        
        # Uso probarDataset() para obtener las clasificaciones correctas y la precisión
        precision, clasifCorrectas = self.probarDataset(dataset)[0:2]

        # Muestro resultados
        self.lineEdit_probar_correctas.setText(str(clasifCorrectas))
        self.lineEdit_probar_total.setText(str(nroPatrones))
        self.lineEdit_probar_precision.setText(f'{precision:.2%}')
        self.mostrarPorConsola('>>Prueba de patrones finalizada')



    # MÉTODOS PARA VER CONTENIDO DE LA RED Y DE DATASETS


    def verDataset(self, dataset):
        """Abre una ventana con el dataset pasado mostrado en forma tabular y gráfica."""
        self.window_dataset = UIDialog_dataset
        self.window_dataset.show()
        self.window_dataset.plainTextEdit_tabular.clear()
        self.window_dataset.plainTextEdit_grafico.clear()
        imprimirDatasetTabular(dataset)
        imprimirDatasetGraficoConAsteriscos(dataset)
        self.window_dataset.plainTextEdit_tabular.moveCursor(QTextCursor.Start)
        self.window_dataset.plainTextEdit_grafico.moveCursor(QTextCursor.Start)
        
    def verRed(self):
        """Abre una ventana que muestra la estructura y contenido actual de la red."""
        self.window_red = UIDialog_red
        self.window_red.show()
        self.window_red.plainTextEdit_red.clear()
        imprimirRed(self.red)
        self.window_red.plainTextEdit_red.moveCursor(QTextCursor.Start)


# Para ventana de impresión de dataset
class UI_dialog_dataset(QDialog):
    def __init__(self):
        super(UI_dialog_dataset, self).__init__()

        # Cargamos el archivo .ui
        uic.loadUi(resource_path("ui\\uidataset.ui"), self)

        # Hacemos inicializaciones
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ver dataset') # Título de la ventana
        self.center() # Centramos ventana
        self.setWindowIcon(QIcon(resource_path('icons\\icon3.ico'))) # Ícono de la ventana

    def center(self):
        """Hace que la ventana aparezca centrada."""
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


# Para ventana de impresión de red
class UI_dialog_red(QDialog):
    def __init__(self):
        super(UI_dialog_red, self).__init__()

        # Cargamos el archivo .ui
        uic.loadUi(resource_path("ui\\uired.ui"), self)
        
        # Hacemos inicializaciones
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ver red neuronal') # Título de la ventana
        self.center() # Centramos ventana
        self.setWindowIcon(QIcon(resource_path('icons\\icon2.ico'))) # Ícono de la ventana

    def center(self):
        """Hace que la ventana aparezca centrada."""
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())




# ***********************************************************
# PROGRAMA PRINCIPAL
# ***********************************************************


'''
Posiciones ocupadas por cada letra, considerando la matriz como una lista de 100 elementos (del 0 al 99)
 ____________________ ____________________ ____________________
|                    |                    |                    |
|    12              |              17    |          1516      |
|    22              |              27    |        24    27    |
|    32              |              37    |        34          |
|    4243444546      |      4344454647    |    4243444546      |
|    52        57    |    52        57    |        54          |
|    62        67    |    62        67    |        64          |
|    72        77    |    72        77    |        74          |
|    8283848586      |      8384858687    |        84          |
|                    |                    |                    |
 ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ '''
posb = [12,22,32,42,43,44,45,46,52,57,62,67,72,77,82,83,84,85,86]
posd = [17,27,37,43,44,45,46,47,52,57,62,67,72,77,83,84,85,86,87]
posf = [15,16,24,27,34,42,43,44,45,46,54,64,74,84]

# Inicializo los patrones de cada letra
patronb, patrond, patronf = inicializarPatrones()

# Inicializamos la app
app = QApplication(sys.argv)
UIWindow = UI()
UIDialog_dataset = UI_dialog_dataset()
UIDialog_red = UI_dialog_red()
app.exec_()