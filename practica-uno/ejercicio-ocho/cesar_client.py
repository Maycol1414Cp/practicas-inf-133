import requests
import json

def crear_mensaje(contenido):
    print(f"Creando mensaje con contenido: {contenido}")
    data = {"contenido": contenido}
    response = requests.post("http://localhost:8000/mensajes", data=json.dumps(data))
    print("Respuesta del servidor:")
    print(response.json())

def listar_mensajes():
    print("Listando todos los mensajes")
    response = requests.get("http://localhost:8000/mensajes")
    print("Respuesta del servidor:")
    print(response.json())

def buscar_mensaje(id):
    print(f"Buscando mensaje con ID: {id}")
    response = requests.get(f"http://localhost:8000/mensajes/{id}")
    print("Respuesta del servidor:")
    print(response.json())

def actualizar_mensaje(id, contenido):
    print(f"Actualizando mensaje con ID: {id}, nuevo contenido: {contenido}")
    data = {"contenido": contenido}
    response = requests.put(f"http://localhost:8000/mensajes/{id}", data=json.dumps(data))
    print("Respuesta del servidor:")
    print(response.json())

def eliminar_mensaje(id):
    print(f"Eliminando mensaje con ID: {id}")
    response = requests.delete(f"http://localhost:8000/mensajes/{id}")
    print("Respuesta del servidor:")
    print(response.json())

if __name__ == "__main__":
    crear_mensaje("hola")
    listar_mensajes()
    buscar_mensaje(1)
    actualizar_mensaje(1, "adios")
    eliminar_mensaje(1)