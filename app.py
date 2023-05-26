# 1. Library imports
import uvicorn
from fastapi import FastAPI
import pymysql
from TableStruct import bddinputs
from typing import List
from urllib.parse import urlparse
import os

from model import SentimentModel, ReviewSentiment

# 2. Create app and model objects
app = FastAPI(title= "Sentiment Model API")
model = SentimentModel()
# model = IrisModel()

#conneries
def connect():
    # Récupérer l'URL de la base de données à partir des variables d'environnement
    database_url = os.getenv("DATABASE_URL")

    # Extraire les composants de l'URL de la base de données
    url_components = urlparse(database_url)
    db_host = url_components.hostname
    db_user = url_components.username
    db_password = url_components.password
    db_name = url_components.path.strip('/')

    # Configurer la connexion à la base de données MySQL
    conn = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return conn

#-------------------------------------------------API BDD GET--------------------------------------------
#affichage pr test
@app.get("/")
async def get_items() -> List[bddinputs]:
    # Effectuer des opérations sur la base de données
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM inputs")
        results = cursor.fetchall()

    # Convertir les résultats en une liste d'objets Test a refacto par la suite
    items = []
    for row in results:
        data_dict = {
            "input": row[0],
            "prediction" : row[1],
            "probability" : row[2],
            "istrue" : row[3],
        }

        data_user = bddinputs(**data_dict)
        items.append(data_user)

    # Retourner les résultats de l'API
    return items

#
@app.get("/data")
async def get_items(col, filter) -> List[bddinputs]:
    # Effectuer des opérations sur la base de données
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM inputs WHERE {col} = {filter}")
        results = cursor.fetchall()

    # Convertir les résultats en une liste d'objets Test a refacto par la suite
    items = []
    for row in results:
        data_dict = {
            "input": row[0],
            "prediction" : row[1],
            "probability" : row[2],
            "istrue" : row[3],
        }

        data_user = bddinputs(**data_dict)
        items.append(data_user)

    # Retourner les résultats de l'API
    return items

#------------------------------------------------------API app----------------------------------------
@app.post('/test_predict')

def predict_sentiment(review: ReviewSentiment):
    data = review.dict()
    prediction, probability = model.predict_sentiment(
        data['review']
    )
    return {
        'prediction': prediction,
        'probability': probability
    }
@app.get('/predict')

def predict_sentiment(review: ReviewSentiment):
    data = review.dict()
    prediction, probability = model.predict_sentiment(
        data['review']
    )
    return {
        'prediction': prediction,
        'probability': probability
    }

 #----------------------------------------------API BDD POST-----------------------------------------------------
@app.post("/add")
async def create_item(item: bddinputs):
    # Effectuer des opérations sur la base de données
    conn = connect()
    with conn.cursor() as cursor:
        query = "INSERT INTO inputs (input, prediction, probability, istrue) " \
                 "VALUES (%s, %s, %s, %s)"
        values = (item.input, item.prediction, item.probability, item.istrue)
        cursor.execute(query, values)
        conn.commit()

    return {"message": "Item created successfully"}

@app.post("/del")
async def delete_item():
    # Effectuer des opérations sur la base de données
    conn = connect()
    with conn.cursor() as cursor:
        query = "DELETE FROM inputs"
        cursor.execute(query)
        conn.commit()

    return {"message": "Items deleted successfully"}

# # 4. Run the API with uvicorn
# #    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
