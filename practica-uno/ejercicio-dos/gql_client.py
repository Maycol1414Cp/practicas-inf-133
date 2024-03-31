import requests

url = 'http://localhost:8000/graphql'

#listar todas las plantas
query_lista ="""
{
    plantas{
        id
        nombre
        especie
        edad
        altura
        fruto
    }
}"""
response = requests.post(url, json={'query': query_lista})
print(response.text)

 #crear planta
print("crear planta")
query_crear ="""
    mutation {
        crearPlanta(
            nombre: "Pino",
            especie: "Pinus",
            edad: 10,
            altura: 5,
            fruto: true
        ) {
            planta {
                id
                nombre
                especie
                edad
                altura
                fruto
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.text)

#buscar las plantas por especie
print("buscar planta por especie")
query_especie ="""
{
    buscarEspecie(especie: "Pinus") {
        id
        nombre
        especie
        edad
        altura
        fruto
    }
}
"""
response = requests.post(url, json={'query': query_especie})
print(response.text)

#editar planta
print("editar planta")
query_editar ="""
    mutation {
        editarPlanta(
            id: 1,
            nombre: "Pino",
            especie: "Pinus",
            edad: 10,
            altura: 5,
            fruto: false
        ) {
            planta {
                id
                nombre
                especie
                edad
                altura
                fruto
            }
        }
    }
"""
response = requests.post(url, json={'query': query_editar})
print(response.text)

# plantas con frutos 
print("plantas con frutos")
query_frutos="""
    {
        frutos{
                id
                nombre
                especie
                edad
                altura
                fruto
            }
    }
"""
response = requests.post(url, json={'query': query_frutos})
print(response.text)


#eliminar planta
print("eliminar planta")
query_eliminar ="""
    mutation {
        eliminarPlanta(id: 1) {
            planta {
                id
                nombre
                especie
                edad
                altura
                fruto
            }
        }
    }
"""
response = requests.post(url, json={'query': query_eliminar})
print(response.text)
