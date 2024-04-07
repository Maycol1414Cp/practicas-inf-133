from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

pacientes = [{
    "ci": "123456789",
    "nombre": "Brayan",
    "apellido": "Cruz",
    "edad": 25,
    "genero": "Masculino",
    "diagnostico": "Diabetes",
    "doctor": "Pedro Pérez"},
    {
    "ci": "987654321",
    "nombre": "Maria",
    "apellido": "Perez",
    "edad": 30,
    "genero": "Femenino",
    "diagnostico": "Hipertension",
    "doctor": "Juana Salinas"
    }]

class PacienteBuilder:
    def __init__(self):
        self.paciente = {}

    def set_ci(self, ci):
        self.paciente["ci"] = ci
        return self

    def set_nombre(self, nombre):
        self.paciente["nombre"] = nombre
        return self

    def set_apellido(self, apellido):
        self.paciente["apellido"] = apellido
        return self

    def set_edad(self, edad):
        self.paciente["edad"] = edad
        return self

    def set_genero(self, genero):
        self.paciente["genero"] = genero
        return self

    def set_diagnostico(self, diagnostico):
        self.paciente["diagnostico"] = diagnostico
        return self

    def set_doctor(self, doctor):
        self.paciente["doctor"] = doctor
        return self

    def build(self):
        return self.paciente

class PacientesService:
    @staticmethod
    def buscar_paciente(ci):
        for paciente in pacientes:
            if paciente["ci"] == ci:
                return paciente
        return None

    @staticmethod
    def listar_pacientes():
        return pacientes

    @staticmethod
    def agregar_paciente(data):
        pacientes.append(data)
        return pacientes

    @staticmethod
    def actualizar_paciente(ci, data):
        paciente = PacientesService.buscar_paciente(ci)
        if paciente:
            paciente.update(data)
            return pacientes
        else:
            return None

    @staticmethod
    def eliminar_paciente(ci):
        paciente = PacientesService.buscar_paciente(ci)
        if paciente:
            pacientes.remove(paciente)
            return pacientes
        else:
            return None

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

        if parsed_path.path == "/pacientes":
            if "ci" in query_params:
                ci = query_params["ci"][0]
                paciente = PacientesService.buscar_paciente(ci)
                if paciente:
                    HTTPResponseHandler.handle_response(self, 200, [paciente])
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            elif "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = [paciente for paciente in pacientes if paciente["diagnostico"] == diagnostico]
                HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = [paciente for paciente in pacientes if paciente["doctor"] == doctor]
                HTTPResponseHandler.handle_response(self, 200, pacientes_filtrados)
            else:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            paciente_builder = PacienteBuilder()
            paciente = paciente_builder \
                .set_ci(data["ci"]) \
                .set_nombre(data["nombre"]) \
                .set_apellido(data["apellido"]) \
                .set_edad(data["edad"]) \
                .set_genero(data["genero"]) \
                .set_diagnostico(data["diagnostico"]) \
                .set_doctor(data["doctor"]) \
                .build()
            pacientes = PacientesService.agregar_paciente(paciente)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith("/pacientes/"):
            ci = parsed_path.path.split("/")[-1]
            data = self.read_data()
            pacientes = PacientesService.actualizar_paciente(ci, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith("/pacientes/"):
            ci = parsed_path.path.split("/")[-1]
            pacientes = PacientesService.eliminar_paciente(ci)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

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
