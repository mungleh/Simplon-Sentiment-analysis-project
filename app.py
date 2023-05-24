# 1. Library imports
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
import pymysql
from TableStruct import bddinputs,  bddtest
from typing import List
from urllib.parse import urlparse
import os

from model import SentimentModel, ReviewSentiment

# 2. Create app and model objects
app = FastAPI(title= "Sentiment Model API")
model = SentimentModel()
# model = IrisModel()

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Récupérer l'URL de la base de données à partir des variables d'environnement
database_url = os.getenv("DATABASE_URL")

# Extraire les composants de l'URL de la base de données
url_components = urlparse(database_url)
db_host = url_components.hostname
db_user = url_components.username
db_password = url_components.password
db_name = url_components.path.strip("/")

# Configurer la connexion à la base de données MySQL
conn = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

#affichage pr test
@app.get("/")
async def get_items() -> List[bddtest]:
    # Effectuer des opérations sur la base de données
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM test LIMIT 5")
        results = cursor.fetchall()

    # Convertir les résultats en une liste d'objets Test a refacto par la suite
    items = []
    for row in results:
        data_dict = {
            "id": row[0],
            "review" : row[1],
            "rating" : row[2],
        }

        data_user = bddtest(**data_dict)
        items.append(data_user)

    # Retourner les résultats de l'API
    return items

#-----------------------------------------------------------------------API app--------------------------------------------------------------
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

 #------------------------------------------------------------------------API BDD---------------------------------------------------------------------------
@app.post("/add")
async def create_item(item: bddinputs):
    # Effectuer des opérations sur la base de données
    with conn.cursor() as cursor:
        query = "INSERT INTO inputs (title, feature, prediction) " \
                 "VALUES (%s, %s, %s)"
        values = (item.title,item.feature, item.prediction)
        cursor.execute(query, values)
        conn.commit()

    return {"message": "Item created successfully"}

@app.post("/del")
async def delete_item():
    # Effectuer des opérations sur la base de données
    with conn.cursor() as cursor:
        query = "DELETE FROM inputs"
        cursor.execute(query)
        conn.commit()

    return {"message": "Items deleted successfully"}

# # 4. Run the API with uvicorn
# #    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
