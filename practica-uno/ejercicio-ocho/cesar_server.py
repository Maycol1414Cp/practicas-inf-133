from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Mensaje:
    def __init__(self, id, contenido):
        self.id = id
        self.contenido = contenido
        self.contenido_encriptado = self.encriptar()

    def encriptar(self):
        return ''.join(chr((ord(c) - 97 + 3) % 26 + 97) if c.isalpha() else c for c in self.contenido)

    def to_dict(self):
        return {
            "id": self.id,
            "contenido": self.contenido,
            "contenido_encriptado": self.contenido_encriptado
        }

class Singleton:
    _instance = None
    mensajes = []
    id_counter = 1

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    def crear_mensaje(self, contenido):
        mensaje = Mensaje(self.id_counter, contenido)
        self.mensajes.append(mensaje)
        self.id_counter += 1
        return mensaje

    def listar_mensajes(self):
        return [mensaje.to_dict() for mensaje in self.mensajes]

    def buscar_mensaje(self, id):
        for mensaje in self.mensajes:
            if mensaje.id == id:
                return mensaje
        return None

    def actualizar_mensaje(self, id, contenido):
        mensaje = self.buscar_mensaje(id)
        if mensaje is not None:
            mensaje.contenido = contenido
            mensaje.contenido_encriptado = mensaje.encriptar()
        return mensaje

    def eliminar_mensaje(self, id):
        mensaje = self.buscar_mensaje(id)
        if mensaje is not None:
            self.mensajes.remove(mensaje)
        return mensaje

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/mensajes":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            mensaje = Singleton().crear_mensaje(data["contenido"])
            self._send_response(201, mensaje.to_dict())
        else:
            self._send_response(404, {"error": "Ruta no encontrada"})

    def do_GET(self):
        if self.path.startswith("/mensajes"):
            id = None
            if "/" in self.path[9:]:
                id = int(self.path[10:])
            if id is not None:
                mensaje = Singleton().buscar_mensaje(id)
                if mensaje is not None:
                    self._send_response(200, mensaje.to_dict())
                else:
                    self._send_response(404, {"error": "Mensaje no encontrado"})
            else:
                mensajes = Singleton().listar_mensajes()
                self._send_response(200, mensajes)
        else:
            self._send_response(404, {"error": "Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/mensajes"):
            id = None
            if "/" in self.path[9:]:
                id = int(self.path[10:])
            if id is not None:
                content_length = int(self.headers["Content-Length"])
                put_data = self.rfile.read(content_length)
                data = json.loads(put_data)
                mensaje = Singleton().actualizar_mensaje(id, data["contenido"])
                if mensaje is not None:
                    self._send_response(200, mensaje.to_dict())
                else:
                    self._send_response(404, {"error": "Mensaje no encontrado"})
            else:
                self._send_response(400, {"error": "ID no proporcionado"})
        else:
            self._send_response(404, {"error": "Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/mensajes"):
            id = None
            if "/" in self.path[9:]:
                id = int(self.path[10:])
            if id is not None:
                mensaje = Singleton().eliminar_mensaje(id)
                if mensaje is not None:
                    self._send_response(200, {"mensaje": "Mensaje eliminado"})
                else:
                    self._send_response(404, {"error": "Mensaje no encontrado"})
            else:
                self._send_response(400, {"error": "ID no proporcionado"})
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