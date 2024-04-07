
import requests
import json

def crear_partida(jugador):
    data = {"jugador": jugador}
    response = requests.post("http://localhost:8000/partida", data=json.dumps(data))
    print(response.json())

def listar_partidas():
    response = requests.get("http://localhost:8000/partidas")
    print(response.json())

def listar_partidas_perdidas():
    response = requests.get("http://localhost:8000/partidas/perdidas")
    print(response.json())

def listar_partidas_ganadas():
    response = requests.get("http://localhost:8000/partidas/ganadas")
    print(response.json())

if __name__ == "__main__":
    
    print("Creando partida...\n jugando piedra\n")
    crear_partida("piedra")
    # ver partidas jugadas
    print("Listando partidas jugadas...\n")
    listar_partidas()
    # ver partidas perdidas
    print("Listando partidas perdidas...\n")
    listar_partidas_perdidas()
    # ver partidas ganadas
    print("Listando partidas ganadas...\n")
    listar_partidas_ganadas()