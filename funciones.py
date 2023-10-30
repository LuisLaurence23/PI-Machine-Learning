import pandas as pd
import pickle



#Lectura de archivos
df_games = pd.read_parquet('./data/steam_games22.parquet')
df_reviews = pd.read_parquet('./data/user_reviews.parquet')
#df_items = pd.read_parquet('./data/user_items.parquet')


#Dataframes usados para el punto 1
#df_games = pd.read_parquet('./data/steam_games22.parquet')


#Dataframes usados para el punto 2
merged_reviews_games = df_reviews.merge(df_games[['item_id', 'price']])
merged_reviews_games.drop(columns=['helpful','posted_year',"sentiment_analysis"], inplace=True)
merged_reviews_games['item_id'] = merged_reviews_games['item_id'].astype('int32')


#Dataframes usados para el punto 3
#df_marge_item = pd.merge(df_games , df_items,on="item_id" )
#df_nuevo = df_marge_item.drop(columns=["item_id","app_name","price","developer","items_count","item_name","playtime_2weeks"])


#Dataframes usados para el punto 4
merged_df = pd.merge(df_reviews, df_games, on='item_id')
merged_df = merged_df.rename(columns={'posted_year': 'year'})
merged_dff=merged_df[['year','recommend','sentiment_analysis','developer','app_name']]


#Dataframes usados para el punto 5
analisis_f= merged_df[['developer','sentiment_analysis']]


#Dataframes usados para Machine Learning
df_machine= pd.read_parquet('./data/df_ML2.parquet')



#----------------------------------------------------------------Función1----------------------------------------------------------------

def developer(desarrollador):
    
    #Filtramos el df de juegos con el desarrollador especificado
    df_developer = df_games[df_games["developer"] == desarrollador]
    
    #Se obtiene la cantidad de items por año de lanzamiento
    items_year = df_developer.groupby("release_year")["item_id"].count()

    #Filtramos los juegos gratuitos (price = 0)
    df_dev_free = df_developer[df_developer["price"] == 0] 

    #Cantidad de juegos gratuitos por años
    free_items = df_dev_free.groupby("release_year")["price"].count() 

    #Porcentaje de contenido gratuito por año
    free_proportion = round((free_items / items_year) * 100, 2)

    #Creamos el nombre a las series para unirlas en un df:
    items_year.name = "Cantidad de Items"
    free_proportion.name = "Contenido Free"

    
    df1 = pd.merge(items_year, free_proportion, on = "release_year").reset_index() #se unen las series en un df
    df1 = df1.fillna(0)                                                            #llenamos NaN con 0
    df1 = df1.rename(columns={"release_year" : "Año"})                             #renombre de columna release_year por Año


    #Agregamos el simbolo de porcentaje
    df1["Contenido Free"] = df1["Contenido Free"].apply(lambda x: f"{x}%") 

    #orient="records" para que el diccionario sea de la forma: [{columna -> valor}]
    diccionario = df1.to_dict(orient="records")
    
    #Se eliminan los df que ya no se usan en la funcion
    del df_developer, items_year, df_dev_free, free_items, free_proportion, df1
    
    return diccionario

#----------------------------------------------------------------Función2----------------------------------------------------------------

def userdata2(user_id):
    #Filtramos los datos para el usuario especificado
    user_data = merged_reviews_games[merged_reviews_games['user_id'] == user_id]

    #Suma de dinero gastado por el usuario
    dinero_gastado = user_data['price'].sum()

    #Suma de recomendaciones positivas por el usuario (recommend = True)
    recomendacion = (user_data['recommend'] == True).sum()
    porcentaje_recomendacion = recomendacion / len(user_data) * 100

    #Cantidad de items
    cantidad_de_items = user_data['item_id'].nunique()#

    #Diccionario con los resultados
    resultados = {
        'Cantidad de dinero gastado': dinero_gastado,
        'Porcentaje de recomendación': porcentaje_recomendacion,
        'Cantidad de items': cantidad_de_items
    }
    
    #Se eliminan los df que ya no se usan en la funcion
    del user_data, dinero_gastado, recomendacion, porcentaje_recomendacion, cantidad_de_items
    
    return resultados


#----------------------------------------------------------------Función3----------------------------------------------------------------

#En esta función en especifico, tuve algunos problemas al realizar el deploy en render por cuestiones de memoria. El df_items tiene
#aproximadamente 5 millones de registros, por lo que al momento de realizar el deploy, el servidor mandaba un error por memoria.
#Por lo tanto la dejo comentada para no tener ese problema. Solamente me da el resultado de manera local en la API.

''' 
def UserForGenrep(genero):

    #filtramos donde el genero sea 1 (True)
    df_genre = df_nuevo[df_nuevo[genero] == 1] 
    
    #idxmax() devuelve el indice del valor maximo del usuario con mas horas jugadas en el género
    usur_mas_horas = df_genre.groupby("user_id")["playtime_forever"].sum().idxmax() 
    
    #Filtramos por el usuario con mas horas jugadas
    filtro_usur = df_genre[df_genre["user_id"] == usur_mas_horas]
    
    #Agrupamos por año y sumamos las horas jugadas
    horas_juego_x_año = filtro_usur.groupby("release_year")["playtime_forever"].sum()

    #Pasamos a diccionario
    registro = horas_juego_x_año.to_dict()
    
    #Diccionario con los resultados
    Horas_por_año = {}
    for clave, valor in registro.items():
        clave_formateada = f'Año: {int(clave)}'
        valor_formateado = int(valor)
        Horas_por_año[clave_formateada] = valor_formateado

    return {"Usuario con más horas jugadas": usur_mas_horas, "Horas jugadas por año": Horas_por_año}
'''

#----------------------------------------------------------------Función4----------------------------------------------------------------

def best_developer_yearp(year):
    #Filtramos por año especificado en la función
    df_year = merged_dff[merged_dff['year'] == year]
    
    #Aplicamos un filtro para obtener los juegos recomendados y con sentimiento positivo, agrupamos por desarrollador y contamos la cantidad de juegos
    df_count = df_year.loc[(df_year['recommend'] == True) & (df_year['sentiment_analysis'] == 2)].groupby('developer')['app_name'].count().reset_index()
    
    #Ordenamos de mayor a menor y tomamos los 3 primeros y los guardamos en una lista
    top_desarrolladores = df_count.sort_values('app_name', ascending=False).head(3)['developer'].tolist()
    
    #Creamos lista de diccionarios para la respuesta
    resultados = {f'Puesto {i+1}': desarrollador for i, desarrollador in enumerate(top_desarrolladores)}
    
    return resultados



#----------------------------------------------------------------Función5----------------------------------------------------------------

def developer_reviews_analysis(desarrolladora):
    #Filtramos por desarrolladora especificada en la función
    desarrolladores = analisis_f[analisis_f['developer'] == desarrolladora]
    
    #Filtramos por sentimiento positivo(2) y negativo(0)
    df_positivas    = desarrolladores[desarrolladores['sentiment_analysis'] == 2]
    df_negativas    = desarrolladores[desarrolladores['sentiment_analysis'] == 0]
    
    #Obtenemos la cantidad de reviews positivas y negativas
    cantidad_positivas = len(df_positivas)
    cantidad_negativas = len(df_negativas)

    #Creamos un diccionario con los resultados
    resultados = {
        desarrolladora: {
            'positivas': cantidad_positivas,
            'negativas': cantidad_negativas
        }
    }
    
    #Se eliminan los df que ya no se usan en la funcion
    del desarrolladores, df_positivas, df_negativas, cantidad_positivas, cantidad_negativas
    
    #Retornamos el diccionario
    return resultados




#----------------------------------------------------------------Machine Learning---------------------------------------------------------


#Traemos el modelo ya entrenado con ayuda del modulo pickle
with open ('./data/modelo2.pkl', 'rb') as file:
    modelo=pickle.load(file)

def recomendar_peliculas(user_id):
    
    #Creamos una lista vacía para guardar los juegos recomendados, y un diccionario para guardar el
    #retorno final con clave-valor
    
    listado=[]
    diccionario = {}
    
    #Juegos ya valorados por el usuario que se pasa como parámetro 
    juegos_valorados = df_machine[df_machine['user_id'] == user_id]['app_name'].unique()

    #Juegos disponibles
    todos_los_juegos = df_machine['app_name'].unique()

    #Juegos no valorados por el usuario (para no recomendarle los mismos)
    juegos_no_valorados = list(set(todos_los_juegos) - set(juegos_valorados))

    #Hacemos predict para los juegos no valorados por el usuario
    predicciones = [modelo.predict(user_id, juego) for juego in juegos_no_valorados]

    #Ordenamos las predicciones respecto a la valoración y tomamos los 5 mejos juegos recomendados
    recomendaciones = sorted(predicciones, key=lambda x: x.est, reverse=True)[:5]


    #Guardamos los juegos recomendados en una lista 
    for recomendacion in recomendaciones:
        listado.append(recomendacion.iid)
     
    #Creamos un diccionario con clave-valor para retornar los juegos recomendados   
    for i, juego in enumerate(listado, start=1):
        opcion = f"opcion{i}"
        diccionario[opcion] = juego

    #Si el usuario no existe, se muestra el mensaje "El usuario no existe"
    if user_id not in df_machine['user_id'].unique():
        return "El usuario no existe"
    else:
        return diccionario




