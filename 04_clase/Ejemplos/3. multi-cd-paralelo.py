from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


modelo = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

class Agente:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

    def ejecutar(self, datos):
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                f"""
                Sos un agente especializado.

                Tu nombre es: {self.nombre}
                Tu función es: {self.rol}

                Respondé solamente con el resultado solicitado.
                """
            ),
            (
                "human",
                "Datos: {datos}"
            )
        ])

        parser = StrOutputParser()

        cadena = prompt | modelo | parser

        respuesta = cadena.invoke({
            "datos": datos
        })

        return respuesta


class Coordinador:
    def __init__(self):
        self.agentes = {
            "ordenar": Agente(
                "Agente Ordenador",
                "Ordenar una lista de números de menor a mayor"
            ),

            "promedio": Agente(
                "Agente Promedio",
                "Calcular el promedio de una lista de números"
            ),

            "maximo": Agente(
                "Agente Máximo",
                "Determinar el número máximo"
            ),

            "minimo": Agente(
                "Agente Mínimo",
                "Determinar el número mínimo"
            )
        }

    def ejecutar(self, datos):
        resultados = {}

        for nombre, agente in self.agentes.items():
            resultados[nombre] = agente.ejecutar(datos)

        return resultados


coordinador = Coordinador()

numeros = [8, 3, 15, 2, 9, 11]
print('Entrada:', numeros)
print()

resultados = coordinador.ejecutar(numeros)

print("RESULTADOS")
print("------------------------")

for tarea, resultado in resultados.items():
    print(f"{tarea}: {resultado}")