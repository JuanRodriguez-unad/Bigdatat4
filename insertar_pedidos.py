from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import os


try:
    # Conectar a MongoDB
    client = MongoClient("mongodb+srv://juanpa56336:[////////////]@tiendaonline.xpoqesf.mongodb.net/?retryWrites=true&w=majority")
    # Crear o seleccionar la base de datos y colección
    db = client["tiendaOnline"]
    pedidos = db["pedidos"]

    # Limpiar datos previos si existen
    pedidos.delete_many({})

    # Insertar 100 documentos
    documentos = []
    for i in range(1, 101):
        documentos.append({
            "cliente": f"Cliente {i}",
            "productos": [
                {"nombre": "Producto A", "cantidad": random.randint(1, 3), "precio": 10000 + i * 100},
                {"nombre": "Producto B", "cantidad": 2, "precio": 15000}
            ],
            "fecha": datetime.now() - timedelta(days=random.randint(0, 30)),  
            "estado": "Enviado" if i % 2 == 0 else "Pendiente"
        })

    pedidos.insert_many(documentos)
    print("Se insertaron 100 pedidos correctamente.")

except Exception as e:
    print(f"Error al conectar o insertar datos en MongoDB: {e}")