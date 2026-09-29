class Agente:
    def __init__(self, nombre, objetivo):
        self.nombre = nombre
        self.objetivo = objetivo

    def ejecutar(self):
        print(f'{self.nombre} está trabajando.')
        print(f'Objetivo: {self.objetivo}')

agente = Agente("Agente Analista", "Analizar datos de mercado")

agente.ejecutar()

