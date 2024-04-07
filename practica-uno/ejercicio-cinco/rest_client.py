import requests

# Consulta a un servidor RESTful
url = "http://localhost:8000"

# POST para agregar un nuevo animal
ruta_post = url + "/animales"
nuevo_animal = {
    "nombre": "Maria",
    "especie": "Leon",
    "genero": "Hembra",
    "edad": 4,
    "peso": 150
}

print("Agregando un nuevo animal:")
post_response = requests.post(url=ruta_post, json=nuevo_animal)
print(post_response.text)
print("\n")

# GET para obtener todos los animales
ruta_get_all = url + "/animales"
print("Obteniendo todos los animales:")
get_all_response = requests.get(url=ruta_get_all)
print(get_all_response.text)
print("\n")

# GET para filtrar animales por especie
especie = "Leon"
ruta_get_by_species = f"{url}/animales?especie={especie}"
print(f"Obteniendo animales de la especie '{especie}':")
get_by_species_response = requests.get(url=ruta_get_by_species)
print(get_by_species_response.text)
print("\n")

# GET para filtrar animales por género
genero = "Macho"
ruta_get_by_gender = f"{url}/animales?genero={genero}"
print(f"Obteniendo animales del género '{genero}':")
get_by_gender_response = requests.get(url=ruta_get_by_gender)
print(get_by_gender_response.text)
print("\n")

# PUT para actualizar la información de un animal (por su ID)
id_a_actualizar = 1  # ID del animal a actualizar
ruta_put = f"{url}/animales/{id_a_actualizar}"
datos_actualizados = {
    "edad": 6,
    "peso": 190
}
print(f"Actualizando información del animal con ID {id_a_actualizar}:")
put_response = requests.put(url=ruta_put, json=datos_actualizados)
print(put_response.text)
print("\n")

# DELETE para eliminar un animal (por su ID)
id_a_eliminar = 2  # ID del animal a eliminar
ruta_delete = f"{url}/animales/{id_a_eliminar}"
print(f"Eliminando el animal con ID {id_a_eliminar}:")
delete_response = requests.delete(url=ruta_delete)
print(delete_response.text)
print("\n")
