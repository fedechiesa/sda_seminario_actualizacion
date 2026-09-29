from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


# ==================================================
# MODELO
# ==================================================

modelo = ChatOpenAI(
    model="gpt-5.4-mini"
)


# ==================================================
# CLASE BASE AGENTE
# ==================================================

class Agente:

    def __init__(self, nombre, instrucciones):

        self.nombre = nombre

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                instrucciones
            ),
            (
                "human",
                "{entrada}"
            )
        ])

        self.cadena = self.prompt | modelo | StrOutputParser()


    def ejecutar(self, entrada):

        print(f"\n🤖 Ejecutando: {self.nombre}")

        return self.cadena.invoke({
            "entrada": entrada
        })


# ==================================================
# INVESTIGADOR
# ==================================================

class AgenteInvestigador(Agente):

    def __init__(self):

        super().__init__(
            "Investigador",
            """
            Sos un agente investigador.

            Investigá conceptualmente el tema recibido.

            Identificá:
            - conceptos importantes;
            - características;
            - aplicaciones;
            - ventajas;
            - limitaciones.

            No redactes el informe final.

            Respondé exclusivamente en español. No utilices palabras de otros idiomas.
            """
        )


# ==================================================
# ANALISTA
# ==================================================

class AgenteAnalista(Agente):

    def __init__(self):

        super().__init__(
            "Analista",
            """
            Sos un agente analista.

            Analizá la investigación recibida.

            Debés:
            - identificar puntos importantes;
            - relacionar conceptos;
            - detectar ventajas;
            - detectar riesgos;
            - extraer conclusiones.

            No redactes el informe final.

            Respondé exclusivamente en español. No utilices palabras de otros idiomas.
            """
        )


# ==================================================
# REDACTOR
# ==================================================

class AgenteRedactor(Agente):

    def __init__(self):

        super().__init__(
            "Redactor",
            """
            Sos un agente redactor profesional.

            Generá un informe final utilizando
            la información recibida.

            Estructura:

            1. Introducción
            2. Desarrollo
            3. Ventajas
            4. Riesgos o limitaciones
            5. Conclusión

            Respondé exclusivamente en español. No utilices palabras de otros idiomas.
            """
        )


# ==================================================
# SALIDA ESTRUCTURADA DEL COORDINADOR
# ==================================================

class Decision(BaseModel):

    agente: Literal[
        "investigador",
        "analista",
        "redactor",
        "finalizar"
    ] = Field(
        description="Próximo agente que debe ejecutarse"
    )

    motivo: str = Field(
        description="Motivo de la decisión"
    )


# ==================================================
# COORDINADOR
# ==================================================

class Coordinador:

    def __init__(self):

        self.investigador = AgenteInvestigador()
        self.analista = AgenteAnalista()
        self.redactor = AgenteRedactor()


        self.modelo_coordinador = modelo.with_structured_output(
            Decision,
            method="json_schema"
        )


        self.prompt_coordinador = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                Sos el coordinador de un sistema multiagente.

                Agentes disponibles:

                investigador:
                obtiene información sobre el tema.

                analista:
                analiza la información obtenida.

                redactor:
                prepara el informe final.

                finalizar:
                seleccionar cuando el informe final
                ya está completo.

                Analizá el estado actual y decidí
                qué agente debe actuar.

                No hagas vos mismo el trabajo.
                """
            ),
            (
                "human",
                """
                Tema:
                {tema}

                Investigación:
                {investigacion}

                Análisis:
                {analisis}

                Informe:
                {informe}
                """
            )
        ])

        self.cadena_coordinador = self.prompt_coordinador | self.modelo_coordinador


    def decidir(self, tema, investigacion, analisis, informe):

        return self.cadena_coordinador.invoke({
            "tema": tema,
            "investigacion": investigacion,
            "analisis": analisis,
            "informe": informe
        })


    def ejecutar(self, tema):

        investigacion = ""
        analisis = ""
        informe = ""

        max_pasos = 10


        for paso in range(max_pasos):

            print("\n================================")
            print(f"PASO {paso + 1}")
            print("================================")

            decision = self.decidir(tema, investigacion, analisis, informe)

            print(f"Coordinador decidió: {decision.agente}")

            print(f"Motivo: {decision.motivo}")


            if decision.agente == "investigador":

                investigacion = self.investigador.ejecutar(tema)


            elif decision.agente == "analista":

                entrada = f"""
                Tema:
                {tema}

                Investigación:
                {investigacion}
                """
                
                analisis = self.analista.ejecutar(entrada)


            elif decision.agente == "redactor":

                entrada = f"""
                Tema:
                {tema}

                Investigación:
                {investigacion}

                Análisis:
                {analisis}
                """

                informe = self.redactor.ejecutar(entrada)


            elif decision.agente == "finalizar":
                print("\n✅ Sistema finalizado")
                return informe


        print("\n⚠ Se alcanzó el máximo de pasos")

        return informe


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    sistema = Coordinador()

    tema = """
    Aplicaciones de inteligencia artificial
    en la educación
    """

    resultado = sistema.ejecutar(tema)


    print("\n")
    print("================================")
    print("INFORME FINAL")
    print("================================")

    print(resultado)