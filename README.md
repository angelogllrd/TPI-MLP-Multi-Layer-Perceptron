# Análisis MLP (Multi-Layer Perceptron) 
TPI del año 2022 para la asignatura Inteligencia Artificial de la UTN FRRe.

![Portada](https://user-images.githubusercontent.com/51035369/207970240-5a0e859f-dcec-4c65-b7be-68f1d4c2f88f.png)

## Tabla de contenidos
1. [Consigna](#consigna)
2. [Requerimientos para ejecutar el .py](#requerimientos-para-ejecutar-el-py)
3. [Generación del ejecutable (Windows y Linux)](#generación-del-ejecutable-windows-y-linux)
4. [Estructura de los datasets](#estructura-de-los-datasets)
5. [Estructura de la red neuronal](#estructura-de-la-red-neuronal)
6. [Partes de la aplicación](#partes-de-la-aplicación)
7. [Instrucciones de uso de la aplicación](#instrucciones-de-uso-de-la-aplicación)
8. [Estructuración del código](#estructuración-del-código)
9. [Últimos cambios](#últimos-cambios)

## Consigna

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

## Generación del ejecutable (Windows y Linux)

> Descarga de la aplicación: [Windows](https://mega.nz/file/oU8FyKSD#-RtbxVG-4oHusGubdogGGYl_SYHAVaoVxt71JoBLX_U) / [Linux](https://mega.nz/file/tAU12SRS#VqHcc5a4op4hIj1YW2LPBH2J4wZek5jXty73OuoYqhk)
  
Para evitar la instalación de las librerias podemos obtener un ejecutable, tanto en Windows como en Linux, usando [**Auto PY to EXE**](https://dev.to/eshleron/how-to-convert-py-to-exe-step-by-step-guide-3cfi):
  ```
  pip install auto-py-to-exe
  auto-py-to-exe
  ```
<p align="center">
<img width="" height="" src="https://github.com/angelogllrd/TPI-MLP-Multi-Layer-Perceptron/assets/51035369/22d74466-2686-4c99-a8b6-379bdebbde45">
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

- Como se pide en la consigna, los datasets se generan cumpliendo el 10% sin distorsión, y el restante 90% distorsionado entre 1% y 30%. 
- Los datasets se representan usando listas de listas, donde cada sublista es un patrón de entrada o fila del dataset con 103 elementos (1s y 0s), donde los primeros 100 corresponden al patrón y los últimos 3 a las clases, una para cada letra (b, d y f).
- Para asegurar que los conjuntos de test y validación sean representativos, se genera de la siguiente manera, quedando 4 porciones de cada tipo de ejemplo:

<p align="center">
<img width="70%" height="70%" src="https://user-images.githubusercontent.com/51035369/199055338-a007ef82-d296-41e8-af7e-33b57a095ecb.png">
</p>

- Los datasets de test y validación se crean incluyendo ejemplos de cada porción, lo mas similares posibles en cantidad.
- Se estableció que el porcentaje de ejemplos para test debe ser uno que haga divisible por 4 (4 porciones representativas) el número de ejemplos de test para 100, 500 y 1000 ejemplos. Este porcentaje se calculó en un 8%, número que permite que los restantes ejemplos del dataset alcancen para formar todos los conjuntos de validación representativos para los 3 datasets, según los siguientes cálculos:

<p align="center">
<img width="70%" height="70%" src="https://user-images.githubusercontent.com/51035369/199057030-1ae8ed92-41b1-428f-8dfa-4b17188a9445.png">
</p>

- Gráficamente, para un dataset de 1000 ejemplos cuando se toma un 12% para test:

<p align="center">
<img width="70%" height="70%" src="https://user-images.githubusercontent.com/51035369/199052629-9b68372d-e04a-4bd3-a900-6aaade3f6f61.png">
</p>

- La división en los diferentes conjuntos del dataset de 100, 500 o 1000 ejemplos que se genera se puede ilustrar con uno de 100, considerando que siempre tomamos 8% para test y el restante para entrenamiento:

<p align="center">
<img width="90%" height="90%" src="https://user-images.githubusercontent.com/51035369/200608949-5079d736-9e4d-4de4-bb27-749ae0509809.png">
</p>

- En la aplicación, cuando entrenamos, en realidad se llevan a cabo 3 entrenamientos, uno detrás del otro, considerando en cada uno un conjunto de validación distinto:

<p align="center">
<img width="60%" height="60%" src="https://user-images.githubusercontent.com/51035369/200468587-6c6788d5-aaf9-486e-8c34-dc07740d7e4d.png">
</p>

</details>

## Estructura de la red neuronal
  
![200857729-afc1c9ad-a962-4396-a839-d6a528fbf9fc](https://user-images.githubusercontent.com/51035369/202927141-dcfe2b93-417a-4bf3-9c08-080e58c20098.png)

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
  
## Partes de la aplicación
  
> Descarga de la aplicación: [Windows](https://mega.nz/file/oU8FyKSD#-RtbxVG-4oHusGubdogGGYl_SYHAVaoVxt71JoBLX_U) / [Linux](https://mega.nz/file/tAU12SRS#VqHcc5a4op4hIj1YW2LPBH2J4wZek5jXty73OuoYqhk)

La aplicación se divide en 2 pestañas principales: **"Entrenamiento y test"** y **"Probar patrón"**.

### Pestaña **"Entrenamiento y test"**:

<p align="center">
<img width="80%" height="80%" src="https://user-images.githubusercontent.com/51035369/207969597-2aa35650-3756-49aa-ad70-ece770e9da72.png">
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
<img width="60%" height="60%" src="https://user-images.githubusercontent.com/51035369/200910432-b482715f-f92d-496f-a329-06f7fcf55380.png">
</p>

<p align="center">
<img width="60%" height="60%" src="https://user-images.githubusercontent.com/51035369/207969515-69b46ae0-d986-4b06-bc0e-f4d80d46bd6e.png">
</p>    
    
### Pestaña **"Probar patrón"**:

<p align="center">
<img width="80%" height="80%" src="https://user-images.githubusercontent.com/51035369/207969674-5784fa0c-b202-486a-a26d-466c5f977337.png">
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

> Descarga de la aplicación: [Windows](https://mega.nz/file/oU8FyKSD#-RtbxVG-4oHusGubdogGGYl_SYHAVaoVxt71JoBLX_U) / [Linux](https://mega.nz/file/tAU12SRS#VqHcc5a4op4hIj1YW2LPBH2J4wZek5jXty73OuoYqhk)

1. **Generar/Cargar dataset o Seleccionar modelo precargado:**
     
     ![image](https://user-images.githubusercontent.com/51035369/208118316-89d9b5ee-1540-4d16-a0cf-36e23c91335b.png)

     - **Generar/Cargar dataset**
         - En la **Sección 1**, seleccionar el tamaño del dataset a generar, y presionar el botón **"Generar"** (se habilita después de seleccionar un tamaño). También es posible usar el botón **"Cargar"** para cargar el archivo .txt de un dataset guardado previamente con la aplicación. Opcionalmente, luego de cargar/generar un dataset, se habilita el botón **"Guardar"**, que guarda el dataset en la carpeta "datasets" en la ruta del ejecutable.
       
           ![2022-11-07 22_44_46-Window](https://user-images.githubusercontent.com/51035369/200431389-a95e57ff-46a4-4903-b72c-c0e95898df82.png)
       
         - La generación o la carga de un dataset produce la división del mismo en dos partes: entrenamiento y test. A su vez, con ejemplos del dataset de entrenamiento se forman los 3 conjuntos de validación. Por lo tanto, **los conjuntos o datasets resultantes son 5**.
       
           ![2022-11-07 22_29_20-Window](https://user-images.githubusercontent.com/51035369/200432193-eecdced6-9646-4d58-b746-2d9679c12888.png)
       
         - Luego, se habilita la **Sección 2** para crear una estructura de red, y los botones de la **Sección 6** para ver los diferentes conjuntos formados.
       
           ![2022-11-07 22_49_43-Window](https://user-images.githubusercontent.com/51035369/200432402-0466b0b8-1958-47a1-81f4-a8971f5fa602.png)
     
     - **Seleccionar modelo precargado**:
         - Alternativamente, podemos ahorrarnos entrenar una red y cargar una red/modelo ya entrenado seleccionando uno de los 72 modelos precargados en la **Sección 4** (para hacer test) o en la **Sección 7** (para probar patrones). En el primer caso, se habilita el resto de la **Sección 4**, y en el segundo la **Sección 8** y la **Sección 9**:
         
           ![7](https://user-images.githubusercontent.com/51035369/208119635-bb938749-aa3b-4bda-b5d7-6f2908acab2a.png)
         
         - Seguir por el **Paso 4** o el **Paso 5**.
  
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
       
       - **Seleccionar un error aceptable:** El entrenamiento termina cuando el Error de entrenamiento promedio (promedio de los MSE de cada patrón en una época) resulta por debajo del error aceptable ingresado. Opcionalmente, descomentando el código de la primera imágen (dentro de `entrenarRed()`) y comentando el código de la segunda, el entrenamiento terminará cuando el error de entrenamiento de CADA patrón esté por debajo del error aceptable.
         
         ![2022-12-16 11_30_26-Window](https://user-images.githubusercontent.com/51035369/208120635-8c00443f-1c81-4492-90b5-f29cd6bd5b69.png)

         ![2022-12-16 11_30_52-Window](https://user-images.githubusercontent.com/51035369/208120655-d23afab6-13e5-48f3-af8f-277ae96c0c98.png)
         
         Con esta opción de fin, y para evitar que el entrenamiento se prolongue indefinidamente cuando la red no converge (o lo hace muy lento), la aplicación genera una alerta cuando detecta que el error de cierta cantidad de las últimas épocas es el mismo (comparando cierta cantidad de decimales de los errores). La alerta ofrece la opción de **Parar** el entrenamiento o **Seguir** con el mismo (hasta detectar la misma situación):
         
         ![2022-11-20 21_36_03-Acción requerida](https://user-images.githubusercontent.com/51035369/202963265-abf05e27-7aa7-4249-aef5-fddf37c3ace2.png)
         
       - **Seleccionar un número de épocas/iteraciones fijo**: El entrenamiento se hace por un número de épocas fijado, independientemente del Error de entrenamiento como en el caso anterior.
     - Una vez seleccionada una opción, presionar el botón **"Entrenar"** para comenzar el entrenamiento. En realidad, esto lleva a cabo 3 entrenamientos (considerando en cada uno un conjunto de validación distinto). En cada uno de esos 3 entrenamientos:
       - Se restan o quitan los ejemplos de uno conjunto de validación al dataset de entrenamiento original, y se entrena con el conjunto resultante. 
       - Al final de cada época dentro de ese entrenamiento, se resguarda el Error de entrenamiento (promedio de los errores de cada patrón en la época) y el Error de validación (promedio de los errores resultantes al aplicar cada uno de los patrones del conjunto de validación a la red), para poder generar los gráficos de MSE promedio vs. Épocas.
       - Al final, se guarda la red entrenada (con los pesos resultantes), para ser seleccionada en la etapa de test o en la prueba de patrones (segunda pestaña). Por lo tanto, al final de la etapa de entrenamiento quedan guardadas 3 redes entrenadas (misma arquitectura, entrenada considerando 3 conjuntos de validación). Internamente, también se guarda la arquitectura de la red, y los conjuntos de entrenamiento, test y validación asociados (estos últimos porque se los necesita para más adelate y corren el riesgo de ser sobreescritos al crear un nuevo dataset).
     - Al finalizar el entrenamiento, se muestran:
       - **Resultados:** Épocas que llevó el entrenamiento, Error de entrenamiento de la última época, y Error de validación de la última época.
       
           ![2022-12-16 11_33_00-TPI MLP 2022 - Inteligencia Artificial - UTN FRRe](https://user-images.githubusercontent.com/51035369/208121122-b7d0e3e0-ab07-4130-9111-9b7d69a8d0cb.png)

       - **Gráficos de MSE promedio vs. Épocas:** Cada gráfico representa el Error de entrenamiento y Error de validación por cada época.

           ![Figure_1](https://user-images.githubusercontent.com/51035369/208121238-6d0fc70c-5169-4a6b-926d-537ccef63b1d.png)

     - Se habilita el botón "Guardar redes", que guarda las 3 redes que se acaban de entrenar como archivos .json en la carpeta "redes_entrenadas" en la ruta del ejecutable.
       
       ![image](https://user-images.githubusercontent.com/51035369/208121507-fa854a29-72dc-4c02-bccd-2bf0d9350e11.png)

     
En este momento podemos elegir realizar el test, o bien ir a la segunda pestaña para probar patrones distorsionados

4. **Realizar el test**:
     - En la **Sección 4** seleccionar, en primer lugar, el tipo de modelo a cargar:
       - Uno de los 72 modelos precargados,
       - Una de las redes que se entrenaron desde el inicio de la aplicación:
       
       ![image](https://user-images.githubusercontent.com/51035369/208122011-3ddf988f-081e-4792-ae5e-3851e8841f01.png)
  
     - Luego seleccionar el modelo en la segunda lista (esto habilita el resto de la sección):
  
       ![image](https://user-images.githubusercontent.com/51035369/208123252-9fc07330-982b-4a03-aaef-33d419fd6a75.png)

     - Presionar el botón "Hacer test". Esto inserta los patrones del dataset de test guardado en la red seleccionada, en dicha red. Luego calcula las salidas, detecta la letra representada por las salidas y la compara con la salida deseada, obteniendo el número de clasificaciones correctas.
     - Se muestran los resultados (Clasificaciones correctas, números de casos de prueba, y la precisión, calculada a partir de los dos primeros), junto con el gráfico de los Errores por cada patrón.
  
       ![image](https://user-images.githubusercontent.com/51035369/208122516-be282f34-1af3-4b37-9e96-7b583195c3bd.png)
     
       ![image](https://user-images.githubusercontent.com/51035369/208122354-e533d316-c010-4dff-a7b4-ee8ba32b5488.png)

5. **Probar patrones** (segunda pestaña):
     - En la **Sección 7** seleccionar, en primer lugar, el tipo de modelo a cargar:
       - Uno de los 72 modelos precargados,
       - Una de las redes que se entrenaron desde el inicio de la aplicación:
  
       ![image](https://user-images.githubusercontent.com/51035369/208123056-d2205db5-0c5d-478b-b9c6-a71d324940c6.png)

     - Luego seleccionar el modelo en la segunda lista. Esto carga la red seleccionada como red actual, junto con los datasets guardados con la misma (los datasets de entrenamiento y validación guardados en la red seleccionada se usan para comprobar si un patrón aleatorio fué usado en el entrenamiento de esa red), y habilita la **Sección 8** y la **Sección 9**:
  
       ![image](https://user-images.githubusercontent.com/51035369/208123597-42ec688c-2ad4-4620-a958-d269d6268f30.png)

     - Luego, tenemos 2 opciones:
       - **Sección 8: Generar y clasificar un patrón con distorsión aleatoria**

           ![image](https://user-images.githubusercontent.com/51035369/208124414-a4b6a7e9-bce7-4b63-b956-492bf3906e94.png)

           - Seleccionar una letra con uno de los 3 botones (se muestra la letra en la matriz de pixeles).
           - Seleccionar la distorsión a generar. **ACLARACIÓN**: El programa comprueba si el patrón distorsionado resultante es uno de los patrones usados para entrenar la red. Si lo fué, se muestra "Si" en el label "¿Patrón usado para entrenar?", mientras que si no, se muestra "No".
           - Presionar el botón "Distorsionar" (se muestra la letra distorsionada en la matriz de pixeles). Esto habilita la parte derecha de la Sección 8, donde clasificamos la letra distorsionada.
           - Presionar el botón "Clasificar". Se muestra la letra que representa la salida de la red al insertar el patrón distorsionado, junto con los valores de salida que se usaron para clasificar la letra.
       - **Sección 9: Generar y clasificar un número dado de patrones con distoriones aleatorias**:

           ![image](https://user-images.githubusercontent.com/51035369/208124626-dfce57a8-a0ca-405b-aedb-e9621ed5ccc8.png)

           - Ingresar el número de patrones distorsionados a generar.
           - Presionar el botón "Probar patrones". Se muestra a la izquierda la matriz de pixeles con cada patrón generado, junto con la letra clasificada a la derecha. **ACLARACIÓN**: Al igual que en la Sección 8, se comprueba si cada patrón generado fué usado en el entrenamiento de la red, y solamente se usan aquellos que no lo fueron.
           - Se muestran los resultados de precisión.
</details>

## Estructuración del código
  
- Importación de librerias necesarias (PyQt5, sys, os, random, time, math, json, matplotlib, numpy).
- `resource_path()`: Función para no tener problemas con las rutas en la conversion a .exe. Todos los paths que referencian a archivos externos se pasan a esta función. 
- **FUNCIONES PARA LA CREACIÓN E IMPRESIÓN DE PATRONES Y DATASETS**:
  - `inicializarPatrones()`: Devuelve los patrones de las 3 letras, en forma de listas de 100 elementos con 1 y 0, usando las posiciones ocupadas por cada letra, considerando la matriz como una lista de 100 elementos (del 0 al 99).
  - `imprimirMatriz()`: Recibe un patrón e imprime la matriz de pixeles con * en cada pixel pintado. Se la usa solamente para pruebas en `generarDataset()`.
  - `generarDistorsion()`: Distorsiona el patron pasado un porc% (cambia "porc" veces 0 por 1, y 1 por 0).
  - `generarDataset()`: Retorna el dataset completo, y los conjuntos de entrenamiento, test, y validación generados como se explica [más arriba](https://github.com/angelogllrd/TPI-MLP-Multi-Layer-Perceptron/blob/main/README.md#estructura-de-los-datasets).
  - `cargarDataset()`: Se usa en la 1ra pestaña, con el boton "Cargar". Toma un dataset completo (con los 100, 500 o 1000 ejemplos) y extrae los demás datasets usando la misma lógica que `generarDataset()`.
  - `imprimirDatasetGraficoConAsteriscos()`: Imprime el dataset en forma gráfica (matrices de los patrones) con * en cada pixel pintado, dispuesto en "cant_filas" filas de "patrones_por_fila" patrones.
  - `imprimirDatasetGraficoConPosiciones()`: Imprime el dataset en forma gráfica (matrices de los patrones) con la posición en cada pixel pintado, dispuesto en "cant_filas" filas de "patrones_por_fila" patrones.
  - `imprimirDatasetTabular()`: Imprime el dataset en forma tabular.
  - `restarDatasets()`: Quita de un dataset filas de otro. Se lo usa en `entrenarRed()` para restar al conjunto de entrenamiento los de validación, y en `comprobarPatron()` para obtener los ejemplos usados en el entrenamiento de una red y comprobar si un patrón fue usado para el entrenamiento.
- **CREACIÓN DE LA RED Y DE FUNCIONES PARA EL ALGORITMO**:
  - `crearRed()`: Crea la estructura de la red, con sus capas y neuronas en cada capa, tal como se describe [más arriba](https://github.com/angelogllrd/TPI-MLP-Multi-Layer-Perceptron/blob/main/README.md#estructura-de-la-red-neuronal).
  - `imprimirRed()`: Muestra el contenido de la red en su estado actual, por cada capa.
  - `dibujarTituloCapa()`: Usado en `imprimirRed()`. Dibuja el título recuadrado de una capa.
  - `inicializarPesos()`: Corresponde al **Paso 1**. Inicializa los pesos de la red con valores pequeños aleatorios (entre -0.5 y 0.5)
  - `aplicarPatronDeEntrada()`: Corresponde al **Paso 2**. Presenta un patrón de entrada del dataset, copiándolo a la salida de las neuronas de la capa de entrada. También inserta las salidas deseadas (3 últimos elementos del patrón) en las salidas deseadas de las neuronas de salida.
  - `calcularSalidasRed()`: Corresponde al **Paso 3**. Propaga las entradas y calcula las salidas de la red.
  - `calcularNetNeurona()`: Calcula el net de cada neurona. Usado en `calcularSalidasRed()`.
  - `calcularSalidaNeurona()`: Calcula la salida de cada neurona, dependiendo de la capa y la función de transferencia asociada. Usado en `calcularSalidasRed()`.
  - `funcionLineal()`: Recibe el net y devuelve el resultado de la función lineal.
  - `funcionSigmoidal()`: Recibe el net y devuelve el resultado de la función sigmoidal. Además, trata los casos cuando el net pasado es menor a -709.78271, lo que provoca un overflow en la representación en coma flotante.
  - `calcularTerminosErrorRed()`: Corresponde al **Paso 4**. Calcula los términos de error para neuronas de salida y ocultas, comenzando por las de salida (propagación de errores hacia atrás).
  - `calcularTerminoError()`: Determina un termino de error en base a la capa actual, la neurona actual, y el numero de esa neurona. Usada en `calcularTerminosErrorRed()`.
  - `derivadaFuncionSigmoidal()`: Calcula la derivada de la función sigmoidal. Usada en `calcularTerminoError()`.
  - `actualizarPesosRed()`: Corresponde al **Paso 5**. Actualiza los pesos de la red.
  - `calcularMSE()`: Corresponde al **Paso 6**. Calcula el error cuadrático medio entre la salida obtenida y la deseada.
- **OTRAS FUNCIONES**:
  - `convertirErrorAString()`: Convierte un error (flotante) a un string del mismo, considerando que puede estar en notación científica. Se usa porque el formateo de strings para tomar cierta cantidad de cifras decimales redondea la última cifra de acuerdo a los valores siguientes. Por ejemplo, `f'{0.123456789:.8f}'` quedaría `'0.12345679'`, cuando debería ser `'0.12345678'`. El redondeo ocasiona que la comparación de las cifras decimales para verificar errores repetidos no se haga correctamente.
- **UI, DEFINICIÓN DE CLASES, ATRIBUTOS Y MÉTODOS**:
  - `class UI()`: Clase correspondiente a la ventana principal.
    - `uic.loadUi()`: Carga el archivo .ui de la ventana principal.
    - `initUI()`: Hace inicializaciones como: poner nombre a la ventana, centrarla, mostrar en el panel de la derecha la instrucción inicial, colocar el ícono a la ventana, y mostrar la ventana.
    - **ATRIBUTOS, ACCIONES DISPARADAS, INICIALIZACIONES, DESACTIVACIONES:**
      - "Labels": Se crea listas con los objetos label de cada matriz de pixeles de la segunda pestaña. Más adelante, recorrer estas listas es lo que permite pintar los patrones en la matriz.
      - "Acciones disparadas por pushbuttons": Se define a qué métodos llama cada pushbutton cuando es presionado.
      - "Acciones disparadas por spinboxes": Se define el método llamado cuando cambia el valor de un spinbox.
      - "Acciones disparadas por radiobuttons": Se define el método llamado cuando se selecciona un radiobutton.
      - "Acciones disparadas por sliders": Se define el método llamado cuando se mueve un slider.
      - "Acciones disparadas por comboboxes": Se define el método llamado cuando se selecciona un elemento de la lista de un combobox.
      - "Desactivaciones iniciales de sección Arquitectura de la red": Desactivaciones necesarias de elementos de la Sección 2.
      - "Desactivaciones iniciales de sección Entrenamiento": Desactivaciones necesarias de elementos de la Sección 3.
      - "Desactivaciones iniciales de sección Test": Desactivaciones necesarias de elementos de la Sección 4.
      - "Desactivación inicial del label y botones para mostrar red y datasets": Desactivaciones necesarias de elementos de la Sección 6.
      - "Desactivaciones iniciales de la segunda pestaña": Desactiva necesarias de elementos de la Sección 8 y Sección 9.
      - "Inicializaciones varias": de los atributos `letraIngresada` (más adelante sirve para saber si ya se presionó o no alguno de los botones de las letras de la segunda pestaña), `funcionDeActivacionSal` (define queé función de transferencia se usa en las neuronas de la capa de salida), `listaRedesEntrenadas` (guarda las redes que entrenamos desde el inicio de la aplicación), y `listaRedesPrecargadas` (guarda las redes/modelos ya entrenados que se cargan al inicio de la aplicación).
      - "Definición de arquitecturas predefinidas": Se define una tupla de diccionarios con las características de las arquitecturas dadas en el TPI.
      - "Inicialización de combobox de arquitecturas predefinidas": Para cada arquitectura listada en el combobox de la Sección 2 se carga por detrás los datos de su estructura, definidos en el ítem anterior.
      - "Carga de redes precargadas": Se encarga de cargar, al inicio de la aplicación, las redes precargadas en el 2do combobox de las secciónes 4 y 7.
    - **MÉTODOS DE CLASE:**
        - `center()`: Sirve para centrar la ventana en la pantalla. Llamado en `initUI()`.
        - `mostrarPorConsola()`: Concatena un string al contenido ya existente en el panel negro de la derecha.
        - `desactivarEsto()`: Recibe una tupla de cosas de la interfaz para desactivar.
        - `activarEsto()`: Recibe una tupla de cosas de la interfaz para activar.
        - `generarAlerta()`: Genera una alerta cuando se detecta que el entrenamiento produjo el mismo error (considerando cierta cantidad de dígitos decimales) durante cierta cantidad de décadas, brindando la opción de "Parar" o "Seguir" el entrenamiento. Su función es brindar al usuario la opción de parar el entrenamiento cuando el error no baja, o baja muy lentamente.
        - `animarEsto()`: Muestra una animación resaltando una sección cuando la misma se activa.
      - **MÉTODOS PARA LA PRIMERA PESTAÑA:**
        - `generarDataset()`: Verifica si alguno de los radio buttons (100, 500 o 1000) se seleccionó y genera los datasets correspondientes. Llamado por el botón "Generar". Activa el botón "Guardar", la sección de "Arquitectura de la red" y los botones para ver los datasets de Entrenamiento, Test, Validación 10%, Validación 20%, y Validación 30%.
        - `guardarDataset()`: Guarda el dataset generado/cargado como un .txt dentro de la carpeta "datasets" en la misma ruta del ejecutable. Llamado por el botón "Guardar".
        - `cargarDataset()`: Carga un .txt de un dataset guardado previamente con la aplicación, y genera los datasets correspondientes. Llamado por el botón "Cargar". Activa el botón "Guardar", la sección de "Arquitectura de la red" y los botones para ver los datasets de Entrenamiento, Test, Validación 10%, Validación 20%, y Validación 30%.
        - `desactivarSeñales()`: Bloquea las señales producidas por cambios de valores en los parámetros de la Sección 2 (cambios en spinboxes, combobox de función de transferencia, textedit de alfa y beta), para que los cambios en dichos valores producidos automáticamente **por la aplicación** cuando se selecciona una arquitectura predefinida de la lista del combobox de dicha Sección 2 no dispare la detección que se hace al cambiar dichos valores **manualmente** (dicha detección pretende detectar si la configuración manual de la arquitectura coincide con una predefinida y seleccionarla en la lista), lo que generaría resultados no deseados. De esta manera, la detección solamente se produce cuando los cambios de parámetros son manuales.
        - `tratarArquitecturaPredefinida()`: Carga automáticamente los parámetros de la arquitectura predefinida seleccionada en el combobox de la Sección 2. Usa `desactivarSeñales()` para desactivar la detección del cambio de valor en los parámetros, cambia los valores, y vuelve a activar las señales.
        - `tratarCambioParametrosArq()`: Por un lado comprueba, ante un cambio de parámetro de la Sección 2, si los parametros coinciden con los de una arquitectura predefinida, y la selecciona en la lista del combobox. Por el otro, activa o desactiva el spinbox de tamaño de capa oculta 2 y su label, llamando a `tratarSpinBoxCapaOculta2()`.
        - `tratarSpinBoxCapaOculta2()`: Activa o desactiva el spinbox de tamaño de capa oculta 2 y su label, dependiendo del número de capas ocultas.
        - `crearRed()`: Toma los parámetros seleccionados para la red, y crea la estructura. Activa parte de la Sección 3 (Entrenamiento) y el botón de la esquina inferior derecha "Red actual" para ver el contenido de la red.
        - `entrenarRed()`: Realiza 3 entrenamientos, en cada uno considerando un conjunto de validación diferente. De acuerdo a la condición de fin seleccionada, realiza cada entrenamiento hasta que el Error de entrenamiento o Error global (MSE promedio de una época) sea menor que el error aceptable ingresado, o durante un número fijo de épocas o iteraciones. Dentro de cada entrenamiento y por cada época también se calcula el Error de validación. Una vez finalizados los 3 entrenamientos, arroja los resultados por cada uno (épocas que consumió, Error de entrenamiento y Error de validación de la última época). Llamada por el botón "Entrenar". Activa el botón "Guardar redes" de la misma sección.
        - `mostrarErrorEpoca()`: Usado dentro de `entrenarRed()`. Muestra por la consola de la aplicación el error de entrenamiento al terminar una época.
        - `guardarRedEntrenada()`: Guarda una red entrenada para poder usarla en la etapa de test o para probar patrones distorsionados, y la lista en el 2do combobox de las Secciones 4 y 7. Para listarla, comprueba si tiene una arquitectura predefinida. Si la tiene, busca el ítem de dicha arquitectura en el combobox de la Sección 2 y obtiene el texto que la describe. Si no, forma la descripción. Además de la red, guarda su estructura (para actualizar atributos de clase cuando la cargo), el dataset de test, de entrenamiento y el conjunto de validación correspondiente al entrenamiento, de manera de poder usarlos en cualquier momento. Llamada dentro de `entrenarRed()`.
        - `tratarComboboxTipoModelo()`: Es llamada cuando seleccionamos una de las 2 opciones del 1er. combobox de las Secciones 4 y 7, y se encarga de cargar la lista de redes precargadas o recién entrenadas en el 2do combobox de dichas secciones.
        - `esArquitecturaPredefinida()`: Comprueba si la red actual tiene una arquitectura predefinida. Si la tiene, retorna el string que la describe, tal como está en el combobox de la Sección 2. Si no, retorna string vacío. En ambos casos, retorna en segundo lugar la estructura de la arquitectura (necesaria par actualizar atributos al cargar una red). Llamada dentro de `guardarRedEntrenada()`.
        - `finalizarEntrenamiento()`: Agrupa operaciones comunes a los entrenamientos con las dos condiciones de fin, para evitar repetición de código. Llamada dentro de `entrenarRed()`.
        - `guardarRedesEntrenadas()`: Guarda las últimas redes entrenadas en la Sección 3 (las 3 redes entrenadas, cada una con un conjunto de validación distinto), y los datasets de entrenamiento, test y validación asociados en archivos .json dentro de la carpeta "redes_entrenadas" en el directorio del ejecutable. 
        - `vaciarRed()`: Asigna al atributo "red" una estructura de red vacía. Se usa para resetear la red en cada entrenamiento. Llamado dentro de `entrenarRed()`.
        - `probarDataset()`: Calcula las clasificaciones correctas de los patrones de un dataset, la precisión, el error promedio y obtiene la lista de errores o MSEs, y retorna esos cuatro elementos. Llamada dentro de `hacerTest()`, `probarPatrones()`, y `entrenarRed()`.
        - `probarPatron()`: Presenta un patrón a la red, calcula la salida, comprueba si la salida obtenida es igual a la deseada, y devuelve 1 o 0 dependiendo de la coincidencia, el error, y las salidas obtenidas convertidas a binario, y sin convertir. Llamada dentro de `probarDataset()`, y `clasificarPatron()`.
        - `graficarErrores()`: Genera 3 gráficos, uno por cada uno de los 3 entrenamientos que se hacen al presionar el botón "Entrenar", comparando Errores de entrenamiento y Validación contra las épocas. Llamado por `entrenarRed()`.
        - `hacerTest()`: Toma del 2do combobox de la Sección 4 la red seleccionada, prueba el dataset de test en ella, muestra resultados de precisión, y el gráfico de error de test. Llamada por el botón "Hacer test".
        - `tratarComboboxTest()`: Llamada cuando se selecciona del 2do combobox de la Sección 4 una red entrenada o precargada. Activa el resto de la sección "Test", carga como red actual la red seleccionada en el combobox, y resguarda el dataset de test correspondiente al entrenamiento de la red cargada para poder usarlo en la etapa de test.
        - `cargarRedSeleccionada()`: Llamada cuando se selecciona del 2do combobox de la Sección 4 o de la Sección 7 una red entrenada. Carga como red actual la red seleccionada en el combobox pasado, y retorna los datasets de entrenamiento, test y validación usados en el entrenamiento de la red cargada. Llamada en `tratarComboboxTest()` y en `tratarComboboxProbarpatron()`.
      - **MÉTODOS PARA LA SEGUNDA PESTAÑA:**
        - `tratarComboboxProbarpatron()`:  Llamada cuando se selecciona del 2do. combobox de la Sección 7 una red entrenada o precargada. Activa nuevas funciones de la pestaña "Probar patrón", carga como red actual la red seleccionada en el combobox, y resguarda los datasets de entrenamiento y validación correspondiente al entrenamiento de la red cargada para poder usarlos en `comprobarPatron()`.
        - `tratarLineEditSlider()`: Traslada el valor del slider al line edit de la derecha, a medida que se lo mueve.
        - `tratarLetra()`: Llamado al presionar el botón de alguna de las letras (botones "b", "d", y "f"). Hace que se muestre por "consola" la letra seleccionada, que se muestre en la matriz de pixeles, y guarda dicha letra en su respectivo atributo.
        - `setLetraIngresada`: Guarda la letra seleccionada. Llamada en `tratarLetra()`.
        - `getLetraIngresada()`: Devuelve la letra seleccionada previamente. Llamada por `generarDistorsion()`.
        - `mostrarLetra()`: Pinta una matriz de pixeles de acuerdo al patrón pasado. Llamada por `tratarLetra()`, `generarDistorsion()`, y `probarPatrones()`.
        - `borrarLetra()`: Pone en blanco una matriz de pixeles. Llamada por `mostrarLetra()`.
        - `generarDistorsion()`: Muestra la letra distorsionada en la 1ra matriz. Llamado al presionar el botón "Distorsionar" y por `probarPatrones()`.
        - `copiarPatron()`: Devuelve una copia del patrón sin distorsionar de la letra pasada. Llamada por `generarDistorsion()` y por `probarPatrones()`.
        - `guardarPatronDistorsionado()`: Guarda una copia del patrón distorsionado en su correspondiente atributo, para que esté disponible a la hora de clasificar. Llamada por `generarDistorsion()`.
        - `comprobarPatron()`: Comprueba si un patrón fue usado para el entrenamiento. Llamada por `generarDistorsion()` y `probarPatrones()`.
        - `clasificarPatron()`: Presenta un patrón a la red y muestra la letra que representa la salida de la misma. Llamado por el botón "Clasificar" y por `probarPatrones()`.
        - `probarPatrones()`: Clasifica un número dado de patrones aleatorios y muestra la precisión resultante. Llamado con el botón "Probar patrones".
      - **MÉTODOS PARA VER CONTENIDO DE LA RED Y DE DATASETS**:
        - `verDataset`: Abre una ventana con el dataset pasado mostrado en forma tabular y gráfica, usando `imprimirDataset1()` e `imprimirDataset2()`.
        - `verRed()`: Abre una ventana que muestra la estructura y contenido actual de la red, usando `imprimirRed2()`.
  - `class UI_dialog_dataset()`: Clase correspondiente a la ventana de visualización de los datasets.
  - `class UI_dialog_red()`: Clase correspondiente a la ventana de visualización de la red.
- **PROGRAMA PRINCIPAL**:
  - Se inicializan los patrones de cada letra.
  - Se inicializa la app
  
</details>

## Últimos cambios

### Cambios posteriores a la entrega del 9/11
- Agregados tooltips a todos los botones y comboboxes.
<p align="center"><img width="" height="" src="https://user-images.githubusercontent.com/51035369/202962752-49a0f731-8acb-4a6e-b0c0-e86847383e3f.gif"></p>

- Cambiada la presentación de resultados:
  - Los resultados ya no se muestran con notación científica.
    <p align="center"><img width="" height="" src="https://user-images.githubusercontent.com/51035369/208113320-9dd5aeee-0e60-43cc-8461-55f1d99fe484.png"></p>
  - Los errores en los resultados del entrenamiento se muestran con una precisión de hasta 8 dígitos decimales.  
  - Los valores de precisión se muestran en forma de porcentaje con 2 dígitos decimales.
    <p align="center"><img width="" height="" src="https://user-images.githubusercontent.com/51035369/208113733-110dedc6-5bdf-4a14-89b4-0677e6b299ae.png"></p>
  - Al clasificar un patrón, las salidas de las neuronas de salida se muestran en forma de porcentaje con 2 dígitos decimales.
    <p align="center"><img width="" height="" src="https://user-images.githubusercontent.com/51035369/208113801-8e2e6a50-5583-48a9-abf1-061b77ca5762.png"></p>
- Se dejó de usar el corte automático a las 200 épocas, que prolongaba demasiado el entrenamiento para datasets muy grandes (500 y 100 ejemplos), y, en cambio, se agregó una ventana de alerta cuando el entrenamiento produce el mismo error (considerando cierta cantidad de cifras decimales en el error) durante cierta cantidad de épocas, a fin de ofrecer la opción de cortar el entrenamiento cuando la red no converge (o converge muy lento). 
<p align="center"><img width="" height="" src="https://user-images.githubusercontent.com/51035369/202961615-cc5e8e9f-c4b7-4b7f-abd7-43a5c8b421bc.png"></p>

- Los errores repetidos y la cantidad de cifras consideradas para comparar los errores se puede modificar en las siguientes líneas:
<p align="center"><img width="" height="" src="https://user-images.githubusercontent.com/51035369/208113966-377954be-1a84-4910-9cc2-53a1d2b86c3f.png"></p>

- Mejorada la representación de las informaciones mostradas por la consola de la aplicación. Se agregó espaciado entre renglones y ahora se listan los errores producidos por cada época durante el entrenamiento.
<p align="center"><img width="50%" height="50%" src="https://user-images.githubusercontent.com/51035369/208114057-180a9813-f0d5-4d8f-8437-d4f1f62136dd.png"></p>

- Se mejoró la representación del contenido de la red (botón "Red actual"). Se organizaron matricialmente las neuronas de entrada (para evitar una lista larga de 100 neuronas) y se agregó un recuadro a cada capa para distinguir mejor cuando comienza cada una.
<p align="center"><img width="" height="" src="https://user-images.githubusercontent.com/51035369/202963076-1cb53936-241f-4165-be1b-5efd4a797393.png"></p>

- Se agregó una animación de resaltado para distinguir cuando se activa una sección nueva en la aplicación.
  
  <p align="center"><img width="" height="" src="https://user-images.githubusercontent.com/51035369/202929260-9ae04f62-61d5-42e4-8e7d-06c9b793e4e1.gif"></p>
  
- Se quitaron los "ticks" fijos del eje x en el gráfico de Errores vs Épocas, lo que provocaba que cuando las épocas eran muchas (>100), los números quedaran muy juntos. Ahora, matplotlib los genera automáticamente. Lo que antes era la época 1, ahora se indica con 0, y lo que era la época *n* ahora es la época *n-1*. Lo mismo para el gráfico de error de test.
  <p align="center"><img width="" height="" src="https://user-images.githubusercontent.com/51035369/208114256-3b1dd850-c89a-44fc-8211-55b65e22200d.png"></p>
  <p align="center"><img width="" height="" src="https://user-images.githubusercontent.com/51035369/208114683-e1e96da5-43d3-418f-b175-5e18e383a0e5.png"></p>

- Ahora se permite hacer las inferencias con modelos precargados, sin obligarme a entrenarlos antes. Dichos modelos se cargan al inicio de la aplicación, y son los 72 modelos generados en las 72 pruebas solicitadas en la consigna:

  ![7](https://user-images.githubusercontent.com/51035369/208116225-5726087f-54ab-4445-a782-ba2996a48f03.png)

</details>
