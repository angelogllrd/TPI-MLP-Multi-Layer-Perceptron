# Análisis MLP (Multi-Layer Perceptron) 
TPI del año 2022 para la asignatura Inteligencia Artificial de la UTN FRRe.

![2022-11-08 00_12_32-TPI MLP 2022 - Inteligencia Artificial - UTN FRRe](https://user-images.githubusercontent.com/51035369/200443223-3d869881-bd41-43cf-9246-96f443e610d9.png)

## Consigna
<details><summary>Ver Consigna</summary>

#### Objetivos:
1. Implementar el algoritmo MLP.
2. Evaluar la precisión (MSE, error de entrenamiento y validación) de una MLP teniendo en cuenta distintas configuraciones: cantidad de capas, cantidad de neuronas, funciones de activación
3. Elaborar un informe completo en base a las pruebas realizadas.

#### Descripción del problema:
Este trabajo consiste en implementar el algoritmo MLP que permita, dado un dataset en R<sup>2</sup> parametrizar la cantidad de capas, neuronas y funciones de activación con los que se entrenará la red neuronal. La idea es desarrollar una aplicación que defina la arquitectura de la red (con 3 salidas, cada una asociada a un patrón de entrada), tome los datos de diferentes datasets, entrene el modelo y devuelva los resultados de clasificación (MSE, error de entrenamiento y validación).

La implementación deberá contar también con una interfaz de usuario para el ingreso de un patrón distorsionado (determinado por el usuario), que será clasificado según alguno de los patrones aprendidos, mostrando los resultados obtenidos.

Los patrones a detectar y clasificar estarán contenidos en una matriz de 10x10 que contendrán las letras b, d, f como se ve en las siguientes figuras:

<p align="center">
<img width="" height="" src="https://user-images.githubusercontent.com/51035369/199028696-ef21051e-c629-44d1-b034-db173e6e0bef.png">
</p>

#### Datasets
- El grupo de trabajo deberá generar 3 datasets que contengan 100, 500 y 1000 ejemplos. El 10% deberán ser patrones sin distorsionar y el resto con una distorsión del 1% al 30%. Los Datasets deberán ser representativos a la hora de definir la distribución de los ejemplos de entrenamiento.

#### Requerimientos mínimos para el entrenamiento
- Por cada Dataset deberán construirse tres conjuntos de validación con 10%, 20% y 30% de los ejemplos. El conjunto de validación debe ser representativo del Dataset de entrenamiento.
- 1 o 2 capas ocultas.
- De 5 a 10 neuronas por capa.
- Funciones de activación: lineal y sigmoidal.
- Coeficiente de aprendizaje entre 0 y 1.
- Término momento entre 0 y 1.

#### Requerimientos mínimos para el reconocimiento
- Patrón distorsionado de 0% a 30% generado de manera automática o manual.

#### Requerimientos mínimos de pruebas para el informe
- Se deberán realizar como mínimo las siguientes pruebas para cada uno de los datasets con conjuntos de validación de 10%, 20% y 30% de patrones:
  - 1 capa oculta de 5 neuronas, función de transferencia lineal, coeficiente de aprendizaje 0,5 y término momento 0,5.
  - 1 capa oculta de 10 neuronas, función de transferencia lineal, coeficiente de aprendizaje 0,5 y término momento 0,5.
  - 2 capas ocultas (primera capa de 5 neuronas, segunda capa de 5 neuronas), función de transferencia lineal, coeficiente de aprendizaje 0,5 y término momento 0,5.
  - 2 capas ocultas (primera capa de 10 neuronas, segunda capa de 10 neuronas), función de transferencia lineal, coeficiente de aprendizaje 0,5 y término momento 0,5.
  - Repetir las mismas pruebas con término momento 0,9.

#### Consideraciones adicionales:
- Se deberá contar con una interfaz de usuario que permita la total operabilidad de la aplicación.
- Las interfaces deberán ser amigables (se aceptarán solamente entornos gráficos) e intuitivas (menú contextual de guía).
- El código debe estar totalmente documentado/comentado.
- El algoritmo debe ser enteramente desarrollado por los alumnos.
- Debe ser una aplicación de escritorio.
</details>

## Requerimientos para ejecutar el .py
<details><summary>Ver Requerimientos para ejecutar el .py</summary>

  
- [**Python 3**](https://www.python.org/downloads/)
- [**pip**](https://pypi.org/project/pip/) (ya incluido con el instalador de Windows). En Linux:
  ```
  sudo apt update
  sudo apt install python3-pip
  ```
- **PyQt5** (libreria para la UI)
  ```
  pip install PyQt5
  ```
- **Qt Designer** (para abrir y editar la UI) 
  - Windows
    - Opción 1: https://build-system.fman.io/qt-designer-download
    - Opción 2: (Si la versión de Python es 3.10, cambiar \Python3xx por \Python310)
      ```
      pip install PySide6
      %USERPROFILE%\AppData\Local\Programs\Python\Python3xx\Lib\site-packages\PySide6\designer.exe
      ```
  - Linux:
    ```
    sudo apt-get install qttools5-dev-tools
    designer
    ```
- **Matplotlib** (Para las gráficas de errores vs. épocas)
  ```
  pip install matplotlib
  ```
</details>

## Ejecutable (Windows y Linux)
<details><summary>Ver Ejecutable (Windows y Linux)</summary>
  
Para evitar la instalación de las librerias, podemos obtener un ejecutable usando [**Auto PY to EXE**](https://dev.to/eshleron/how-to-convert-py-to-exe-step-by-step-guide-3cfi):
  ```
  pip install auto-py-to-exe
  auto-py-to-exe
  ```
<p align="center">
<img width="" height="" src="https://user-images.githubusercontent.com/51035369/199046470-f7a59d19-6258-423f-ac75-3876d7c3eb2e.png">
</p>
  
O directamente con **pyinstaller** (lo que usa Auto PY to EXE por detrás):
  ```
  pip install pyinstaller
  pyinstaller --noconfirm --onefile --windowed --icon "path_a_la_carpeta/tpi/icons/icon.ico" --add-data "path_a_la_carpeta/tpi/icons;icons/" --add-data "path_a_la_carpeta/tpi/ui;ui/"  "path_a_la_carpeta/tpi/tpi.py"
  ```
  En cualquier caso, para no tener problemas con las referencias relativas en el .exe final, el developer de Auto PY to EXE recomienda agregar al código [esto](https://nitratine.net/blog/post/issues-when-using-auto-py-to-exe/#the-one-file-resource-wrapper), y pasar cada path de los archivos referenciados a la función `resource_path()`. Por ejemplo, en lugar de:
  ```
  self.setWindowIcon(QIcon('icons\\icon2.ico'))
  ```
  quedaría:
  ```
  self.setWindowIcon(QIcon(resource_path('icons\\icon2.ico')))
  ```
</details>

## Estructura de los datasets
<details><summary>Ver Estructura de los datasets</summary>
- Como se pide en la consigna, los datasets se generan cumpliendo el 10% sin distorsión, y el restante 90% distorsionado entre 1% y 30%. 
- Los datasets se representan usando listas de listas, donde cada sublista es un patrón de entrada o fila del dataset con 103 elementos (1s y 0s), donde los primeros 100 corresponden al patrón y los últimos 3 a las clases, una para cada letra (b, d y f).
- Para asegurar que los conjuntos de test y validación sean representativos, se genera de la siguiente manera, quedando 4 porciones de cada tipo de ejemplo:

<p align="center">
<img width="70%" height="70%" src="https://user-images.githubusercontent.com/51035369/199055338-a007ef82-d296-41e8-af7e-33b57a095ecb.png">
</p>

- Los datasets de test y validación se crean incluyendo ejemplos de cada porción, lo mas similares posibles en tamaño.
- Se estableció que el porcentaje de ejemplos para test debe ser uno que haga divisible por 4 (4 porciones representativas) el número de ejemplos de test para 100, 500 y 1000 ejemplos. Este porcentaje se calculó en un 8%, número que permite que los restantes ejemplos del dataset alcancen para formar todos los conjuntos de validación representativos para los 3 datasets, según los siguientes cálculos:

<p align="center">
<img width="70%" height="70%" src="https://user-images.githubusercontent.com/51035369/199057030-1ae8ed92-41b1-428f-8dfa-4b17188a9445.png">
</p>

- Gráficamente, para un dataset de 1000 ejemplos cuando se toma un 12% para test:

<p align="center">
<img width="70%" height="70%" src="https://user-images.githubusercontent.com/51035369/199052629-9b68372d-e04a-4bd3-a900-6aaade3f6f61.png">
</p>
</details>

## Estructura de la red neuronal
<details><summary>Ver Estructura de la red neuronal</summary>

- La red se representa también usando lista de listas, donde cada sublista es una capa. 
- Cada neurona dentro cada capa se representa mediante un diccionario, cuyos items varían dependiendo de qué capa se trate.
  - Las neuronas de la capa de entrada solamente tienen salida (que son iguales a las entradas).
  - Las neuronas de las capas ocultas y de salida contienen:
    - **pesos**: Una lista con los pesos de las conexiones entre la unidad actual y todas las unidades de la capa anterior. Por lo tanto, hay tantos pesos como neuronas en la capa anterior.
    - **cambiosPeso**: Usado para el cálculo del término momento. Se actualizan en cada actualización de pesos.
    - **net**: Almacena el cálculo del net de la neurona.
    - **salida**: Almacena el cálculo de la salida de la neurona.
    - **delta**: Almacena el cálculo del término de error de la neurona.
  - Las neuronas de la capa de salida almacenan, además de lo anterior:
    - **salidaDeseada**: Valor de uno de los 3 últimos elementos del patrón.
</details>
  
## Partes de la aplicación de escritorio
<details><summary>Ver Partes de la aplicación de escritorio</summary>
  
> Descarga de la aplicación: [Windows](https://drive.google.com/file/d/1WtA38S4O7MvZgWZLr3xD9tKdn52uQ3Ge/view?usp=sharing) / [Linux](https://drive.google.com/file/d/1CCp0kANpVLxpkK-MhyXm5l_y_MWBBv3B/view?usp=sharing)

La aplicación se divide en 2 pestañas principales: **"Entrenamiento y test"** y **"Probar patrón"**.

### Pestaña **"Entrenamiento y test"**:

<p align="center">
<img width="80%" height="80%" src="https://user-images.githubusercontent.com/51035369/200418814-98371479-d96a-4e68-90cf-05c333a66951.png">
</p>

- **Sección 1**: 
  - Se comienza generando un dataset de 100, 500 o 1000 ejemplos, con el botón "Generar". 
  - También es posible comenzar cargando el .txt de un dataset guardado previamente, con el botón "Cargar".
  - Es posible "Guardar" el dataset generado, en cuyo caso se crea un .txt con un string de la estructura de lista de listas del dataset (el botón se activa cuando genero o cargo un dataset).
- **Sección 2**:
  - Es posible seleccionar una de las arquitecturas de red predefinidas (dadas en la consigna del TPI) y crear la estructura de la red con el botón "Crear red".
  - También es posible ingresar manualmente los parámetros de la red neuronal.
  - Se habilita una vez generado/cargado un dataset.
- **Sección 3**:
  - Esta parte corresponde al entrenamiento. Podemos entrenar la red hasta que el error de época resulte aceptablemente pequeño (menor al error aceptable ingresado), o por un número de iteraciones/épocas fijado. En el primer caso, se limita el entrenamiento a 200 épocas, para evitar que siga indefinidamente cuando la red no converge.
  - Una vez terminado el entrenamiento, se presentan los resultados (número de épocas que llevó el entrenamiento, y errores de entrenamiento y de validación de la última época).
  - Las redes y su estado resultante del entrenamiento son guardadas luego del mismo, para poder seleccionarlas más adelante en la etapa de test, o para porbar un patrón.
  - Se habilita una vez creada la red.
- **Sección 4**:
  - Esta parte corresponde al testing. Es posible seleccionar una red previamente entrenada con la que probar los patrones del dataset de test y calcular la precisión.
  - Se habilita una vez terminado el entrenamiento.
- **Sección 5**:
  - Sección a modo de "consola", que muestra diferentes informaciones a medida que se realiza el proceso.
- **Sección 6**:
  - Estos botones permiten visualizar el contenido de la red (botón "Red"), o de los diferentes conjuntos (Botones "Entrenamiento", "Test", "Validación 10%", "Validación 20%", y "Validación 30%") en forma tabular y gráfica:
  
<p align="center">
<img width="60%" height="60%" src="https://user-images.githubusercontent.com/51035369/200420425-1e48df7b-3e03-40a3-bc80-38c48dce71c5.png">
</p>

<p align="center">
<img width="60%" height="60%" src="https://user-images.githubusercontent.com/51035369/200420528-22a0e6ab-053c-4b71-9c45-edbc71fb3964.png">
</p>    
    
### Pestaña **"Probar patrón"**:

<p align="center">
<img width="80%" height="80%" src="https://user-images.githubusercontent.com/51035369/200421015-fc7198c9-91b7-43ce-a1b2-78863d0b8406.png">
</p>

- **Sección 7**:
  - En esta parte se selecciona la red previamente entrenada con la que se desea probar los patrones.
- **Sección 8**:
  - Esta sección cumple con la parte de la consigna que solicitaba una opción para el ingreso de un patrón distorsionado que debía ser clasificado.
  - Primero se debe seleccionar una letra y la distorsión, y luego presionar el botón "Distorsionar" para habilitar la sección de clasificación de la derecha. Además, la aplicación comprueba si el patrón distorsionado fué usado en el entranamiento (en cuyo caso "¿Patrón usado para entrenar?" dirá que "Si").
  - En la parte derecha, con el botón "Clasificar" se ingresa el patrón a la red seleccionada, se muestra la letra representada por la salida de la red, y las salidas obtenidas por cada neurona de salida (yb, yd, e yf).
- **Sección 9**:
  - Parecida a la sección de arriba, pero permite clasificar un cierto número de patrones (de letras aleatorias, con distorsión aleatoria entre 0 y 30%), comprobando que no hayan sido usados para entrenar, y arroja los resultados de precisión.
</details>
  
## Instrucciones de uso de la aplicación
<details><summary>Ver Instrucciones de uso de la aplicación</summary>

> Descarga de la aplicación: [Windows](https://drive.google.com/file/d/1WtA38S4O7MvZgWZLr3xD9tKdn52uQ3Ge/view?usp=sharing) / [Linux](https://drive.google.com/file/d/1CCp0kANpVLxpkK-MhyXm5l_y_MWBBv3B/view?usp=sharing)

1. **Generar/Cargar dataset:** 
     - En la **Sección 1**, seleccionar el tamaño del dataset a generar, y presionar el botón **"Generar"** (se habilita después de seleccionar un tamaño). También es posible usar el botón **"Cargar"** para cargar el archivo .txt de un dataset guardado previamente con la aplicación. Opcionalmente, luego de cargar/generar un dataset, se habilita el botón **"Guardar"**, que guarda el dataset en la ruta del ejecutable.
       
       ![2022-11-07 22_44_46-Window](https://user-images.githubusercontent.com/51035369/200431389-a95e57ff-46a4-4903-b72c-c0e95898df82.png)
       
     - La generación o la carga de un dataset produce la división del mismo en dos partes: entrenamiento y test. A su vez, con ejemplos del dataset de entrenamiento se forman los 3 conjuntos de validación. Por lo tanto, **los conjuntos o datasets resultantes son 5**.
       
       ![2022-11-07 22_29_20-Window](https://user-images.githubusercontent.com/51035369/200432193-eecdced6-9646-4d58-b746-2d9679c12888.png)
       
     - Luego, se habilita la **Sección 2** para crear una estructura de red, y los botones de la **Sección 6** para ver los diferentes conjuntos formados.
       
       ![2022-11-07 22_49_43-Window](https://user-images.githubusercontent.com/51035369/200432402-0466b0b8-1958-47a1-81f4-a8971f5fa602.png)

2. **Crear estructura de red**:
     - En la **Sección 2** tenemos 2 opciones:
       - **Seleccionar arquitectura predefinida de la lista**: En cuyo caso los campos de los de parámetros de abajo se rellenan automáticamente con los parámetros de la arquitectura seleccionada.
       
         ![2022-11-07 22_54_05-Window](https://user-images.githubusercontent.com/51035369/200432727-18596035-6ed8-4ca3-86df-024ac512d39f.png)

       - **Seleccionar parámetros personalizados**: Es posible seleccionar otros valores de los parámetros para crear una arquitectura no listada en las predefinidas. Si los valores seleccionados coinciden con los de una arquitectura predefinida, ésta aparace automáticamente seleccionada en la lista. De la misma forma, cuando seleccionamos una arquitectura predefinida, y luego cambiamos alguno de los parámetros, la misma deja de estar seleccionada en la lista.
       
         ![2022-11-07 22_54_48-Window](https://user-images.githubusercontent.com/51035369/200432812-70450cfa-4d53-4f69-a7fa-576b5aad70cd.png)

     - Una vez configurada la arquitectura deseada, presionar el botón "Crear red". Luego, se habilita parte de la **Sección 3** y el botón "Red actual" de la **Sección 6**, para ver el contenido de la red creada.

       ![2022-11-07 22_55_46-Window](https://user-images.githubusercontent.com/51035369/200433048-be17315a-ee5d-4a7c-9d54-61e2cf67d957.png)

     - **ACLARACIÓN**: En cada momento, hay una "red actual" cargada, con la que se entrena, se testea y se prueban patrones, y es la que se ve con el botón "Red actual". Crear una nueva red o seleccionar una red entrenada guardada previamente de una de las listas, sobreescribe automáticamente esa red actual, pasando la nueva red (creada o seleccionada) a ser la actual.
3. **Entrenar la red creada**:
     - En la **Sección 3** tenemos 2 opciones para la condición de fin del entrenamiento:
     
       ![2022-11-07 22_41_23-Window](https://user-images.githubusercontent.com/51035369/200433365-47550610-7b0d-4d1f-b8d1-f53df033d2b6.png)
       
       - **Seleccionar un error aceptable:** El entrenamiento termina cuando el Error de entrenamiento promedio (promedio de los MSE de cada patrón en una época) resulta por debajo del error aceptable ingresado. Opcionalmente, descomentando el código en las líneas 977 a 981 y comentando las líneas 993 a 997, el entrenamiento terminará cuando el error de entrenamiento de CADA patrón esté por debajo del error aceptable.
         
         ![2022-11-07 22_19_34-Window](https://user-images.githubusercontent.com/51035369/200433406-97d428b6-5f5f-4192-8afe-b0cfc01294ac.png)
         
         ![2022-11-07 22_19_53-Window](https://user-images.githubusercontent.com/51035369/200433426-a16033a7-4719-41dd-8505-78dcd0ccec75.png)

       - **Seleccionar un número de épocas/iteraciones fijo**: El entrenamiento se hace por un número de épocas fijado, independientemente del Error de entrenamiento como en el caso anterior.
     - Una vez seleccionada una opción, presionar el botón **"Entrenar"** para comenzar el entrenamiento. En realidad, esto lleva a cabo 3 entrenamientos (considerando en cada uno un conjunto de validación distinto). En cada uno de esos 3 entrenamientos:
       - Se restan o quitan los ejemplos de uno conjunto de validación al dataset de entrenamiento original, y se entrena con el conjunto resultante. 
       - Al final de cada época dentro de ese entrenamiento, se resguarda el Error de entrenamiento (promedio de los errores de cada patrón en la época) y el Error de validación (promedio de los errores resultantes al aplicar cada uno de los patrones del conjunto de validación a la red), para poder generar los gráficos de MSE promedio vs. Épocas.
       - Al final, se guarda la red entrenada (con los pesos resultantes), para ser seleccionada en la etapa de test o en la prueba de patrones (segunda pestaña). Por lo tanto, al final de la etapa de entrenamiento quedan guardadas 3 redes entrenadas (misma arquitectura, entrenada considerando 3 conjuntos de validación). Internamente, también se guarda la arquitectura de la red, y los conjuntos de entrenamiento, test y validación asociados (estos últimos porque se los necesita para más adelate y corren el riesgo de ser sobreescritos al crear un nuevo dataset).
     - Al finalizar el entrenamiento, se muestran:
       - **Resultados:** Épocas que llevó el entrenamiento, Error de entrenamiento de la última época, y Error de validación de la última época.
       
           ![2022-11-07 22_42_09-Window](https://user-images.githubusercontent.com/51035369/200434007-12138a54-c41c-4a38-ae2e-0d3ca24ad65e.png)

       - **Gráficos de MSE promedio vs. Épocas:** Cada gráfico representa el Error de entrenamiento y Error de validación por cada época.
       
           ![Figure_1](https://user-images.githubusercontent.com/51035369/200434033-6bbcf586-0fc9-4d07-8829-3a07a5d9a751.png)

     - Se habilita una parte de la **Sección 4** y la **Sección 7**.
     
En este momento podemos elegir realizar el test, o bien ir a la segunda pestaña para probar patrones distorsionados

4. **Realizar el test**:
     - En la **Sección 4** seleccionar la red entrenada previamente con la que queremos realizar el test, y presionar el botón "Hacer test". Esto inserta los patrones del dataset de test guardado en la red seleccionada, en dicha red. Luego calcula las salidas, detecta la letra representada por las salidas y la compara con la salida deseada, obteniendo el número de clasificaciones correctas.
       
       ![2022-11-07 23_19_17-Window](https://user-images.githubusercontent.com/51035369/200436074-77db6ca6-f7e6-4ef1-a793-6f40a487ff8f.png)

     - Se muestran los resultados (Clasificaciones correctas, números de casos de prueba, y la precisión, calculada a partir de los dos primeros), junto con el gráfico de los Errores por cada patrón.
     
       ![Figure_1](https://user-images.githubusercontent.com/51035369/200439614-6f25f033-53aa-4384-aca5-deb6557cd9ed.png)

       ![2022-11-07 23_19_41-Window](https://user-images.githubusercontent.com/51035369/200436701-53e568e9-a6e4-42d2-914e-9bf8730f51e3.png)

5. **Probar patrones** (segunda pestaña):
     - En la **Sección 7** seleccionar la red entrenada previamente con la que queremos probar patrones distorsionados.
     
       ![2022-11-07 23_27_21-Window](https://user-images.githubusercontent.com/51035369/200437109-599be7fd-a506-4c4a-a6f0-30bca024d8ee.png)

     - Esto carga la red seleccionada como red actual, junto con los datasets guardados con la misma (los datasets de entrenamiento y validación guardados en la red seleccionada se usan para comprobar si un patrón aleatorio fué usado en el entrenamiento de esa red), y habilita la **Sección 7** y la **Sección 8**.
     - Luego, tenemos 2 opciones:
       - **Sección 7: Generar y clasificar un patrón con distorsión aleatoria**

           ![image](https://user-images.githubusercontent.com/51035369/200440431-32251ae2-33b1-4f0b-8f45-317418c28496.png)

           - Seleccionar una letra con uno de los 3 botones (se muestra la letra en la matriz de pixeles).
           - Seleccionar la distorsión a generar. **ACLARACIÓN**: El programa comprueba si el patrón distorsionado resultante es uno de los patrones usados para entrenar la red. Si lo fué, se muestra "Si" en el label "¿Patrón usado para entrenar?", mientras que si no, se muestra "No".
           - Presionar el botón "Distorsionar" (se muestra la letra distorsionada en la matriz de pixeles). Esto habilida la parte derecha de la Sección 7, donde clasificamos la letra distorsionada.
           - Presionar el botón "Clasificar". Se muestra la letra que representa la salida de la red al insertar el patrón distorsionado, junto con los valores de salida que se usaron para clasificar la letra.
       - **Sección 8: Generar y clasificar un número dado de patrones con distoriones aleatorias**:

           ![image](https://user-images.githubusercontent.com/51035369/200439675-bf7048ab-9a92-4c36-abb8-96a88aaf7650.png)

           - Ingresar el número de patrones distorsionados a generar.
           - Presionar el botón "Probar patrones". Se muestra a la izquierda la matriz de pixeles con cada patrón generado, junto con la letra clasificada a la derecha. **ACLARACIÓN**: Al igual que en la Sección 7, se comprueba si cada patrón generado fué usado en el entrenamiento de la red, y solamente se usan aquellos que no lo fueron.
           - Se muestran los resultados de precisión.
</details>

## Estructuración del código
<details><summary>Ver Estructuración del código</summary>
  
- Importación de librerias necesarias (PyQt5, sys, os, random, time, math, matplotlib, numpy).
- `resource_path()`: Función para no tener problemas con las rutas en la conversion a .exe. Todos los paths que referencian a archivos externos se pasan a esta función. 
- **Funciones para la creación e impresión de patrones y datasets**:
  - `inicializarPatrones()`: Devuelve los patrones de las 3 letras, en forma de listas de 100 elementos con 1 y 0, usando las posiciones ocupadas por cada letra, considerando la matriz como una lista de 100 elementos (del 0 al 99).
  - `imprimirMatriz()`: Recibe un patrón e imprime la matriz de pixeles.
  - `generarDistorsion()`: Distorsiona el patron pasado un porc% (cambia "porc" veces 0 por 1, y 1 por 0).
  - `generarDataset()`: Retorna el dataset completo, y los conjuntos de entrenamiento, test, y validación generados como se explica [más arriba](https://github.com/angelogllrd/TPI-MLP-Multi-Layer-Perceptron/blob/main/README.md#estructura-de-los-datasets).
  - `cargarDataset()`: Se usa en la 1ra pestaña, con el boton "Cargar". Toma un dataset completo (con los 100, 500 o 1000 ejemplos) y extrae los demás datasets usando la misma lógica que `generarDataset()`.
  - `convertirStringADataset()`: Convierte una string de lista de listas a una estructura de lista de listas. Se usa cuando se carga un dataset desde un .txt.
  - `imprimirDataset1()`: Imprime el dataset en forma gráfica (matrices de los patrones), usando `imprimirMatriz()`.
  - `imprimirDataset2()`: Imprime el dataset en forma tabular.
  - `restarDatasets()`: Quita de un dataset filas de otro. Se lo usa para restar al conjunto de entrenamiento los de validación.
- **Creación de la red y de funciones para el algoritmo**:
  - `crearRed()`: Crea la estructura de la red, con sus capas y neuronas en cada capa, tal como se describe [más arriba](https://github.com/angelogllrd/TPI-MLP-Multi-Layer-Perceptron/blob/main/README.md#estructura-de-la-red-neuronal).
  - `imprimirRed1()`: Muestra el contenido de la red en su estado actual, por cada capa (no se la usa).
  - `imprimirRed2()`: Igual que la anterior, pero muestra la red de forma más ordenada.
  - `inicializarPesos()`: Corresponde al Paso 1. Inicializa los pesos de la red con valores pequeños aleatorios (entre -0.5 y 0.5)
  - `aplicarPatronDeEntrada()`: Corresponde al Paso 2. Presenta un patrón de entrada del dataset, copiándolo a la salida de las neuronas de la capa de entrada. También inserta las salidas deseadas (3 últimos elementos del patrón) en las salidas deseadas de las neuronas de entrada.
  - `calcularSalidasRed()`: Corresponde al Paso 3. Propaga las entradas y calcular las salidas de la red.
  - `calcularNetNeurona()`: Calcula el net de cada neurona. Usado en `calcularSalidasRed()`.
  - `calcularSalidaNeurona()`: Calcula la salida de cada neurona, dependiendo de la capa y la función de transferencia asociada. Usado en `calcularSalidasRed()`.
  - `funcionLineal()`: Recibe el net y devuelve el resultado de la función lineal.
  - `funcionSigmoidal()`: Recibe el net y devuelve el resultado de la función sigmoidal. Además, trata los casos cuando el net pasado es menor a -709.78271, lo que provoca un overflow en la representación en coma flotante.
  - `calcularTerminosErrorRed()`: Corresponde al Paso 4. Calcula los términos de error para neuronas de salida y ocultas, comenzando por las de salida (propagación de errores hacia atrás).
  - `calcularTerminoError()`: Determina un termino de error en base a la capa actual, la neurona actual, y el numero de esa neurona. Usada en `calcularTerminosErrorRed()`.
  - `derivadaFuncionSigmoidal()`: Calcula la derivada de la función sigmoidal. Usada en `calcularTerminoError()`.
  - `actualizarPesosRed()`: Corresponde al Paso 5. Actualiza los pesos de la red.
  - `calcularMSE()`: Corresponde al Paso 6. Calcula el error cuadrático medio entre la salida obtenida y la deseada.
- **UI, definición de clases, atributos y métodos**:
  - `class UI()`: Clase correspondiente a la ventana principal.
    - `uic.loadUi()`: Carga el archivo .ui de la ventana principal.
    - `initUI()`: Hace inicializaciones como: poner nombre a la ventana, centrarla, mostrar en el panel de la derecha la instrucción inicial, colocar el ícono a la ventana, y mostrar la ventana.
    - Antes de los demás métodos, existen secciones para definir atributos:
      - "Labels": Se crea listas con los objetos label de cada matriz de pixeles de la segunda pestaña. Más adelante, recorrer estas listas es lo que permite pintar los patrones en la matriz.
      - "Acciones disparadas por push buttons": Se definen a qué métodos llama cada push button cuando es presionado.
      - "Acciones disparadas por spin boxes": Se define el método llamado cuando cambia el valor de un spin box.
      - "Acciones disparadas por sliders": Se define el método llamado cuando se mueve un slider.
      - "Desactivación inicial de label+spinbox de tamaño de capa oculta 2": Activa la opción de tamaño de la 2da capa oculta, si el spinbox de número de capa ocultas está en 2, o la desactiva si vuelve a 1.  
      - Desactivación inicial del label y botones para mostrar red y datasets: Descativa los botones de la esquina inferior derecha, que sirven para mostrar el contenido de la red y los datasets.
      - Desactivaciones iniciales de la 2da pestaña: Desactiva los elementos de la segunda pestaña, hasta que no se haga el entrenamiento.
      - Inicialización de letra ingresada: Más adelante sirve para saber si ya se presionó o no alguno de los botones de las letras de la segunda pestaña.
    - `center()`: Sirve para centrar la ventana en la pantalla. Llamado en `initUI()`.
    - `mostrarPorConsola()`: Concatena un string al contenido ya existente en el panel negro de la derecha
    - Métodos para la primera pestaña:
      - `generarDataset()`: Verifica si alguno de los radio buttons (100, 500 o 1000) se seleccionó y genera los datasets correspondientes. Llamado por el botón "Generar". Activa el botón "Guardar", la sección de "Arquitectura de la red" y los botones para ver los datasets de Entrenamiento, Test, Validación 10%, Validación 20%, y Validación 30%.
      - `guardarDataset()`: Guarda el dataset generado/cargado como un .txt en la misma ruta del .py. Llamado por el botón "Guardar".
      - `cargarDataset()`: Carga un .txt de un dataset guardado previamente, y genera los datasets correspondientes. Llamado por el botón "Cargar". Activa el botón "Guardar", la sección de "Arquitectura de la red" y los botones para ver los datasets de Entrenamiento, Test, Validación 10%, Validación 20%, y Validación 30%.
      - `tratarSpinBoxCapaOculta2()`: Activa o desactiva el spinbox de tamaño de capa oculta 2 y su label, dependiendo del número de capas ocultas. Llamado por el evento de cambio de valor del spin box de dicho valor.
      - `crearRed()`: Toma los parámetros seleccionados para la red, y crea la estructur. Activa la sección de "Entrenamiento" y el botón de la esquina inferior derecha "Red" para ver el contenido de la red.
      - `entrenarRed()`: De acuerdo a la opción seleccionada, realiza el entrenamiento hasta que el error ingresado resulte aceptablemmente pequeño para cada uno de los patrones del dataset, o durante un número fijo de épocas o patrones. Una vez finalizado el entrenamiento, arroja los resultados. Llamado por el botón "Entrenar". Activa la sección de "Hacer test" y las secciones de la segunda pestaña.
      - `vaciarRed()`: Asigna al atributo "red" una estructura de red vacia. Se usa para resetear la red en cada entrenamiento. Llamado dentro de `entrenarRed()`.
      - `probarDataset()`: Calcula la precisión de la clasificación de los patrones de un dataset, y retorna dicha precisión y el número de clasificaciones correctas.
      - `probarPatron()`: Presenta un patrón a la red, calcula la salida, comprueba si la salida obtenida es igual a la deseada, y devuelve 1 o 0 dependiendo de la coincidencia, las salidas obtenida convertidas a binario, y las salidas sin convertir.
      - `graficarErrores()`: Genera un gráfico comparando los MSE contra las épocas. Llamado por `entrenarRed()`.
      - `hacerTest()`: Calcula la precisión en la clasificación del conjunto de test. Llamado por el botón "Hacer test".
    - Métodos para la segunda pestaña:
      - `tratarLineEditSlider()`: Traslada el valor del slider al line edit de la derecha, a medida que se lo mueve.
      - `tratarLetra()`: Llamado al presionar el botón de alguna de las letras (botones "b", "d", y "f"). Hace que se muestre por "consola" la letra seleccionada, que se muestre en la matriz de pixeles, y guarda dicha letra en su respectivo atributo.
      - `setLetraIngresada`: Guarda la letra seleccionada. Llamado en `tratarLetra()`.
      - `getLetraIngresada()`: Devuelve la letra seleccionada previamente.
      - `mostrarLetra()`: Pinta una matriz de pixeles de acuerdo al patrón pasado.
      - `borrarLetra()`: Pone en blanco una matriz de pixeles.
      - `generarDistorsion()`: Muestra la letra distorsionada en la 1ra matriz. Llamado al presionar el botón "Distorsionar". 
      - `copiarPatron()`: Devuelve una copia del patrón sin distorsionar de la letra pasada.
      - `guardarPatronDistorsionado()`: Guarda una copia del patrón distorsionado en su correspondiente atributo, para que esté disponible a la hora de clasificar.
      - `comprobarPatron()`: Comprueba si un patrón fue usado para el entrenamiento.
      - `clasificarPatron()`: Presenta un patrón a la red y muestra la letra que representa la salida de la misma. Llamado por el botón "Clasificar".
      - `probarPatrones()`: Clasifica un número dado de patrones aleatorios y muestra la precisión resultante. Llamado con el botón "Probar patrones"
    - Métodos para ver contenido de la red y de datasets:
      - `verDataset`: Abre una ventana con el dataset pasado mostrado en forma tabular y gráfica, usando `imprimirDataset1()` e `imprimirDataset2()`.
      - `verRed()`: Abre una ventana que muestra la estructura y contenido actual de la red, usando `imprimirRed2()`.
  - `class UI_dialog_dataset()`: Clase correspondiente a la ventana de visualización de los datasets.
  - `class UI_dialog_red()`: Clase correspondiente a la ventana de visualización de la red.
- Programa principal:
  - Se inicializan los patrones de cada letra.
  - Se inicializa la app
  
</details>
