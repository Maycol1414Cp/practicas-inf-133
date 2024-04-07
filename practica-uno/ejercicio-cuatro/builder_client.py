import requests
import json

# URL base del servidor RESTful
url = "http://localhost:8000/"

# GET para obtener todos los pacientes
ruta_get_pacientes = url + "pacientes"
get_pacientes_response = requests.get(ruta_get_pacientes)
print("GET /pacientes:", get_pacientes_response.json())

# POST para agregar un nuevo paciente
ruta_post_paciente = url + "pacientes"
nuevo_paciente_data = {
    "ci": "123456789",
    "nombre": "Juan",
    "apellido": "Pérez",
    "edad": 30,
    "genero": "Masculino",
    "diagnostico": "Diabetes",
    "doctor": "Pedro Pérez"
}
post_paciente_response = requests.post(ruta_post_paciente, json=nuevo_paciente_data)
print("POST /pacientes:", post_paciente_response.json())

# GET para filtrar por CI con query params
ci_paciente = "123456789"
ruta_get_paciente_ci = f"{url}pacientes?ci={ci_paciente}"
get_paciente_ci_response = requests.get(ruta_get_paciente_ci)
print(f"GET /pacientes?ci={ci_paciente}:", get_paciente_ci_response.json())

# GET para listar pacientes con diagnóstico de Diabetes
diagnostico = "Diabetes"
ruta_get_pacientes_diagnostico = f"{url}pacientes?diagnostico={diagnostico}"
get_pacientes_diagnostico_response = requests.get(ruta_get_pacientes_diagnostico)
print(f"GET /pacientes?diagnostico={diagnostico}:", get_pacientes_diagnostico_response.json())

# GET para listar pacientes atendidos por el doctor Pedro Pérez
doctor = "Pedro Pérez"
ruta_get_pacientes_doctor = f"{url}pacientes?doctor={doctor}"
get_pacientes_doctor_response = requests.get(ruta_get_pacientes_doctor)
print(f"GET /pacientes?doctor={doctor}:", get_pacientes_doctor_response.json())

# PUT para actualizar información de un paciente
ci_paciente_actualizar = "123456789"
ruta_put_paciente = f"{url}pacientes/{ci_paciente_actualizar}"
datos_actualizados = {
    "nombre": "Juanito",
    "edad": 35
}
put_paciente_response = requests.put(ruta_put_paciente, json=datos_actualizados)
print("PUT /pacientes/{ci}:", put_paciente_response.json())

# DELETE para eliminar un paciente
ruta_delete_paciente = f"{url}pacientes/{ci_paciente_actualizar}"
delete_paciente_response = requests.delete(ruta_delete_paciente)
print("DELETE /pacientes/{ci}:", delete_paciente_response.json())
