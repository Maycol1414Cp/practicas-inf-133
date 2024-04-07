from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import random

class Partida:
    def __init__(self, id, jugador):
        self.id = id
        self.jugador = jugador
        self.servidor = random.choice(["piedra", "papel", "tijera"])
        self.resultado = self.determinar_ganador()

    def determinar_ganador(self):
        if self.jugador == self.servidor:
            return "empate"
        if (self.jugador == "piedra" and self.servidor == "tijera") or \
           (self.jugador == "papel" and self.servidor == "piedra") or \
           (self.jugador == "tijera" and self.servidor == "papel"):
            return "ganó"
        return "perdió"

    def to_dict(self):
        return {
            "id": self.id,
            "jugador": self.jugador,
            "servidor": self.servidor,
            "resultado": self.resultado
        }

class Singleton:
    _instance = None
    partidas = []
    id_counter = 1

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    def crear_partida(self, jugador):
        partida = Partida(self.id_counter, jugador)
        self.partidas.append(partida)
        self.id_counter += 1
        return partida

    def listar_partidas(self):
        return [partida.to_dict() for partida in self.partidas]

    def listar_partidas_perdidas(self):
        return [partida.to_dict() for partida in self.partidas if partida.resultado == "perdió"]

    def listar_partidas_ganadas(self):
        return [partida.to_dict() for partida in self.partidas if partida.resultado == "ganó"]

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/partida":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            partida = Singleton().crear_partida(data["jugador"])
            self._send_response(201, partida.to_dict())
        else:
            self._send_response(404, {"error": "Ruta no encontrada"})

    def do_GET(self):
        if self.path == "/partidas":
            partidas = Singleton().listar_partidas()
            self._send_response(200, partidas)
        elif self.path == "/partidas/perdidas":
            partidas = Singleton().listar_partidas_perdidas()
            self._send_response(200, partidas)
        elif self.path == "/partidas/ganadas":
            partidas = Singleton().listar_partidas_ganadas()
            self._send_response(200, partidas)
        else:
            self._send_response(404, {"error": "Ruta no encontrada"})

    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()