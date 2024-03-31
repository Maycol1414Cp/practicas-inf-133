from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from graphene import ObjectType, Int, String, Boolean, List, Schema,Field, Mutation

class Planta(ObjectType):
    id = Int() 
    nombre = String() # nombre popular
    especie = String() # nombre cientifico. 
    edad =  Int()  # en meses
    altura = Int() # en cm
    fruto = Boolean()

class Query(ObjectType):
    plantas = List(Planta)
    buscar_especie = Field(List(Planta), especie=String())
    #listar plantas con frutos
    frutos = Field(List(Planta))


    def resolve_plantas(self, info):
        return plantas
    
    def resolve_buscar_especie(self, info, especie):
        #retornar planta con especie
        for planta in plantas:
            if planta.especie == especie:
                yield planta
        return None
    def resolve_frutos(self, info):
        #retornar lista de plantas con frutos
        for planta in plantas:
            if planta.fruto:
                yield planta
 
class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        fruto = Boolean()
    
    planta = Field(Planta)
    
    def mutate(self, info, nombre, especie, edad, altura, fruto):
        nueva_planta = Planta(
            id=len(plantas) + 1,
            nombre=nombre,
            especie=especie,
            edad=edad,
            altura=altura,
            fruto=fruto
        )
        plantas.append(nueva_planta)

        return CrearPlanta(planta=nueva_planta)
    
class EditarPlanta(Mutation):
    class Arguments:
        id = Int()
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        fruto = Boolean()
    
    planta = Field(Planta)
    
    def mutate(self, info, id, nombre, especie, edad, altura, fruto):
        for planta in plantas:
            if planta.id == id:
                planta.nombre = nombre
                planta.especie = especie
                planta.edad = edad
                planta.altura = altura
                planta.fruto = fruto
                return EditarPlanta(planta=planta)
        return None
    

class EliminarPlanta(Mutation):
    class Arguments:
        id = Int()
    
    planta = Field(Planta)
    
    def mutate(self, info, id):
        for planta in plantas:
            if planta.id == id:
                plantas.remove(planta)
                return EliminarPlanta(planta=planta)
        return None
    
class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    editar_planta = EditarPlanta.Field()
    eliminar_planta = EliminarPlanta.Field()

plantas = [
    Planta(
        id=1,
        nombre='Pino',
        especie='Pinus',
        edad=24,
        altura=120,
        fruto=False
    ),
    Planta(
        id=2,
        nombre='Manzano',
        especie='Malus domestica',
        edad=36,
        altura=150,
        fruto=True
    )
]

schema = Schema(query=Query, mutation=Mutations)

class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()