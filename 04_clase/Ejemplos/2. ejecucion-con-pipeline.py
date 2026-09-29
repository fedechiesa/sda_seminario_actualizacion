class Operacion:
    def __init__(self, funcion):
        self.funcion = funcion

    def __or__(self, otra):
        #print('__or__')
        def nueva_funcion(valor):
            resultado = self.funcion(valor)
            return otra.funcion(resultado)

        return Operacion(nueva_funcion)

    def ejecutar(self, valor):
        return self.funcion(valor)


mayusculas = Operacion(
    lambda texto: texto.upper()
)

saludar = Operacion(
    lambda texto: "Hola " + texto
)

exclamar = Operacion(
    lambda texto: texto + "!!!"
)


cadena = mayusculas | saludar | exclamar

resultado = cadena.ejecutar("Pepe")

print(resultado)