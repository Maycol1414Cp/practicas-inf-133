from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

# Lista de animales (datos de ejemplo)
animales = []

class AnimalFactory:
    @staticmethod
    def create_animal(tipo, **kwargs):
        if tipo == "Mamifero":
            return Mamifero(**kwargs)
        elif tipo == "Ave":
            return Ave(**kwargs)
        elif tipo == "Reptil":
            return Reptil(**kwargs)
        elif tipo == "Anfibio":
            return Anfibio(**kwargs)
        elif tipo == "Pez":
            return Pez(**kwargs)
        else:
            return None

class Animal:
    def __init__(self, id, nombre, especie, genero, edad, peso):
        self.id = id
        self.nombre = nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "especie": self.especie,
            "genero": self.genero,
            "edad": self.edad,
            "peso": self.peso
        }

class Mamifero(Animal):
    def __init__(self, tipo_pelo, **kwargs):
        super().__init__(**kwargs)
        self.tipo_pelo = tipo_pelo

# Implementar clases para otros tipos de animales: Ave, Reptil, Anfibio, Pez

class AnimalService:
    @staticmethod
    def add_animal(animal):
        animales.append(animal)
        return animal

    @staticmethod
    def get_all_animals():
        return [animal.to_dict() for animal in animales]

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            HTTPResponseHandler.handle_response(self, 200, AnimalService.get_all_animals())
        elif parsed_path.path == "/animales/especie":
            especie = query_params.get("especie", [None])[0]
            if especie:
                animales_filtrados = [animal.to_dict() for animal in animales if animal.especie == especie]
                HTTPResponseHandler.handle_response(self, 200, animales_filtrados)
            else:
                HTTPResponseHandler.handle_response(self, 400, {"error": "Especie no proporcionada"})
        elif parsed_path.path.startswith("/animales/"):
            id = parsed_path.path.split("/")[-1]
            animal = next((animal for animal in animales if animal.id == id), None)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, animal.to_dict())
            else:
                HTTPResponseHandler.handle_response(self, 404, {"error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Ruta no encontrada"})

    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            tipo = data.get("tipo")
            animal_data = data.get("data")
            if not tipo:
                HTTPResponseHandler.handle_response(self, 400, {"error": "Tipo de animal no proporcionado"})
                return
            animal = AnimalFactory.create_animal(tipo, **animal_data)
            if animal:
                added_animal = AnimalService.add_animal(animal)
                HTTPResponseHandler.handle_response(self, 201, added_animal.to_dict())
            else:
                HTTPResponseHandler.handle_response(self, 400, {"error": "Tipo de animal no válido"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Ruta no encontrada"})

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith("/animales/"):
            id = parsed_path.path.split("/")[-1]
            animal = next((animal for animal in animales if animal.id == id), None)
            if animal:
                data = self.read_data()
                for key, value in data.items():
                    setattr(animal, key, value)
                HTTPResponseHandler.handle_response(self, 200, animal.to_dict())
            else:
                HTTPResponseHandler.handle_response(self, 404, {"error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Ruta no encontrada"})

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith("/animales/"):
            id = parsed_path.path.split("/")[-1]
            animal = next((animal for animal in animales if animal.id == id), None)
            if animal:
                animales.remove(animal)
                HTTPResponseHandler.handle_response(self, 200, {"message": "Animal eliminado"})
            else:
                HTTPResponseHandler.handle_response(self, 404, {"error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(self, 404, {"error": "Ruta no encontrada"})

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
