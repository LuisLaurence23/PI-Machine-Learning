
from fastapi import FastAPI
from funciones import developer_reviews_analysis
#from funciones import UserForGenrep (Funcion 3 que usa el df_items)
from funciones import best_developer_yearp
from funciones import userdata2
from funciones import developer
from funciones import recomendar_peliculas


# Instanciamos FastAPI
app = FastAPI() 

#--------------------------------------------------------Función1---------------------------------------------------------------------------

#Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora

@app.get("/developer/{desarrollador}")       #Hacemos el endpoint
async def developer_def(desarrollador: str): #Definimos la función, el parámetro es el nombre del desarrollador
    result2 = developer(desarrollador)       #Llamamos a la función developer y le pasamos el parámetro
    return result2                           #Retornamos el resultado de la función




#--------------------------------------------------------Función2---------------------------------------------------------------------------

#Devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items

@app.get("/userdata/{user_id}")             #Hacemos el endpoint
async def userdata_handler(user_id: str):   #Definimos la función, el parámetro es el id del usuario
    try:                                    #Intentamos ejecutar la función
        result3 = userdata2(user_id)        #Llamamos a la función userdata2 y le pasamos el parámetro
        return result3                      #Retornamos el resultado de la función
    except Exception as e:                  #Si hay un error, lo capturamos
        return {"error": str(e)}            #Retornamos el error




#-------------------------------------------------------Función3-----------------------------------------------------------------------------
''' 
Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento
 
@app.get("/UserForGenre/{genero}")
async def UserForGenre(genero: str):
    try:
        result = UserForGenrep(genero)
        return result
    except Exception as e:
        return {"error": str(e)}
    '''
    
#-------------------------------------------------------Función4-----------------------------------------------------------------------------

'''Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.
   (reviews.recommend = True y comentarios positivos).'''

@app.get("/best_developer_year/{year}")             #Hacemos el endpoint
async def Best_developer_year(year: str):           #Definimos la función, el parámetro es el año
    try:                                            #Intentamos ejecutar la función
        year_int = int(year)                        #Convertimos el año a entero
        result2 = best_developer_yearp(year_int)    #Llamamos a la función best_developer_yearp y le pasamos el parámetro
        return result2                              #Retornamos el resultado de la función
    except Exception as e:                          #Si hay un error, lo capturamos
        return {"error": str(e)}                    #Retornamos el error




#-------------------------------------------------------Función5-------------------------------------------------------------------------------

'''Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros
   de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.'''

@app.get("/developer_reviews_analysis/{desarrollador}")  #Hacemos el endpoint
async def developer_def(desarrollador: str):             #Definimos la función, el parámetro es el nombre del desarrollador
    result2 = developer_reviews_analysis(desarrollador)  #Llamamos a la función developer_reviews_analysis y le pasamos el parámetro
    return result2                                       #Retornamos el resultado de la función



#-------------------------------------------------------Machine Learning------------------------------------------------------------------------

'''Ingresando el id de un usuario, recibimos una lista con 5 juegos recomendados para dicho usuario.'''
@app.get("/recomendacion_usuario/{id_usuario}")    #Hacemos el endpoint
async def recomendacion_usuario(id_usuario: str):  #
    result = recomendar_peliculas(id_usuario)
    return result
