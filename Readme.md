<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**Machine Learning Operations (MLOps)**</h1>

<p align="center">
<p align=center><img src=https://iasolver.es/wp-content/uploads/2021/05/mlops-768x338.png><p>
</p>



# <h1 align=center> **Introducción** </h1>
En este primer proyecto, hemos explorado y aplicado técnicas de Machine Learning a través de un flujo de trabajo que abarca desde la Extracción, Transformación y Carga ***(ETL)*** de datos hasta el Análisis Exploratorio de Datos ***(EDA)*** y el ***Modelado de algoritmos***.
El proceso se realizó principalmente para llegar a un modelo de Machine Learning predictivo enfocado a videjojuegos de la plataforma Steam.
En este README, se encontrará información esencial sobre cómo acceder a los recursos, cómo ejecutar el modelo, y una breve descripción de el proceso que seguimos para lograr los resultados que aquí presentamos. 


# <h1 align=center> **Descripción** </h1>


En la primera fase de nuestro proyecto, creamos un archivo denominado [Etl.ipynb](/Etl.ipynb) con el propósito de llevar a cabo el proceso de Extracción, Transformación y Carga (ETL) de datos. Este proceso se centró en la obtención de datos, su transformación para su posterior uso, y la corrección de posibles problemas, como valores nulos o errores en los conjuntos de datos. Un ejemplo destacado fue la manipulación de una columna que contenía listas de diccionarios.

Posteriormente, nos adentramos en el Análisis Exploratorio de Datos (EDA) que se encuentra en el archivo [Eda.ipynb](/Eda.ipynb), donde se realizó una visualización de los datos clave que influirían en nuestro proceso de modelado. En el contexto de videojuegos, generamos gráficos informativos, como el top 3 de juegos más recomendados, la frecuencia de géneros, los cinco principales desarrolladores, entre otros elementos relevantes.

Finalmente, el proceso de modelado se centró en la creación de una función que, tomando como parámetro un ID de usuario, retornó cinco recomendaciones de videojuegos. Este proceso fue el punto culminante de nuestro proyecto y constituye una parte fundamental de nuestro trabajo. Este archivo se llama [Machine_learning2.ipynb](/Machine_learning2.ipynb), el cual tiene el desarrollo del modelamiento.



# <h1 align=center> **ETL (Extracción, Transformación y carga de deatos)** </h1>

Para el procesamiento [Etl.ipynb](/Etl.ipynb), se realizó trabajo que desempeña un Data Engineer, lo cual se realizaron los siguientes puntos para 3 diferentes datasets que se nos presentaron: games,reviews e items:

* Importamos las librerías necesarias y poder hacer primeramente la lectura de los archivos tipo Json.
* Para un mejor procesamiento, convertimos cada archivo a Dataframe con ayuda de pandas y dar una visualización breve del df para ver a lo que nos enfrentaremos para las transformaciones de datos.
* En dos df (reviews e items) particulares se observaron columnas con listas de diccionarios, se realizó el procedimiento de hacer explode para desanidar esas listas y trabajar los datos.
* Se realizó la eliminación de columnas que no se consideraron importantes.
* Observacion de filas con valores vacíos/nulos, errores en tipos de dato.
* Se realizó la sustitución, eliminación o conversión de dichos valores en base al criterio.
* Finalmente toda esa data obtenida lista para trabajarse, la almacenamos en la carpeta [data](/data). Los df fueron almacenados en formato parquet, elegimos dicho formato con la finalidad de ahorrarnos peso de archivo, ya que comparado con otras opciones como en csv conviene mejor formato parquet, aparte que es de gran ayuda para ser consumidos por la aplicación de Fast Api.




# <h1 align=center> **EDA (Análisis Exploratorio de Datos)** </h1>

Podemos seguir el proceso del Análisis en el archivo [Eda.ipynb](/Eda.ipynb), en este punto lo afrontamos de la siguiente manera:<br>
Importamos las librerías necesarias para la lectura de archivos y visualizaciones como matplotlib y seaborn principalmente. Posteriormente nos enfocamos en observar y entender las características usando gráficos, por ejemplo nos hicimos algunas preguntas como cuáles son los 3 juegos con mayor recomendación, los 5 juegos con mayor tiempo jugado, los 5 mejor desarrolladores, etc. con el fin de implícitamente ir contestando los endpoints de nuestra Api.


# <h1 align=center> **Desarrollo FAST API** </h1>
Utilizamos FastAPI para establecer nuestra API y configurar los puntos finales (endpoints) de manera efectiva. La siguiente fase implicó la implementación en Render, lo que nos va permitir poner los datos a disposición de clientes y personas o cualquier otra personas las cuales estén interesadas en acceder a nuestro trabajo. Los endpoints solicitados para este proyecto incluyen:

- `def developer(desarrollador: str)`: Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.

- `def userdata(User_id: str)`: Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.

- `def UserForGenre(genero: str)`: Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

- `def best_developer_year(año: int)`: Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos).

- `def developer_reviews_analysis(desarrolladora: str)`: Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.




# <h1 align=center> **Machine Learning** </h1>

- ***Sistema de recomendación de videojuegos***

Por último, llegamos a la fase de Modelamiento de Machine Learning. Tras un minucioso análisis exploratorio de datos, hemos adquirido una comprensión más profunda y clara, lo que nos capacita para avanzar con confianza y llevar a cabo predicciones mediante nuestro modelo entrenado. El proceso de modelamiento lo podemos visualizar [aquí](/Machine_learning2.ipynb).

Como primer paso importamos las librerías necesarias para poder desarrollar el modelo. Creamos una instancia con ayuda de la librería `surprise` a la cual tenemos que pasarle un user_id, item_id y un rating, que creamos previamente en una nueva columna con ayuda de análisis de sentimientos y recomendaciones. Después se divide con datos de test y entrenamiento para utilizar en este caso un algoritmo llamado Singular Value Descomposition (SVD) para el sistema de recomendación de juegos.

Una vez completado el modelamiento, lo exportamos ya entrenado y listo a un archivo `pkl` con ayuda de la libreria pickle, el archivo se encuentra en la carpeta data, con nombre [modelo2.pkl](/modelo2.pkl), esto con el fin de utilizarlo en las funciones para ahorrarnos tiempo y consumo al momento de consumirlo en la API.

La función nos devuelve lo siguiente:
- `def recomendacion_usuario(id de usuario)`: Ingresando el id de un usuario, deberíamos recibir una lista con 5 juegos recomendados para dicho usuario.


# <h1 align=center> **Entregables** </h1>

## Video

## Archivos del Repositorio
- [Etl-->Extracción, transformación y carga](/Etl.ipynb)
- [Eda-->Análisis exploratorio de datos](/Eda.ipynb)
- [Modelamiento Machine learning](/Machine_learning2.ipynb)

## Archivos para FAST API
- [Archivo main para FAST API](/main.py)
- [Funciones creadas para usarlos en los endpoints](/funciones.py)
- [Requerimientos FAST API ](/requirements.txt)
- [Carpeta data, que contiene los parquet limpios y el modelo entrenado pickle](/data)
- Para poder tener acceso a nuestra aplicación en Render, lo puedes obtener en este [link](https://proyecto-integrador-r58v.onrender.com/docs). Al abrirlo, favor de dar tiempo a que se construya el proceso en Render.

## Fuentes de datos
El repositorio no contiene los datos originales, a continuación coloco los links:

- [Dataset](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj): Carpeta con el archivo de origen en formato .json (steam_games.json).

- [Diccionario de datos](https://docs.google.com/spreadsheets/d/1-t9HLzLHIGXvliq56UE_gMaWBVTPfrlTf2D9uAtLGrk/edit#gid=0): Diccionario con algunas descripciones de las columnas disponibles en el dataset.

## Autor
- Laurence Salas Luis Alberto
- Email: llaurencesalas@gmail.com
- [GitHub](https://github.com/LuisLaurence23)
- [LinkedIn](https://www.linkedin.com/in/luis-alberto-laurence-salas-036a32187/)
