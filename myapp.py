from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pymongo import ASCENDING


app = FastAPI()

# Conexión a la base de datos MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["supermamidb"]
collection = db["smProducts"]

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    # Buscar los items en la colección que coincidan con el ID
    items = collection.find({"prod_id": item_id}).sort("date", ASCENDING)
    
    # Crear una lista para almacenar los resultados
    result = []
    
    # Iterar sobre los resultados y agregarlos a la lista
    for item in items:
        # Convertir el ObjectId a una cadena antes de agregarlo a la lista
        item['_id'] = str(item['_id'])
        result.append(item)
    
    # Verificar si se encontraron elementos
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Item not found")