import pandas as pd


df_games = pd.read_parquet('./data/steam_games2.parquet')
#df_items = pd.read_parquet('./data/user_items.parquet')
df_reviews = pd.read_parquet('./data/user_reviews.parquet')


#UserForGenrep(genero)
#df_marge_item = pd.merge(df_games , df_items,on="item_id" )
#df_nuevo = df_marge_item.drop(columns=["item_id","app_name","price","developer","items_count","item_name","playtime_2weeks"])

#best_developer_yearp(year)
merged_df = pd.merge(df_reviews, df_games, on='item_id')
merged_df = merged_df.rename(columns={'posted_year': 'year'})
#merged_dff=merged_df[['year','recommend','sentiment_analysis','developer','app_name']]


#userdata(user_id)
#merged_reviews_games = df_reviews.merge(df_games[['item_id', 'price']])
#merged_reviews_games.drop(columns=['helpful','posted_year',"sentiment_analysis"], inplace=True)
#merged_reviews_games['item_id'] = merged_reviews_games['item_id'].astype('int32')


#def developer(desarrollador:str)
#df_marge_desarrollador_final= df_marge_item[["item_id", "price","developer","release_year"]]

#developer_reviews_analysis(desarrollador)
analisis_f= merged_df[['developer','sentiment_analysis']]
'''
def UserForGenrep(genero):
    df_genre = df_nuevo[df_nuevo[genero] == 1] #llamo el genero
    usur_mas_horas = df_genre.groupby("user_id")["playtime_forever"].sum().idxmax() #usuario con más horas de juego en el genero
    filtro_usur = df_genre[df_genre["user_id"] == usur_mas_horas] #filtramos por el usuario con mas horas jugadas
    horas_jugXaño = filtro_usur.groupby("release_year")["playtime_forever"].sum() #horas jugadas por año 

    registro = horas_jugXaño.to_dict() #paso las horas por año en diccionario
    #del registro[0] #elimino el registro 0 que no me sirve
    Horas_por_año = {}
    for clave, valor in registro.items():
        clave_formateada = f'Año: {int(clave)}'
        valor_formateado = int(valor)
        Horas_por_año[clave_formateada] = valor_formateado

    return {"Usuario con más horas jugadas": usur_mas_horas, "Horas jugadas por año": Horas_por_año}


def best_developer_yearp(year):
    df_year = merged_dff[merged_dff['year'] == year]
    df_count = df_year.loc[(df_year['recommend'] == True) & (df_year['sentiment_analysis'] == 2)].groupby('developer')['app_name'].count().reset_index()


    top_desarrolladores = df_count.sort_values('app_name', ascending=False).head(3)['developer'].tolist()
    
    # Crear la lista de diccionarios
    resultados = {f'Puesto {i+1}': desarrollador for i, desarrollador in enumerate(top_desarrolladores)}
    
    return resultados





def userdata2(user_id):
    # Filtrar los datos para el usuario especificado
    user_data = merged_reviews_games[merged_reviews_games['user_id'] == user_id]

    user_items = df_items[df_items['user_id'] == user_id]

    # Calcular la cantidad de dinero gastado por el usuario
    dinero_gastado = user_data['price'].sum()

    # Calcular el porcentaje de recomendación en base a reviews.recommend
    recomendacion = (user_data['recommend'] == True).sum()
    porcentaje_recomendacion = recomendacion / len(user_data) * 100

    # Calcular la cantidad de items
    cantidad_de_items = user_items['item_id'].nunique()

    # Crear un diccionario con los resultados
    resultados = {
        'Cantidad de dinero gastado': dinero_gastado,
        'Porcentaje de recomendación': porcentaje_recomendacion,
        'Cantidad de items': cantidad_de_items
    }

    return resultados
    
    
''' 

def developer(desarrollador):
    df_developer = df_games[df_games["developer"] == desarrollador]
    items_year = df_developer.groupby("release_year")["item_id"].count()

    # Se filtra el df del desarrolladorpara aquellos juegos gratuitos (precio cero):
    df_dev_free = df_developer[df_developer["price"] == 0] 

    # Se obtiene la cantidad de items gratuitos por años
    free_items = df_dev_free.groupby("release_year")["price"].count() #cantidad de gratis por año 

    # Se calcula el porcentaje de contenido gratuito por año
    free_proportion = round((free_items / items_year) * 100, 2)

    # Se asigna nombre a las series para poder unirlas en un dataframe:
    items_year.name = "Cantidad de Items"
    free_proportion.name = "Contenido Free"

    df1 = pd.merge(items_year, free_proportion, on = "release_year").reset_index()
    df1 = df1.fillna(0)

    df1 = df1.rename(columns={"release_year" : "Año"})

    # Se da formato a la columna de contenido free:
    df1["Contenido Free"] = df1["Contenido Free"].apply(lambda x: f"{x}%")

    # Se convierte el df en diccionario
    diccionario = df1.to_dict(orient="records")
    del df_developer, items_year, df_dev_free, free_items, free_proportion, df1
    return diccionario




def developer_reviews_analysis(desarrolladora):
    desarrolladores=analisis_f[analisis_f['developer'] == desarrolladora]
    df_positivas = desarrolladores[desarrolladores['sentiment_analysis'] == 2]
    df_negativas = desarrolladores[desarrolladores['sentiment_analysis'] == 0]
    
    cantidad_positivas = len(df_positivas)
    cantidad_negativas = len(df_negativas)

    resultados = {
        desarrolladora: {
            'positivas': cantidad_positivas,
            'negativas': cantidad_negativas
        }
    }
    del desarrolladores, df_positivas, df_negativas, cantidad_positivas, cantidad_negativas
    return resultados