class Operacion:
    def __init__(self, funcion):
        self.funcion = funcion

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

resultado = mayusculas.ejecutar("Pepe")
resultado = saludar.ejecutar(resultado)
resultado = exclamar.ejecutar(resultado)

print(resultado)