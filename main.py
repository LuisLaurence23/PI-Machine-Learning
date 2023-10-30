
from fastapi import FastAPI
from funciones import developer_reviews_analysis
#from funciones import UserForGenrep
from funciones import best_developer_yearp
from funciones import userdata2
from funciones import developer
from funciones import recomendar_peliculas


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

#1
@app.get("/developer/{desarrollador}")
async def developer_def(desarrollador: str):
    result2 = developer(desarrollador)
    return result2 


#2
@app.get("/userdata/{user_id}")
async def userdata_handler(user_id: str):
    try:
        result3 = userdata2(user_id)
        return result3
    except Exception as e:
        return {"error": str(e)}


#3
''' 
@app.get("/UserForGenre/{genero}")
async def UserForGenre(genero: str):
    try:
        result = UserForGenrep(genero)
        return result
    except Exception as e:
        return {"error": str(e)}
    '''
    
#4
@app.get("/best_developer_year/{year}")
async def Best_developer_year(year: str):
    try:
        year_int = int(year)  # Convertir el año a un entero
        result2 = best_developer_yearp(year_int)
        return result2
    except Exception as e:
        return {"error": str(e)}


#5
@app.get("/developer_reviews_analysis/{desarrollador}")
async def developer_def(desarrollador: str):
    result2 = developer_reviews_analysis(desarrollador)
    return result2 


#Machine Learning id_usuario
@app.get("/recomendacion_usuario/{id_usuario}")
async def recomendacion_usuario(id_usuario: str):
    result = recomendar_peliculas(id_usuario)
    return result
