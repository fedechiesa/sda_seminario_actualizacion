import json

with open('empleados.json','r', encoding='utf-8') as archivo:
    empleados = json.load(archivo)

#print(empleados)

for empleado in empleados:
    print(empleado['id'], '-', empleado['name'], '-', empleado['profile']['contact']['email'])