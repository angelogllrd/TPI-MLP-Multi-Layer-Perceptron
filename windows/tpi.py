# -*- coding: utf-8 -*-

# Lista de widgets disponible en Formulario -> View Python Code, del Designer
from PyQt5.QtWidgets import QMainWindow, QAbstractSpinBox, QApplication, QDoubleSpinBox, QFormLayout, QGraphicsView, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLayout, QLineEdit, QMainWindow, QPlainTextEdit, QPushButton, QRadioButton, QSizePolicy, QSlider, QSpinBox, QStatusBar, QTabWidget, QVBoxLayout, QWidget, QFileDialog, QDesktopWidget, QDialog
from PyQt5.QtGui import QTextCursor, QIcon # Para moverme hasta arriba en los QPlainTextEdit donde se muestran la red y datasets
from PyQt5 import uic
from PyQt5 import QtCore # Para usar expresiones regulares con QRegularExpression
from PyQt5 import QtTest # Para generar delays

import sys, os, random

from math import exp, floor, ceil

from time import sleep

import matplotlib.pyplot as plt
import numpy as np



# Para no tener problemas con las rutas en la conversion a .exe 
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
# FUNCIONES PARA CREACION E IMPRESION DE PATRONES Y DATASETS
# ***********************************************************


def inicializarPatrones():
    # Devuelve los patrones de las 3 letras, en forma de listas de 100 elementos con 1 y 0
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
    return b,d,f


def imprimirMatriz(patron):
    # Recibe un patron e imprime la matriz de pixeles
    UIWindow.window_dataset.plainTextEdit_grafico.appendPlainText(' __________ ') # print(' __________ ')
    for f in range(10):
        fila = '|'
        for c in range(10):
            if patron[f*10+c] == 0: # f*10+c transforma una posicion fila-columna a una posicion 0-99 del patron
                fila += ' '
            else:
                fila += '*'
        UIWindow.window_dataset.plainTextEdit_grafico.appendPlainText(fila+'|') # print(fila+'|')
    UIWindow.window_dataset.plainTextEdit_grafico.appendPlainText(' ¯¯¯¯¯¯¯¯¯¯ ') # print(' ¯¯¯¯¯¯¯¯¯¯ ')


def generarDistorsion(patron, porc):
    # Distorsiona el patron pasado un porc% (cambia "porc" veces 0 por 1, y 1 por 0)
    pos_anterior = []
    for pixel in range(porc):
        while True:
            pos = random.randint(0,99)
            if pos not in pos_anterior: # Solamente distorsiono pixeles que todavia no distorsione
                break
        pos_anterior.append(pos) # Guardo posicion para no volver a distorsionarla
        if patron[pos] == 0:
            patron[pos] = 1
        else:
            patron[pos] = 0


def generarDataset(ejemplos):
    '''
    * Genera un dataset con el nro de ejemplos pasado, cumpliendo 10% sin distorsion, y el resto distorsionado 1%-30%. 
      El dataset es una lista de listas, donde cada sublista es un patron de entrada o fila del dataset. 
      Para asegurar que los conjuntos de test y validacion sean representativos, se genera de la siguiente manera,
      quedando 4 porciones de cada tipo de ejemplo:
             ____________________ _
            | 10% sin distorsion | --> Contiene las 3 letras agregadas de manera "ciclica", comenzando por una al azar
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
      
    * Los datasets de test y validacion se crean incluyendo ejemplos de cada porcion, lo mas similares posibles en tamaño.    
    * Retorna el dataset completo, y los conjuntos de entrenamiento, test, y validacion.
    '''
    
    dataset = []

    porc_test = 0.08 # Debe ser un porcentaje que haga divisible por 4 (4 porciones representativas) el numero de ejemplos de test para 100, 500 y 1000.
                     # Con 12% para test, los restantes ejemplos NO alcanzan para conseguir formar conjuntos de validacion representativos.
                     # Tomar el 8% SI permite formar todos los conjuntos de validacion representativos para los 3 datasets (segun calculos).
    
    sin_dist = int(ejemplos * 0.10) # Cantidad de ejemplos sin distorsion
    con_dist_por_rango = int((ejemplos-sin_dist)/3) # Cantidad de ejemplos para los rangos de distorsion (1-10%, 11-20% y 21-30%)

    letras = [['b',patronb,[1,0,0]], ['d',patrond,[0,1,0]], ['f',patronf,[0,0,1]]] 
    random.shuffle(letras) # Para que la porcion sin distorsion no comience siempre por "b", porque el 10% de 100, 500 y 1000 no es divisible por 3 y nunca queda igual cantidad de cada letra
    ind = 0 # Para recorrer "letras" en forma ciclica

    # GENERO EL DATASET PRINCIPAL
    for ejemplo in range(ejemplos):
        # Sin distorsion
        if ejemplo < sin_dist:
            letra = letras[ind][0]
            patron = letras[ind][1].copy()
            clases = letras[ind][2]
            if ind < 2:
                ind += 1
            else: 
                ind = 0
        else:
            # Con distorsion por rangos
            letra_aleatoria = random.choice(letras) # Cuando hay distorsion, selecciono letra al azar
            letra = letra_aleatoria[0]
            patron = letra_aleatoria[1].copy() # Copio el patron sin distorsionar de la letra
            clases = letra_aleatoria[2]
            if ejemplo < sin_dist+con_dist_por_rango:
                distorsión_aleatoria = random.randint(1, 10) # Distorsion aleatoria del 1-10%
            elif ejemplo < sin_dist+con_dist_por_rango*2:
                distorsión_aleatoria = random.randint(11, 20) # Distorsion aleatoria del 11-20%
            elif ejemplo < ejemplos:
                distorsión_aleatoria = random.randint(21, 30) # Distorsion aleatoria del 21-30%
            generarDistorsion(patron, distorsión_aleatoria) # Distorsiono el patron
        dataset.append(patron+clases) # Lo agrego al dataset principal

        # # Esto imprime las matrices, junto con la letra y la distorsion a medida que las genera (solamente para probar)
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

    # QUITO DE LAS PORCIONES LOS EJEMPLOS QUE CARGUE EN EL DATASET DE TEST, Y FORMO DATASET DE ENTRENAMIENTO
    parte_sin_dist = parte_sin_dist[etpp:]
    parte_dist_1_10 = parte_dist_1_10[etpp:]
    parte_dist_11_20 = parte_dist_11_20[etpp:]
    parte_dist_21_30 = parte_dist_21_30[etpp:]
    dataset_entr = parte_sin_dist + parte_dist_1_10 + parte_dist_11_20 + parte_dist_21_30 

    # GENERO LOS CONJUNTOS DE VALIDACION
    for porc_valid in [0.1, 0.2, 0.3]:
        # Genero el conjunto de acuerdo al porcentaje
        ev = int(ejemplos * porc_valid) # ev = ejemplos_validacion
        if (ev % 4) == 0: # Cantidad de ejemplos del conjunto de validacion es divisible por 4, porciones iguales
            evpp = int(ev/4)  # evpp = ejemplos_validacion_por_porcion
            conj = parte_sin_dist[:evpp] + parte_dist_1_10[:evpp] + parte_dist_11_20[:evpp] + parte_dist_21_30[:evpp]
        else: # Cantidad de ejemplos del conjunto de validacion NO divisible por 4, porciones distintas
            evpp1 = floor(ev/4) 
            evpp2 = evpp1 + 1
            l_evpp = [evpp1, evpp1, evpp2, evpp2] # Ejemplos de validacion = evpp1*2 + evpp2*2
            random.shuffle(l_evpp) # Para que los ejemplos que tomo de cada porcion no sean siempre los mismos
            conj = parte_sin_dist[:l_evpp[0]] + parte_dist_1_10[:l_evpp[1]] + parte_dist_11_20[:l_evpp[2]] + parte_dist_21_30[:l_evpp[3]]
        
        # # Para probar
        # print('Cantidad de ejemplos del conjunto de validacion de', int(porc_valid*100),'%:', len(conj))
        # imprimirDataset1(conj)

        # Asigno el conjunto en su correspondiente variable
        if porc_valid == 0.1:
            conj_val10 = conj
        elif porc_valid == 0.2:
            conj_val20 = conj
        else:
            conj_val30 = conj

    return dataset, dataset_entr, dataset_test, conj_val10, conj_val20, conj_val30

'''
def generarDataset(ejemplos):   
    # Lo mismo que la anterior, pero hace la seleccion de los ejemplos de los conjuntos de test y validacion
    # de manera ALEATORIA, es decir, no asegura que tengan la misma cantidad de cada una de las 4 porciones.
    
    dataset = []
    sin_distorsionar = ejemplos * 0.10
    porc_test = 0.2 # A diferencia del anterior generarDataset(), podemos poner diferentes porcentajes

    # GENERO EL DATASET PRINCIPAL
    for ejemplo in range(ejemplos):
        letra = random.choice(['b','d','f'])
        if letra == 'b':
            patron = patronb.copy()
            clases = [1,0,0]
        elif letra == 'd':
            patron = patrond.copy()
            clases = [0,1,0]
        else:
            patron = patronf.copy()
            clases = [0,0,1]
        
        if ejemplo >= sin_distorsionar: # Si ya genere mas del 10% de ejemplos, distorsiono entre 1% y 30%
            distorsión_aleatoria = random.randint(1, 30)
            generarDistorsion(patron, distorsión_aleatoria)
        dataset.append(patron+clases)
        
        # # Esto imprime las matrices, junto con la letra y la distorsion a medida que las genera (solamente para probar)
        # imprimirMatriz(patron)
        # print('Ejemplo:',ejemplo+1)
        # print('Letra:', letra)
        # print('Distorsion: ', end='')
        # if ejemplo < sin_distorsionar:
        #   print('Sin distorsionar')
        # else:
        #   print(distorsión_aleatoria,'%')

    dataset_entr = dataset.copy()
    random.shuffle(dataset_entr) # Mezclo aleatoriamente los patrones

    # GENERO EL DATASET DE TEST
    et = int(ejemplos * porc_test) # et = ejemplos_test
    dataset_test = dataset_entr[:et]

    # QUITO LOS EJEMPLOS CARGADOS EN EL DATASET DE TEST (EL DATASET RESULTANTE ES EL DE ENTRENAMIENTO)
    dataset_entr = dataset_entr[et:]

    # GENERO LOS CONJUNTOS DE VALIDACION
    for porc_valid in [0.1, 0.2, 0.3]:
        ev = int(ejemplos * porc_valid) # ev = ejemplos_validacion
        conj = dataset_entr[:ev]

        if porc_valid == 0.1:
            conj_val10 = conj
        elif porc_valid == 0.2:
            conj_val20 = conj
        else:
            conj_val30 = conj

    return dataset, dataset_entr, dataset_test, conj_val10, conj_val20, conj_val30
'''

def cargarDataset(dataset):
    # Se usa en la 1ra pestaña, con el boton "Cargar". Toma un dataset "full" (con los 100, 500 o 1000 ejemplos, sin mezclar, 
    # sin repartir en test, validacion, etc) y extrae los demas datasets usando la misma logica que el primer generarDataset(). 

    ejemplos = len(dataset)
    porc_test = 0.08
    
    sin_dist = int(ejemplos * 0.10) # Cantidad de ejemplos sin distorsion
    con_dist_por_rango = int((ejemplos-sin_dist)/3) # Cantidad de ejemplos para los rangos de distorsion (1-10%, 11-20% y 21-30%)

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

    # QUITO DE LAS PORCIONES LOS EJEMPLOS QUE CARGUE EN EL DATASET DE TEST, Y FORMO DATASET DE ENTRENAMIENTO
    parte_sin_dist = parte_sin_dist[etpp:]
    parte_dist_1_10 = parte_dist_1_10[etpp:]
    parte_dist_11_20 = parte_dist_11_20[etpp:]
    parte_dist_21_30 = parte_dist_21_30[etpp:]
    dataset_entr = parte_sin_dist + parte_dist_1_10 + parte_dist_11_20 + parte_dist_21_30 

    # GENERO LOS CONJUNTOS DE VALIDACION
    for porc_valid in [0.1, 0.2, 0.3]:
        # Genero el conjunto de acuerdo al porcentaje
        ev = int(ejemplos * porc_valid) # ev = ejemplos_validacion
        if (ev % 4) == 0: # Cantidad de ejemplos del conjunto de validacion es divisible por 4, porciones iguales
            evpp = int(ev/4)  # evpp = ejemplos_validacion_por_porcion
            conj = parte_sin_dist[:evpp] + parte_dist_1_10[:evpp] + parte_dist_11_20[:evpp] + parte_dist_21_30[:evpp]
        else: # Cantidad de ejemplos del conjunto de validacion NO divisible por 4, porciones distintas
            evpp1 = floor(ev/4) 
            evpp2 = evpp1 + 1
            l_evpp = [evpp1, evpp1, evpp2, evpp2] # Ejemplos de validacion = evpp1*2 + evpp2*2
            random.shuffle(l_evpp) # Para que los ejemplos que tomo de cada porcion no sean siempre los mismos
            conj = parte_sin_dist[:l_evpp[0]] + parte_dist_1_10[:l_evpp[1]] + parte_dist_11_20[:l_evpp[2]] + parte_dist_21_30[:l_evpp[3]]

        # Asigno el conjunto en su correspondiente variable
        if porc_valid == 0.1:
            conj_val10 = conj
        elif porc_valid == 0.2:
            conj_val20 = conj
        else:
            conj_val30 = conj

    return dataset_entr, dataset_test, conj_val10, conj_val20, conj_val30


def convertirStringADataset(string):
    # Convierte una string de lista de listas a una estructura de lista de listas.
    # Se usa cuando se carga un dataset desde un .txt
    pos = -1
    dataset = []
    while True:
        fila= []
        for i in range(103):
            pos += 3
            #print(pos, string[pos], i)
            fila.append(int(string[pos]))
        dataset.append(fila)
        if string[pos+2] == ']':
            break
        else:
            pos += 2
    return dataset


def imprimirDataset1(dataset):
    # Imprime el dataset en forma gráfica (matrices de los patrones)
    for fila in dataset:
        imprimirMatriz(fila)


def imprimirDataset2(dataset):
    # Imprime el dataset en forma tabular
    nombres_col1 = ''
    for i in range(10):
        nombres_col1 += str(i)+'         '
    UIWindow.window_dataset.plainTextEdit_tabular.appendPlainText(nombres_col1) # print('\n'+nombres_col1)
    nombres_col2 = '0123456789'*10 + ' yb yd yf'
    UIWindow.window_dataset.plainTextEdit_tabular.appendPlainText(nombres_col2) # print(nombres_col2)
    UIWindow.window_dataset.plainTextEdit_tabular.appendPlainText('-'*109) # print('-'*109)
    
    for fila in dataset:
        str_fila = ''
        for pixel in range(len(fila)-3):
            str_fila += str(fila[pixel])
        str_fila += '  ' + str(fila[-3]) + '  ' + str(fila[-2]) + '  ' + str(fila[-1])
        UIWindow.window_dataset.plainTextEdit_tabular.appendPlainText(str_fila) # print(str_fila)


def restarDatasets(aEste, restaleEste):
    # Quita de un dataset filas de otro (lo uso para restar al conjunto de entrenamiento los de validacion)
    aEste2 = aEste[:] # Para no modificar la lista "aEste" original, la copio en una nueva y elimino lo que quiero de la copia
    for fila in restaleEste:
        aEste2.remove(fila) # No hace falta comprobar que "fila" este en "aEste" porque son filas extraidas originalmente de "aEste"
    return aEste2



# ***********************************************************
# CREACION DE LA RED Y DE FUNCIONES PARA EL ALGORITMO
# ***********************************************************


def crearRed(neuronasDeEntrada, nroCapasOcultas, neuronasPorCapaOculta, neuronasDeSalida):
    # Crea la estructura de la red, con las neuronas de cada capa
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
                    'cambiosPeso': [], # Para calculo del termino momento
                    'net': 0,
                    'salida': 0,
                    'salidaDeseada': 0,
                    'delta': 0
                }
            else: # Creo neurona de capa oculta
                n = {
                    'pesos': [], # Pesos de conexiones de unidades de la capa anterior con esta unidad
                    'cambiosPeso': [], # Para calculo del termino momento
                    'net': 0,
                    'salida': 0,
                    'delta': 0
                }
            c.append(n)
        red.append(c)
    return red


def imprimirRed1(red):
    # Muestra el contenido de la red en su estado actual, por cada capa
    for capa in range(len(red)):
        if capa == 0:
            print('Capa de entrada:')
        elif capa == len(red)-1:
            print('\nCapa de salida:')
        else:
            print('\nCapa oculta ' + str(capa) + ':')
        print(red[capa])


def imprimirRed2(red):
    # Muestra el contenido de la red en su estado actual, por cada capa, de forma mas ordenada (ocupa mas espacio)
    for capa in range(len(red)):
        if capa == 0:
            UIWindow.window_red.plainTextEdit_red.appendPlainText('Capa de entrada:') # print('\nCapa de entrada:')
        elif capa == len(red)-1:
            UIWindow.window_red.plainTextEdit_red.appendPlainText('\nCapa de salida:') # print('\nCapa de salida:')
        else:
            UIWindow.window_red.plainTextEdit_red.appendPlainText('\nCapa oculta ' + str(capa) + ':') # print('\nCapa oculta ' + str(capa) + ':')
        for i in range(len(red[capa])):
            UIWindow.window_red.plainTextEdit_red.appendPlainText('   Neur. ' + str(i)) # print('\tNeur.', i)
            UIWindow.window_red.plainTextEdit_red.appendPlainText('      '+ str(red[capa][i])) # print('\t\t',red[capa][i])


def inicializarPesos(red):
    # Paso 1: Inicializar los pesos de la red con valores pequeños aleatorios
    for capa in range(1,len(red)):
        for neuronaActual in red[capa]:
            for neuronaAnterior in range(len(red[capa-1])):
                 neuronaActual['pesos'].append(random.uniform(-0.5,0.5)) # Siguiendo la recomendacion del libro para valores iniciales de pesos (+-0.5)
                 neuronaActual['cambiosPeso'].append(0) # Los cambios de peso sirven para el calculo del termino momento


def aplicarPatronDeEntrada(patron, red):
    # Paso 2: Presentar un patron de entrada del dataset
    
    # Verifico que el nro de neuronas de entrada coindida con el nro de entradas del patron (comprobacion por motivos de test)
    if len(red[0]) != len(patron[:-3]):
        print('Numero de entradas no coincide con numero de neuronas en capa de entrada')
    else:
        for i in range(len(red[0])): # Cargo valores de entrada del patron en neuronas de entrada
            red[0][i]['salida'] = patron[i]
        for salida in range(len(red[-1])): # Guardo valores de salida (clases) del patron en neuronas de salida
            red[-1][salida]['salidaDeseada'] = patron[len(red[0])+salida]


def calcularSalidasRed(fActSalida, fActOculta, red):
    # Paso 3: Propagar las entradas y calcular las salidas de la red
    for capa in range(1,len(red)):
        for neuronaActual in red[capa]:
            # Paso 3.1: Calculo los net (de neuronas ocultas y de salida)
            neuronaActual['net'] = calcularNetNeurona(neuronaActual['pesos'], capa-1, red)
            # Paso 3.2: Calculo las salidas (de neuronas ocultas y de salida)
            neuronaActual['salida'] = calcularSalidaNeurona(neuronaActual['net'], capa, fActSalida, fActOculta, red)

    
def calcularNetNeurona(pesosNeurona, capaAnterior, red):
    # Paso 3.1
    net = 0
    for i in range(len(red[capaAnterior])): # o bien for i in range(len(pesosNeurona))
        net += pesosNeurona[i] * red[capaAnterior][i]['salida']
    return net


def calcularSalidaNeurona(net, capa, fActSalida, fActOculta, red):
    # Paso 3.2
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
    # La constante "e" elevada a un numero mayor a 709.78271 resulta en un numero extremadamente grande
    # que supera la representacion en coma flotante: 1.7976931348623157e+308, y devuelve un error de 
    # OverflowError. 
    # Por la forma de la funcion sigmoidal, esto pasa cuando le pasamos un x menor a -709.78271 (que 
    # eleva "e" a un numero mayor a 709.78271). Si se pudiera representar, el resultado de la funcion 
    # sigmoidal seria un numero con mas de 309 ceros adelante (practicamente 0). Por eso, para evitar
    # el OverflowError cuando se presenta este caso, se reemplaza la potencia de "e" con la constante
    # inf (infinito positivo de punto flotante), que se representa con float('inf') o math.inf, y que 
    # hace que la funcion devuelva directamente 0.
    try:
        potencia = exp(-x) # math.exp(x) retorna "e" elevado a la x potencia
    except OverflowError:
        potencia = float('inf') # o math.inf
    
    # # O tambien:
    # if x < -709.78271:
    #   potencia = float('inf')
    # else:
    #   potencia = exp(-x)

    return 1/(1+potencia)


def calcularTerminosErrorRed(fActSalida, fActOculta, red):
    # Paso 4: Se calculan los terminos de error para neuronas de salida y ocultas, comenzando por las de salida (propagacion de errores hacia atras)
    for capa in reversed(range(1,len(red))): # Recorro las capas hacia atras
        for nroNeurona in range(len(red[capa])):
            neuronaActual = red[capa][nroNeurona]
            neuronaActual['delta'] = calcularTerminoError(capa, neuronaActual, nroNeurona, fActSalida, fActOculta, red)


def derivadaFuncionSigmoidal(salida):
    return salida*(1-salida)


def calcularTerminoError(capa, neuronaActual, nroNeurona, fActSalida, fActOculta, red):
    # Determina un termino de error en base a la capa actual, la neurona actual, y el numero de esa neurona
    # El numero de la neurona es usado para el calculo del delta en neuronas ocultas
    delta = 0
    if capa == len(red)-1: # Estoy en capa de salida, calculo delta para neuronas de salida
        if fActSalida == 'lineal':
            delta = neuronaActual['salidaDeseada'] - neuronaActual['salida']
        else:
            delta = (neuronaActual['salidaDeseada'] - neuronaActual['salida']) * derivadaFuncionSigmoidal(neuronaActual['salida'])
    else: # Estoy en una capa oculta, calculo delta de neuronas ocultas
        sumatoria = 0
        for neuronaCapaSiguiente in red[capa+1]:
            sumatoria += neuronaCapaSiguiente['delta'] * neuronaCapaSiguiente['pesos'][nroNeurona] # Acumulo la sumatoria del producto del delta de cada neurona de la capa siguiente por el peso que almacena en la posicion de la neurona actual
        if fActOculta == 'lineal':
            delta = sumatoria
        else:
            delta = derivadaFuncionSigmoidal(neuronaActual['salida']) * sumatoria
    return delta


def actualizarPesosRed(alfa, beta, red):
    # Paso 5: Actualizacion de los pesos de la red
    for capa in reversed(range(1,len(red))): # Recorro las capas hacia atras (podria hacerlo hacia adelante)
        for neuronaActual in red[capa]: 
            for peso in range(len(red[capa-1])):
                pesoViejo = neuronaActual['pesos'][peso]
                pesoNuevo = pesoViejo + alfa * neuronaActual['delta'] * red[capa-1][peso]['salida'] + beta * neuronaActual['cambiosPeso'][peso]
                cambioPeso = pesoNuevo - pesoViejo
                neuronaActual['pesos'][peso] = pesoNuevo
                neuronaActual['cambiosPeso'][peso] = cambioPeso


def calcularMSE(red):
    # Paso 6: Calcula el error cuadrático medio entre la salida obtenida y la deseada.
    sumatoria = 0
    for neuronaSalida in red[-1]:
        delta = neuronaSalida['salidaDeseada'] - neuronaSalida['salida']
        delta_cuad = delta**2
        sumatoria += delta_cuad
    mse = 0.5 * sumatoria
    return mse



# ***********************************************************
# UI, DEFINICION DE CLASES, ATRIBUTOS Y METODOS
# ***********************************************************


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Cargamos el archivo .ui
        uic.loadUi(resource_path("ui\\uitpi.ui"), self)

        # Hacemos inicializaciones
        self.initUI()

        # Labels
        self.labels_matriz1 = self.findChildren(QLabel, QtCore.QRegularExpression ("^label_\d\d$")) # Creo una lista con los QLabels que forman el 1er grafico de matriz de patron, usando una expresion regular para matchear los nombres (https://doc.qt.io/qtforpython-5/PySide2/QtCore/QRegExp.html)
        self.labels_matriz2 = self.findChildren(QLabel, QtCore.QRegularExpression ("^label_1\d\d$")) # Lo mismo para los labels de la segunda matriz
        def ordenarLabels(label): return label.objectName() # Para ordenar los QLabels por nombre (porque los devuelve desordenados)
        self.labels_matriz1.sort(key = ordenarLabels) # Ordeno los QLabels (el orden es importante para pintar la matriz)
        self.labels_matriz2.sort(key = ordenarLabels) # Ordeno los QLabels (el orden es importante para pintar la matriz)
        
        # # Para probar si lista y ordena correctamente los labels
        # print(len(self.labels_matriz1))
        # print(len(self.labels_matriz2))
        # for label in self.labels_matriz2:
        #     print(label.objectName())

        # Acciones disparadas por push buttons
        self.pushButton_generar.clicked.connect(self.generarDataset)
        self.pushButton_guardar.clicked.connect(self.guardarDataset)
        self.pushButton_cargar.clicked.connect(self.cargarDataset)
        self.pushButton_crearred.clicked.connect(self.crearRed)
        self.pushButton_entrenar.clicked.connect(self.entrenarRed)
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

        # Acciones disparadas por spin boxes
        self.spinBox_capasOcultas.valueChanged.connect(self.tratarSpinBoxCapaOculta2)

        # Acciones disparadas por sliders
        self.horizontalSlider_probar1patron.valueChanged.connect(self.tratarLineEditSlider)

        # Desactivacion inicial de label+spinbox de tamaño de capa oculta 2
        self.spinBox_tamCapaOc2.setEnabled(False)
        self.label_arquired5.setEnabled(False)

        # Desactivacion inicial del label y botones para mostrar red y datasets
        self.pushButton_verred.setEnabled(False)
        self.pushButton_verentr.setEnabled(False)
        self.pushButton_vertest.setEnabled(False)
        self.pushButton_verval10.setEnabled(False)
        self.pushButton_verval20.setEnabled(False)
        self.pushButton_verval30.setEnabled(False)
        self.label_verreddataset.setEnabled(False)

        # Desactivaciones iniciales de la 2da pestaña
        self.label_salida_clasif.setEnabled(False)
        self.label_clasificacion1.setStyleSheet('background-color: rgb(255, 255, 255);border-width: 1px;border-style: solid;border-color: rgb(208, 208, 208);')
        self.label_clasificacion2.setStyleSheet('background-color: rgb(255, 255, 255);border-width: 1px;border-style: solid;border-color: rgb(208, 208, 208);')
        self.pushButton_clasificar.setEnabled(False)
        self.label_yb.setEnabled(False)
        self.lineEdit_yb.setEnabled(False)
        self.label_yd.setEnabled(False)
        self.lineEdit_yd.setEnabled(False)
        self.label_yf.setEnabled(False)
        self.lineEdit_yf.setEnabled(False)
        self.graphicsView.setStyleSheet('border: 1px solid rgb(208, 208, 208);')
        self.graphicsView_2.setStyleSheet('border: 1px solid rgb(208, 208, 208);')

        # Inicializacion de letra ingresada (se usa en segunda pestaña)
        self.letraIngresada = ''


    def initUI(self):
        self.setWindowTitle('TPI MLP 2022 - Inteligencia Artificial - UTN FRRe') # Titulo de la ventana
        self.center() # Centramos ventana
        self.mostrarPorConsola('>>Hola! Comience creando o cargando un dataset') # Instruccion inicial
        self.setWindowIcon(QIcon(resource_path('icons\\icon.ico'))) # Icono de la ventana
        self.show() # Mostramos la app

    def center(self):
        # Hace que la ventana aparezca centrada
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def mostrarPorConsola(self, texto):
        # Muestra en la parte derecha de la UI un texto
        self.consola.appendPlainText(texto)
        self.consola.moveCursor(QTextCursor.End)

    # METODOS PARA LA PRIMERA PESTAÑA

    def generarDataset(self):
        # Verifica si alguno de los radio buttons se selecciono y genera los datasets correspondientes
        rb100 = self.radioButton_100.isChecked() 
        rb500 = self.radioButton_500.isChecked() 
        rb1000 = self.radioButton_1000.isChecked()
        if rb100 or rb500 or rb1000:
            if rb100:
                self.dataset_full, self.dataset_entr, self.dataset_test, self.conjunto_val_10, self.conjunto_val_20, self.conjunto_val_30 = generarDataset(100)                
            elif rb500:
                self.dataset_full, self.dataset_entr, self.dataset_test, self.conjunto_val_10, self.conjunto_val_20, self.conjunto_val_30 = generarDataset(500)
            elif rb1000:
                self.dataset_full, self.dataset_entr, self.dataset_test, self.conjunto_val_10, self.conjunto_val_20, self.conjunto_val_30 = generarDataset(1000)
            self.mostrarPorConsola('>>Datasets de entrenamiento, test y validación creados correctamente')
            self.groupBox_arquitectura.setEnabled(True)
            self.pushButton_verentr.setEnabled(True)
            self.pushButton_vertest.setEnabled(True)
            self.pushButton_verval10.setEnabled(True)
            self.pushButton_verval20.setEnabled(True)
            self.pushButton_verval30.setEnabled(True)
            self.label_verreddataset.setEnabled(True)
            if not self.pushButton_guardar.isEnabled(): # Habilito el boton Guardar si no estaba habilitado
                self.pushButton_guardar.setEnabled(True)
        else:
            self.mostrarPorConsola('>>Debe seleccionar cantidad de ejemplos')

    def guardarDataset(self):
        # Guarda en la ruta del ejecutable el dataset completo generado
        tam = len(self.dataset_full) # Determino el tamaño del dataset actual
        path = os.path.dirname(__file__) # Obtengo el path del ejecutable
        f = open('dataset_de_%s.txt' %(tam), 'w') # Creo el archivo .txt
        f.write(str(self.dataset_full)) # Escribo el archivo
        f.close()
        self.mostrarPorConsola('>>Dataset guardado correctamente en ' + path)

    def cargarDataset(self):
        # Carga un dataset desde un .txt (deberia ser un "dataset_full" guardado previamente, con los 100, 500 o 1000 ejemplos)
        # y extrae los demas conjuntos
        fname = QFileDialog.getOpenFileName(self, 'Open File', '', "*.txt") # Abrimos un cuadro de dialogo
        if not fname[0] == '': # fname[0] devuelve '' cuando cancelamos en el cuadro de dialogo
            path = fname[0] # Obtengo el path del arhivo seleccionado
            f = open(path, "r")
            dataset_string = f.read()
            f.close()
            dataset = convertirStringADataset(dataset_string)
            self.dataset_full = dataset
            self.dataset_entr, self.dataset_test, self.conjunto_val_10, self.conjunto_val_20, self.conjunto_val_30 = cargarDataset(dataset)
            self.mostrarPorConsola('>>Dataset cargado correctamente desde ' + path)
            self.mostrarPorConsola('>>Datasets de entrenamiento, test y validación creados correctamente')
            self.groupBox_arquitectura.setEnabled(True)
            self.pushButton_verentr.setEnabled(True)
            self.pushButton_vertest.setEnabled(True)
            self.pushButton_verval10.setEnabled(True)
            self.pushButton_verval20.setEnabled(True)
            self.pushButton_verval30.setEnabled(True)
            self.label_verreddataset.setEnabled(True)
            if not self.pushButton_guardar.isEnabled(): # Habilito el boton Guardar si no estaba habilitado
                self.pushButton_guardar.setEnabled(True)

            # # Para probar
            # print('Tamaño dataset full:', len(self.dataset_full))
            # print('Tamaño dataset test', len(self.dataset_test))
            # print('Tamaño dataset entrenamiento:', len(self.dataset_entr))
            # print('Tamaño conjunto val 10:', len(self.conjunto_val_10))
            # print('Tamaño conjunto val 20:', len(self.conjunto_val_20))
            # print('Tamaño conjunto val 30:', len(self.conjunto_val_30))

    def tratarSpinBoxCapaOculta2(self):
        # Activa o desactiva el spinbox de tamaño de capa oculta 2 y su label, dependiendo del valor del numero de capas ocultas.
        if self.spinBox_capasOcultas.value() == 2:
            self.spinBox_tamCapaOc2.setEnabled(True)
            self.label_arquired5.setEnabled(True)
        else:
            self.spinBox_tamCapaOc2.setEnabled(False)
            self.label_arquired5.setEnabled(False)

    def crearRed(self):
        # Cargo caracteristicas de la red
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
        self.funcionDeActivacionSal = 'sigmoidal'
        self.alfa = self.doubleSpinBox_alfa.value()
        self.beta = self.doubleSpinBox_beta.value()

        # Creo atributos auxiliares en base a las caracteristicas
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
        # imprimirRed1(self.red)

        # Habilito el entrenamiento y boton para ver red
        self.groupBox_entrenamiento.setEnabled(True)
        self.pushButton_verred.setEnabled(True)

        # Muestro mensaje por consola con informacion de la red creada
        if hay_2:
            cap_oc_2 = '\n*Tamaño capa oculta 2: ' + str(self.tamCapaOc2)
        else:
            cap_oc_2 = ''
        self.mostrarPorConsola('>>Red creada correctamente\n*Nro. total de capas: '+str(self.nroCapas)+'\n*Tamaño capa de entrada: '+str(self.tamCapaEnt)+'\n*Tamaño capa oculta 1: '+str(self.tamCapaOc1)+'%s' %(cap_oc_2)+'\n*Tamaño capa de salida: '+str(self.tamCapaSal)+'\n*Función de transf. de capa oculta: '+self.funcionDeActivacionOc+'\n*Función de transf. de capa de salida: '+self.funcionDeActivacionSal+'\n*Coeficiente de aprendizaje (α): '+str(round(self.alfa,1))+'\n*Término momento (β): '+str(round(self.beta,1)))

    def entrenarRed(self):
        # Hace el entrenamiento hasta obtener MSE por debajo de un error aceptable, o bien repitiendo por una cantidad de epocas ingresadas
        error = self.radioButton_erroracep.isChecked()
        epocas = self.radioButton_iteraciones.isChecked()
        
        if error or epocas:
    
            if error: # Se selecciono el combo box de error aceptable
                # Tomo el error aceptable ingresado
                errorAcep = float(self.lineEdit_erroracep.text())
                
                # Hago un entrenamiento por cada conjunto de validacion
                for conjunto_val in (self.conjunto_val_10, self.conjunto_val_20, self.conjunto_val_30):
                    errorNoAceptable = True # Bandera que me informa si algun patron dio un error mayor al aceptable
                    dataset_entr_actual = restarDatasets(self.dataset_entr, conjunto_val) # Resto al de entrenamiento el conjunto de validacion
                    self.vaciarRed() # Dejo la red vacia para iniciar un nuevo entrenamiento
                    nroEpocas = 0 # Contador de epocas
                    sumErrorEpocas = 0 # Acumula errores de las epocas
                    listaErroresEpoca = [] # Usado para el grafico de MSE vs epoca
                    inicializarPesos(self.red)
                    
                    # Si algun patron tuvo error por encima del aceptable, comienzo una nueva epoca
                    while errorNoAceptable:  
                        errorNoAceptable = False                      
                        sumErrorEpoca = 0 # Acumula error de 1 epoca
                        nroEpocas += 1
                        contFilas = 0
                        # print('Epoca ' + str(nroEpocas))
                        if nroEpocas > 100:
                            self.mostrarPorConsola('>>Mas de 100 epocas...')
                            self.mostrarPorConsola('>>La red no se establizó')
                            break
                        
                        # Itero cada patron del dataset_entr_actual
                        for fila in dataset_entr_actual:
                            contFilas += 1
                            aplicarPatronDeEntrada(fila, self.red)
                            calcularSalidasRed(self.funcionDeActivacionSal, self.funcionDeActivacionOc, self.red)
                            calcularTerminosErrorRed(self.funcionDeActivacionSal, self.funcionDeActivacionOc, self.red)
                            actualizarPesosRed(self.alfa, self.beta, self.red)
                            error = calcularMSE(self.red)
                            if error > errorAcep:
                                errorNoAceptable = True
                                # print('Error que superó:',error)
                            sumErrorEpoca += error

                            # No se cuantas epocas me llevara el entrenamiento, por lo que muestro el progreso por cada epoca
                            prog = ceil(contFilas*100/len(dataset_entr_actual))
                            self.progressBar_entrenamiento.setValue(prog)

                        errorEpoca = sumErrorEpoca / len(dataset_entr_actual)
                        listaErroresEpoca.append(errorEpoca)
                        sumErrorEpocas += errorEpoca

                    precision = round(self.probarDataset(conjunto_val)[0],2)
                    errorEpocas = sumErrorEpocas / nroEpocas
                    if conjunto_val is self.conjunto_val_10:
                        listaErroresEpoca10 = listaErroresEpoca
                        self.lineEdit_prec10.setText(str(precision))
                        self.lineEdit_mse10.setText(str(round(errorEpocas,8)))
                        self.mostrarPorConsola('>>\n*Epocas con conjunto de 10: ' + str(nroEpocas))
                    elif conjunto_val is self.conjunto_val_20:
                        listaErroresEpoca20 = listaErroresEpoca
                        self.lineEdit_prec20.setText(str(precision))
                        self.lineEdit_mse20.setText(str(round(errorEpocas,8)))
                        self.mostrarPorConsola('*Epocas con conjunto de 20: ' + str(nroEpocas))
                    else:
                        listaErroresEpoca30 = listaErroresEpoca
                        self.lineEdit_prec30.setText(str(precision))
                        self.lineEdit_mse30.setText(str(round(errorEpocas,8)))
                        self.mostrarPorConsola('*Epocas con conjunto de 30: ' + str(nroEpocas))
                self.graficarErrores(listaErroresEpoca10, listaErroresEpoca20, listaErroresEpoca30)
            
            else: # Se selecciono el combo box de numero fijo de iteraciones
                # Tomo el numero de iteraciones ingresado
                nroEpocas = self.spinBox_iteraciones.value() 
                
                # Hago un entrenamiento por cada conjunto de validacion
                for conjunto_val in (self.conjunto_val_10, self.conjunto_val_20, self.conjunto_val_30):
                    dataset_entr_actual = restarDatasets(self.dataset_entr, conjunto_val) # Resto al de entrenamiento el conjunto de validacion
                    self.vaciarRed() # Dejo la red vacia para iniciar un nuevo entrenamiento
                    sumErrorEpocas = 0 # Acumula errores de las epocas
                    listaErroresEpoca = []
                    inicializarPesos(self.red)
                    
                    # Itero "nroEpocas" veces el dataset_entr_actual
                    for epoca in range(nroEpocas):
                        if nroEpocas > 1:
                            prog = ceil((epoca+1)*100/nroEpocas)
                            self.progressBar_entrenamiento.setValue(prog)
                        else: # Si se ingresa 1 sola epoca, se pausa la barra de progreso 0.02 seg para no hacerlo tan rapido
                            self.progressBar_entrenamiento.reset()
                            self.progressBar_entrenamiento.setValue(50)
                            sleep(0.02)
                            self.progressBar_entrenamiento.setValue(100)
                        sumErrorEpoca = 0 # Acumula error de 1 epoca

                        # Itero cada patron del dataset_entr_actual
                        for fila in dataset_entr_actual:
                            aplicarPatronDeEntrada(fila, self.red)
                            calcularSalidasRed(self.funcionDeActivacionSal, self.funcionDeActivacionOc, self.red)
                            calcularTerminosErrorRed(self.funcionDeActivacionSal, self.funcionDeActivacionOc, self.red)
                            actualizarPesosRed(self.alfa, self.beta, self.red)
                            error = calcularMSE(self.red)
                            sumErrorEpoca += error
                        errorEpoca = sumErrorEpoca / len(dataset_entr_actual)
                        listaErroresEpoca.append(errorEpoca)
                        sumErrorEpocas += errorEpoca
                    
                    precision = round(self.probarDataset(conjunto_val)[0],2)
                    errorEpocas = sumErrorEpocas / nroEpocas
                    if conjunto_val is self.conjunto_val_10:
                        listaErroresEpoca10 = listaErroresEpoca
                        self.lineEdit_prec10.setText(str(precision))
                        self.lineEdit_mse10.setText(str(round(errorEpocas,8)))
                    elif conjunto_val is self.conjunto_val_20:
                        listaErroresEpoca20 = listaErroresEpoca
                        self.lineEdit_prec20.setText(str(precision))
                        self.lineEdit_mse20.setText(str(round(errorEpocas,8)))
                    else:
                        listaErroresEpoca30 = listaErroresEpoca
                        self.lineEdit_prec30.setText(str(precision))
                        self.lineEdit_mse30.setText(str(round(errorEpocas,8)))
                self.graficarErrores(listaErroresEpoca10, listaErroresEpoca20, listaErroresEpoca30)

            self.mostrarPorConsola('>>Etapa de entrenamiento finalizada')
            self.groupBox_test.setEnabled(True)
            self.groupBox_probar1patron.setEnabled(True)
            self.groupBox_probarmasde1.setEnabled(True)
            self.graphicsView.setStyleSheet('border: 1px solid black;')
            self.graphicsView_2.setStyleSheet('border: 1px solid black;')
            self.label_clasificacion2.setStyleSheet('background-color: rgb(255, 255, 255);border-width: 1px;border-style: solid;border-color: black;')
        
        else:
            self.mostrarPorConsola('>>Debe seleccionar una opción')

    def vaciarRed(self):
        # Asigna al atributo "red" una estructura de red vacia. Se usa para resetear la red en cada entrenamiento
        self.red = crearRed(self.tamCapaEnt, self.capasOcultas, self.neuronasPorCapa, self.tamCapaSal)
        
    def probarDataset(self, dataset):
        # Calcula la precision de la clasificacion con un dataset
        clasifCorrectas = 0

        for fila in dataset:
            clasifCorrecta = self.probarPatron(fila)[0] # probarPatron() retorna en primer lugar 1 si la salida obtenida es igual a la deseada, o 0 en caso contrario
            clasifCorrectas += clasifCorrecta
        
        precision = clasifCorrectas / len(dataset)
        # print('Clasificaciones correctas:',clasifCorrectas)
        # print('Casos de prueba:',len(dataset))
        return precision, clasifCorrectas
   
    def probarPatron(self, patron):
        # Presenta un patron a la red, calcula la salida, comprueba si la salida obtenida es igual a la deseada, y devuelve 1
        # o 0 dependiendo de la coincidencia, y la salida obtenida convertida a binaria y sin convertir
        aplicarPatronDeEntrada(patron, self.red)
        calcularSalidasRed(self.funcionDeActivacionSal, self.funcionDeActivacionOc, self.red)
    
        so1_float = self.red[-1][0]['salida'] # so1 = salida obtenida 1
        so2_float = self.red[-1][1]['salida'] # so2 = salida obtenida 2
        so3_float = self.red[-1][2]['salida'] # so3 = salida obtenida 3
        sd1 = self.red[-1][0]['salidaDeseada'] # sd1 = salida deseada1
        sd2 = self.red[-1][1]['salidaDeseada'] # sd2 = salida deseada2
        sd3 = self.red[-1][2]['salidaDeseada'] # sd3 = salida deseada3

        # Convierto la salida en coma flotante a binaria (para poder comparar con la deseada)
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

        return clasifCorrecta, so1_bin, so2_bin, so3_bin, so1_float, so2_float, so3_float

    def graficarErrores(self, listaErrores10, listaErrores20, listaErrores30):
        # Genera un grafico comparando los MSE contra las epocas
        ypoints10 = np.array(listaErrores10)
        ypoints20 = np.array(listaErrores20)
        ypoints30 = np.array(listaErrores30)
        plt.plot(ypoints10)
        plt.plot(ypoints20)
        plt.plot(ypoints30)
        plt.xlabel("Epocas")
        plt.ylabel("MSE")
        plt.show()

    def hacerTest(self):
        precision, correctas = self.probarDataset(self.dataset_test)
        precision = round(precision, 2)
        self.lineEdit_testcorrectas.setText(str(correctas))
        self.lineEdit_testtotal.setText(str(len(self.dataset_test)))
        self.lineEdit_testprec.setText(str(precision))
        self.mostrarPorConsola('>>Etapa de test finalizada')

    # METODOS PARA LA SEGUNDA PESTAÑA

    def tratarLineEditSlider(self, value):
        # Traslada valor del slider al lineedit
        self.lineEdit_sliderprobar1.setText(str(value))

    def tratarLetra(self, patron, letra):
        # Se llama cuando se presiona el boton de una letra
        self.mostrarPorConsola('>>Letra ' + letra + ' seleccionada')
        self.setLetraIngresada(letra)
        self.mostrarLetra(patron, self.labels_matriz1)

    def setLetraIngresada(self, letra):
        self.letraIngresada = letra

    def getLetraIngresada(self):
        return self.letraIngresada

    def mostrarLetra(self, patron, matriz):
        # Pinta la matriz de pixeles de acuerdo al patron pasado
        self.borrarLetra(matriz)        
        labels = matriz
        for i in range(len(patron)):
            if patron[i] == 1:
                labels[i].setStyleSheet("background-color:black")
                # print(labels[i].objectName()) # Por si quiero ver qué labels modifica
        
    def borrarLetra(self, matriz):
        # Pone en blanco la matriz de pixeles
        labels = matriz
        for label in labels:
            label.setStyleSheet("background-color:white")

    def generarDistorsion(self):
        # Se llama cuando presiono el boton "Distorsionar". Muestra la letra distorsionada en la 1ra matriz de la 2da pestaña
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
                self.mostrarPorConsola('>>Letra ' + letra + ' distorsionada un ' + str(distorsion) + '%')        
            usado = self.comprobarPatron(patron, letra) # Compruebo si el patron fue usado para entrenar
            if usado:
                self.lineEdit_usado.setText('Si')
            else:
                self.lineEdit_usado.setText('No')

            # Activo la parte de clasificacion (a la derecha de la 1ra matriz de pixeles)
            self.label_salida_clasif.setEnabled(True)
            self.label_clasificacion1.setStyleSheet('background-color: rgb(255, 255, 255);border-width: 1px;border-style: solid;border-color: black;')
            self.pushButton_clasificar.setEnabled(True)
            self.label_yb.setEnabled(True)
            self.lineEdit_yb.setEnabled(True)
            self.label_yd.setEnabled(True)
            self.lineEdit_yd.setEnabled(True)
            self.label_yf.setEnabled(True)
            self.lineEdit_yf.setEnabled(True)
            
    def copiarPatron(self, letra):
        # Devuelve una copia del patron sin distorsionar de la letra pasada
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
        # Comprueba si un patron fue usado para el entrenamiento
        resta1 = restarDatasets(self.dataset_entr, self.conjunto_val_10)
        resta2 = restarDatasets(self.dataset_entr, self.conjunto_val_20)
        resta3 = restarDatasets(self.dataset_entr, self.conjunto_val_30)

        if letra == 'b':
            patron_con_clases = patron + [1,0,0]
        elif letra == 'd':
            patron_con_clases = patron + [0,1,0]
        else:
            patron_con_clases = patron + [0,0,1]
        
        if patron_con_clases in resta1 or patron_con_clases in resta2 or patron_con_clases in resta3:
            return True
        else:
            return False

    def clasificarPatron(self, patron, label, probarPatrones):
        # Presenta un patron a la red y muestra la letra que representa la salida de la misma.

        # Agrego 3 valores de clase cualquiera para que funcione correctamente aplicarPatronDeEntrada()
        patron_de_prueba = patron.copy()
        patron_de_prueba += [0,0,0] 

        so1_bin, so2_bin, so3_bin, so1_float, so2_float, so3_float = self.probarPatron(patron_de_prueba)[1:] # probarPatron() retorna, a partir de la posicion 1, la salida en forma binaria y decimal de la red al aplicar un patron

        if so1_bin == 1:
            label.setText('b')
        elif so2_bin == 1:
            label.setText('d')
        else:
            label.setText('f')
        if not probarPatrones: # Solamente cuando no estoy probando patrones (matrices de pixeles de abajo), muestro las salidas obtenidas
            self.lineEdit_yb.setText(str(round(so1_float,8)))
            self.lineEdit_yd.setText(str(round(so2_float,8)))
            self.lineEdit_yf.setText(str(round(so3_float,8)))
            self.mostrarPorConsola('>>Patrón clasificado')

    def probarPatrones(self):
        # Clasifica un numero dado de patrones aleatorios y muestra la precision

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

        # Grafico patrones distorsionados y clasificacion, uno detras de otro, con 50 mseg de pausa entre cada uno
        contFilas = 0 # Para graficar el progreso
        for patron in dataset:
            contFilas += 1
            self.mostrarLetra(patron[:-3], self.labels_matriz2) # Muestro la letra en 2da matriz de pixeles
            self.clasificarPatron(patron[:-3], self.label_clasificacion2, True) # Muestro clasificacion de la letra
            prog = ceil(contFilas*100/len(dataset)) # Calculo progreso
            self.progressBar_probarpatrones.setValue(prog) # Grafico progreso
            QtTest.QTest.qWait(50) # Genero delay para animar la graficacion de la matriz de pixeles
        
        # Uso probarDataset() para obtener las clasificaciones correctas y la precision
        precision, clasifCorrectas = self.probarDataset(dataset)

        # Muestro resultados
        self.lineEdit_probar_correctas.setText(str(clasifCorrectas))
        self.lineEdit_probar_total.setText(str(nroPatrones))
        self.lineEdit_probar_precision.setText(str(round(precision,2)))
        self.mostrarPorConsola('>>Prueba de patrones finalizada')

    # METODOS PARA VER CONTENIDO DE LA RED Y DE DATASETS

    def verDataset(self, dataset):
        # Abre una ventana con el dataset pasado mostrado en forma tabular y grafica
        self.window_dataset = UIDialog_dataset
        self.window_dataset.show()
        self.window_dataset.plainTextEdit_tabular.clear()
        self.window_dataset.plainTextEdit_grafico.clear()
        imprimirDataset2(dataset)
        imprimirDataset1(dataset)
        self.window_dataset.plainTextEdit_tabular.moveCursor(QTextCursor.Start)
        self.window_dataset.plainTextEdit_grafico.moveCursor(QTextCursor.Start)
        
    def verRed(self):
        # Abre una ventana que muestra la estructura y contenido actual de la red
        self.window_red = UIDialog_red
        self.window_red.show()
        self.window_red.plainTextEdit_red.clear()
        imprimirRed2(self.red)
        self.window_red.plainTextEdit_red.moveCursor(QTextCursor.Start)


# Para ventana de impresion de dataset
class UI_dialog_dataset(QDialog):
    def __init__(self):
        super(UI_dialog_dataset, self).__init__()

        # Cargamos el archivo .ui
        uic.loadUi(resource_path("ui\\uidataset.ui"), self)

        # Hacemos inicializaciones
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ver dataset') # Titulo de la ventana
        self.center() # Centramos ventana
        self.setWindowIcon(QIcon(resource_path('icons\\icon3.ico'))) # Icono de la ventana

    def center(self):
        # Hace que la ventana aparezca centrada
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

# Para ventana de impresion de red
class UI_dialog_red(QDialog):
    def __init__(self):
        super(UI_dialog_red, self).__init__()

        # Cargamos el archivo .ui
        uic.loadUi(resource_path("ui\\uired.ui"), self)
        
        # Hacemos inicializaciones
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ver red neuronal') # Titulo de la ventana
        self.center() # Centramos ventana
        self.setWindowIcon(QIcon(resource_path('icons\\icon2.ico'))) # Icono de la ventana

    def center(self):
        # Hace que la ventana aparezca centrada
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())




# ***********************************************************
# PROGRAMA PRINCIPAL
# ***********************************************************

# Posiciones ocupadas por cada letra, considerando la matriz como una lista de 100 elementos (del 0 al 99)
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
