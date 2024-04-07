import requests
import json

BASE_URL = "http://localhost:8000"

def create_animal(tipo, data):
    response = requests.post(f"{BASE_URL}/animales", json={"tipo": tipo, "data": data})
    if response.status_code == 201:
        print("Animal creado con éxito:")
        print(json.dumps(response.json(), indent=4))
    else:
        print("Error al crear el animal:")
        print(response.text)

def list_all_animals():
    response = requests.get(f"{BASE_URL}/animales")
    if response.status_code == 200:
        print("Todos los animales:")
        print(json.dumps(response.json(), indent=4))
    else:
        print("Error al listar los animales:")
        print(response.text)

def search_animals_by_species(especie):
    response = requests.get(f"{BASE_URL}/animales/especie", params={"especie": especie})
    if response.status_code == 200:
        print(f"Animales de la especie {especie}:")
        print(json.dumps(response.json(), indent=4))
    else:
        print("Error al buscar animales por especie:")
        print(response.text)

def update_animal(id, data):
    response = requests.put(f"{BASE_URL}/animales/{id}", json=data)
    if response.status_code == 200:
        print("Información del animal actualizada con éxito:")
        print(json.dumps(response.json(), indent=4))
    else:
        print("Error al actualizar la información del animal:")
        print(response.text)

def delete_animal(id):
    response = requests.delete(f"{BASE_URL}/animales/{id}")
    if response.status_code == 200:
        print("Animal eliminado con éxito.")
    else:
        print("Error al eliminar el animal:")
        print(response.text)

if __name__ == "__main__":
    # Crear un animal
    create_animal("Mamifero", {"id": "1", "nombre": "Lion", "especie": "Felino", "genero": "Macho", "edad": 5, "peso": 200, "tipo_pelo": "Corto"})

    # Listar todos los animales
    list_all_animals()

    # Buscar animales por especie
    search_animals_by_species("Felino")

    # Actualizar la información de un animal
    update_animal("1", {"edad": 6})

    # Eliminar un animal
    delete_animal("1")