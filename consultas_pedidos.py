from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import os

# Reemplaza con tu URI de Atlas
uri = "mongodb+srv://juanpa56336:[/////////]@tiendaonline.xpoqesf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["tiendaOnline"]
pedidos = db["pedidos"]

print("Conectado a MongoDB\n")

# 1. Leer 5 documentos
print("Primeros 5 pedidos:")
for pedido in pedidos.find().limit(5):
    print(pedido)

# 2. Insertar nuevo pedido
nuevo = {
    "cliente": "Cliente Extra",
    "productos": [{"nombre": "Tablet", "cantidad": 1, "precio": 800000}],
    "fecha": datetime.now(),
    "estado": "Pendiente"
}
pedidos.insert_one(nuevo)
print("\nPedido adicional insertado.")

# 3. Actualizar estado de Cliente 5
pedidos.update_one(
    {"cliente": "Cliente 5"},
    {"$set": {"estado": "Cancelado"}}
)
print("Estado de Cliente 5 actualizado a 'Cancelado'.")

# 4. Eliminar Cliente 3
pedidos.delete_one({"cliente": "Cliente 3"})
print("Cliente 3 eliminado.")

# 5. Filtrar por estado
print("\nPedidos con estado 'Pendiente':")
for pedido in pedidos.find({"estado": "Pendiente"}).limit(3):
    print(pedido)

# 6. Pedidos después del 10 de mayo
print("\nPedidos después del 10 de mayo:")
for pedido in pedidos.find({"fecha": {"$gt": datetime(2025, 5, 10)}}).limit(3):
    print(pedido)

# 7. Productos con precio > 50.000
print("\nProductos con precio mayor a 50,000:")
for pedido in pedidos.find({"productos.precio": {"$gt": 50000}}).limit(3):
    print(pedido)

# 8. Contar total de pedidos
total = pedidos.count_documents({})
print(f"\nTotal de pedidos: {total}")

# 9. Sumar ingresos por pedidos
pipeline = [
    {"$unwind": "$productos"},
    {"$group": {
        "_id": None,
        "totalIngresos": {"$sum": {"$multiply": ["$productos.precio", "$productos.cantidad"]}}
    }}
]
print("\nTotal de ingresos:")
for r in pedidos.aggregate(pipeline):
    print(r)

# 10. Promedio de productos por pedido
pipeline = [
    {"$project": {"cantidad": {"$size": "$productos"}}},
    {"$group": {"_id": None, "promedio": {"$avg": "$cantidad"}}}
]
print("\nPromedio de productos por pedido:")
for r in pedidos.aggregate(pipeline):
    print(r)
