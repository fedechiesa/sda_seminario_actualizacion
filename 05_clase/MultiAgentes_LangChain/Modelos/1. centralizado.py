from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv()


# =========================================
# MODELO
# =========================================

modelo = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


# =========================================
# DECISIÓN DEL COORDINADOR
# =========================================

class Decision(BaseModel):

    agente: Literal[
        "investigador",
        "analista",
        "redactor",
        "finalizar"
    ]

    motivo: str


# =========================================
# AGENTE BASE
# =========================================

class Agente:

    def __init__(self, nombre, rol):

        self.nombre = nombre

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                f"""
                Sos el agente {nombre}.

                Tu función es:

                {rol}

                Respondé siempre en español.
                """
            ),
            (
                "human",
                "{entrada}"
            )
        ])

        self.cadena = (
            prompt
            | modelo
            | StrOutputParser()
        )


    def ejecutar(self, entrada):

        print(f"\n--- {self.nombre} ---")

        resultado = self.cadena.invoke({
            "entrada": entrada
        })

        #print(resultado)

        return resultado


# =========================================
# AGENTES
# =========================================

investigador = Agente(
    "Investigador",
    """
    Investigar y organizar información
    relevante sobre el tema.
    """
)


analista = Agente(
    "Analista",
    """
    Analizar la información disponible
    y obtener conclusiones.
    """
)


redactor = Agente(
    "Redactor",
    """
    Crear una respuesta final clara,
    ordenada y didáctica.
    """
)


# =========================================
# COORDINADOR LLM
# =========================================

class Coordinador:

    def __init__(self):

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                Sos el coordinador central de
                un sistema multiagente.

                Tenés disponibles:

                investigador:
                obtiene información.

                analista:
                analiza información.

                redactor:
                prepara la respuesta final.

                finalizar:
                cuando la tarea está terminada.

                Toda la coordinación pasa por vos.

                Elegí qué agente debe actuar
                a continuación.
                """
            ),
            (
                "human",
                """
                Tarea:

                {tarea}

                Estado actual:

                {estado}

                ¿Qué agente debe actuar?
                """
            )
        ])

        self.cadena = (
            prompt
            | modelo.with_structured_output(Decision)
        )


    def decidir(self, tarea, estado):

        return self.cadena.invoke({
            "tarea": tarea,
            "estado": estado
        })



def ejecutar_centralizado(tarea):

    coordinador = Coordinador()

    estado = "Todavía no se realizó ningún trabajo."


    for paso in range(8):

        print("\n======================")
        print("PASO", paso + 1)
        print("======================")

        # El coordinador siempre decide
        decision = coordinador.decidir(
            tarea,
            estado
        )

        print(
            "Coordinador →",
            decision.agente
        )

        print(
            "Motivo:",
            decision.motivo
        )


        if decision.agente == "finalizar":
            break


        elif decision.agente == "investigador":

            resultado = investigador.ejecutar(
                f"""
                Tarea:
                {tarea}

                Estado:
                {estado}
                """
            )


        elif decision.agente == "analista":

            resultado = analista.ejecutar(
                f"""
                Tarea:
                {tarea}

                Estado:
                {estado}
                """
            )


        elif decision.agente == "redactor":

            resultado = redactor.ejecutar(
                f"""
                Tarea:
                {tarea}

                Estado:
                {estado}
                """
            )


        # El resultado vuelve al coordinador
        estado += f"""

        Agente ejecutado:
        {decision.agente}

        Resultado:
        {resultado}
        """


    return estado


resultado = ejecutar_centralizado(
    """
    Explicar las ventajas y riesgos
    de utilizar inteligencia artificial
    en educación.
    """
)

print(resultado)