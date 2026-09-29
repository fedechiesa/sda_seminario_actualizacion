class AsistenteTemperatura:

    def __init__(self):
        self.objetivo = 22

    def consultar(self, temperatura):
        if temperatura < self.objetivo:
            return 'Te recomiendo encender la calefacción'

        elif temperatura > self.objetivo:
            return 'Te recomiendo encender la refrigeración'

        else:
            return 'La temperatura es correcta'


asistente = AsistenteTemperatura()


while True:
    try:
        temperatura = float(input('Ingrese la temperatura actual: '))

        respuesta = asistente.consultar(temperatura)
        print(respuesta)

    except:
        break
