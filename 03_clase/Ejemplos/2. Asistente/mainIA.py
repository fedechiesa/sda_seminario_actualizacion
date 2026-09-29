from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


#pip install openai python-dotenv 
class AsistenteTemperatura:

    def __init__(self):
        self.objetivo = 22

    def consultar(self, temperatura):
        prompt = f"""
Sos un asistente inteligente para control de temperatura.

La temperatura objetivo es {self.objetivo} °C.
La temperatura actual es {temperatura} °C.

Analizá la situación y recomendale al usuario una de estas acciones:

- Te recomiendo encender la calefacción
- Te recomiendo encender la refrigeración
- La temperatura es correcta

Respondé de forma breve y clara.
"""

        respuesta = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return respuesta.output_text


asistente = AsistenteTemperatura()


while True:
    try:
        temperatura = float(input('Ingrese la temperatura actual: '))

        respuesta = asistente.consultar(temperatura)
        print(respuesta)

    except:
        break
