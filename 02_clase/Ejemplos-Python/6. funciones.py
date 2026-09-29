def sumar(a,b):
    return a + b

resultado = sumar(10,20)
print(resultado)


def consultar_temperatura():
    return 32

def encender_ventilador():
    print("ventilador encendido")


temperatura = consultar_temperatura()

if temperatura > 30:
    encender_ventilador()




