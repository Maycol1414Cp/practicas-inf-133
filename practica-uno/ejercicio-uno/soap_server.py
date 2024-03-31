from http.server import HTTPServer, BaseHTTPRequestHandler
from pysimplesoap.server import SoapDispatcher, SOAPHandler
 
 #definiendo operaciones
def sumar(x,y):
    return x + y
 
def restar(x,y):
    return x - y

def multiplicar(x,y):
    return x * y

def dividir(x,y):
    return x / y


dispatcher = SoapDispatcher(
    "ejercicio-uno",
    location="http://localhost:8000/",
    action="http://localhost:8000/", 
    namespace="http://localhost:8000/",
    trace=True,
    ns="http://localhost:8000"
)

dispatcher.register_function(
    "sumar",
    sumar,
    returns={"result": int},
    args={"x": int, "y": int}
)

dispatcher.register_function(
    "restar",
    restar,
    returns={"result": int},
    args={"x": int, "y": int}
)

dispatcher.register_function(
    "multiplicar",
    multiplicar,
    returns={"result": int},
    args={"x": int, "y": int}
)

dispatcher.register_function(
    "dividir",
    dividir,
    returns={"result": int},
    args={"x": int, "y": int}
)

try:
    server = HTTPServer(("localhost", 8000), SOAPHandler)
    server.dispatcher = dispatcher
    print("Server started")
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()
    print("Server stopped")
