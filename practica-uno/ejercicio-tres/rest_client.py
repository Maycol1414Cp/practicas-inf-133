import requests

# URL base del servidor RESTful
url = "http://localhost:8000/"

print("\nlistar todos los pacientes")
# GET para obtener todos los pacientes
ruta_get_pacientes = url + "pacientes"
get_pacientes_response = requests.get(ruta_get_pacientes)
print("GET /pacientes:", get_pacientes_response.json())

print("\nagregar un nuevo paciente")
# POST para agregar un nuevo paciente
ruta_post_paciente = url + "pacientes"
nuevo_paciente = {
    "ci": "123456789",
    "nombre": "Juan",
    "apellido": "Pérez",
    "edad": 30,
    "genero": "Masculino",
    "diagnostico": "Diabetes",
    "doctor": "Pedro Pérez"
}
post_paciente_response = requests.post(ruta_post_paciente, json=nuevo_paciente)
print("POST /pacientes:", post_paciente_response.json())

print("\nbuscar paciente con el CI")
# GET para filtrar por CI con query params
ci_paciente = "123456789"
ruta_get_paciente_ci = f"{url}pacientes?ci={ci_paciente}"
get_paciente_ci_response = requests.get(ruta_get_paciente_ci)
print(f"GET /pacientes?ci={ci_paciente}:", get_paciente_ci_response.json())

print("\nbuscar paciente con diabetes")
# GET para listar pacientes con diagnóstico de Diabetes
diagnostico = "Diabetes"
ruta_get_pacientes_diagnostico = f"{url}pacientes?diagnostico={diagnostico}"
get_pacientes_diagnostico_response = requests.get(ruta_get_pacientes_diagnostico)
print(f"GET /pacientes?diagnostico={diagnostico}:", get_pacientes_diagnostico_response.json())

print("\nbuscar pacientes atendidos por el doctor Pedro Pérez")
# GET para listar pacientes atendidos por el doctor Pedro Pérez
doctor = "Pedro Pérez"
ruta_get_pacientes_doctor = f"{url}pacientes?doctor={doctor}"
get_pacientes_doctor_response = requests.get(ruta_get_pacientes_doctor)
print(f"GET /pacientes?doctor={doctor}:", get_pacientes_doctor_response.json())

print("\nactualizar información de un paciente")
# PUT para actualizar información de un paciente
ci_paciente_actualizar = "123456789"
ruta_put_paciente = f"{url}pacientes/{ci_paciente_actualizar}"
datos_actualizados = {
    "nombre": "Juan",
    "edad": 35
}
put_paciente_response = requests.put(ruta_put_paciente, json=datos_actualizados)
print("PUT /pacientes/{ci}:", put_paciente_response.json())

print("\neliminar un paciente")
# DELETE para eliminar un paciente
ruta_delete_paciente = f"{url}pacientes/{ci_paciente_actualizar}"
delete_paciente_response = requests.delete(ruta_delete_paciente)
print("DELETE /pacientes/{ci}:", delete_paciente_response.json())
