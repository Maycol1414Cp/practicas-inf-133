from zeep import Client
client = Client('http://localhost:8000')

operacion=input("Ingrese la operacion que desea realizar: \n suma \n resta \n multiplicacion \n division \n")
x=int(input("Ingrese el primer numero: "))
y=int(input("Ingrese el segundo numero: "))

match(operacion.lower()):
    case "suma":
        print(client.service.sumar(x,y))
    case "resta":
        print(client.service.restar(x,y))
    case "multiplicacion":
        print(client.service.multiplicar(x,y))
    case "division":
        print(client.service.dividir(x,y))
    case _:
        print("Operacion no valida")