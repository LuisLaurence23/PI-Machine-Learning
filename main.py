
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from funciones import UserForGenrep,best_developer_yearp,userdata2,developer,developer_reviews_analysis

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/UserForGenre/{genero}")
async def UserForGenre(genero: str):
    try:
        result = UserForGenrep(genero)
        return result
    except Exception as e:
        return {"error": str(e)}
    
    
@app.get("/best_developer_year/{year}")
async def Best_developer_year(year: str):
    try:
        year_int = int(year)  # Convertir el año a un entero
        result2 = best_developer_yearp(year_int)
        return result2
    except Exception as e:
        return {"error": str(e)}


@app.get("/userdata/{user_id}")
async def userdata_handler(user_id: str):
    try:
        result3 = userdata2(user_id)
        return result3
    except Exception as e:
        return {"error": str(e)}



@app.get("/developer/{desarrollador}")
async def developer_def(desarrollador: str):
    result2 = developer(desarrollador)
    return result2 


@app.get("/developer_reviews/{desarrolladora}")
async def developer_def(desarrolladora: str):
    result2 = developer_reviews_analysis(desarrolladora)
    return result2 
