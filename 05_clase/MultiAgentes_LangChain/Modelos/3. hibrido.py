from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()


# =========================================
# MODELO
# =========================================

modelo = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)


# =========================================
# DECISIONES ESTRUCTURADAS
# =========================================

class DecisionCoordinador(BaseModel):
    agente: Literal[
        "investigador",
        "analista",
        "redactor",
        "revisor",
        "finalizar"
    ]
    motivo: str


class DecisionInvestigador(BaseModel):
    siguiente: Literal[
        "analista",
        "coordinador"
    ]
    resultado: str
    motivo: str


class DecisionAnalista(BaseModel):
    siguiente: Literal[
        "investigador",
        "redactor",
        "coordinador"
    ]
    resultado: str
    motivo: str


class DecisionRedactor(BaseModel):
    siguiente: Literal[
        "analista",
        "revisor",
        "coordinador"
    ]
    resultado: str
    motivo: str


class DecisionRevisor(BaseModel):
    siguiente: Literal[
        "investigador",
        "analista",
        "redactor",
        "coordinador"
    ]
    resultado: str
    motivo: str


# =========================================
# COORDINADOR LLM
# =========================================

class CoordinadorHibrido:

    def __init__(self):

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                Sos el coordinador principal de
                un sistema multiagente híbrido.

                Agentes disponibles:

                investigador:
                obtiene información concreta y relevante.

                analista:
                analiza la información y obtiene conclusiones.

                redactor:
                construye una respuesta final.

                revisor:
                revisa la calidad de la respuesta.

                finalizar:
                solamente si la respuesta ya fue redactada
                y revisada satisfactoriamente.

                Tu función es controlar globalmente
                el proceso.

                No hagas el trabajo de los agentes.
                Solamente decidí cuál debe intervenir.
                """
            ),
            (
                "human",
                """
                Tarea original:

                {tarea}

                Estado actual del trabajo:

                {estado}

                Decidí qué agente debe intervenir ahora.
                """
            )
        ])

        self.cadena = (
            prompt
            | modelo.with_structured_output(
                DecisionCoordinador
            )
        )

    def decidir(self, tarea, estado):

        return self.cadena.invoke({
            "tarea": tarea,
            "estado": estado
        })


# =========================================
# INVESTIGADOR
# =========================================

class Investigador:

    def __init__(self):

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                Sos el INVESTIGADOR.

                Tu trabajo es obtener y organizar
                información concreta sobre la tarea.

                IMPORTANTE:

                El campo resultado debe contener
                la información realmente obtenida.

                NO escribas frases como:

                "Se recopiló información"
                "Hay suficiente información"
                "Se procederá a analizar"

                Debés escribir los datos, conceptos,
                ventajas, riesgos, ejemplos, etc.

                Cuando termines:

                - elegí "analista" si la información
                  es suficiente para analizar.

                - elegí "coordinador" solamente si
                  existe algún problema que requiera
                  decisión global.
                """
            ),
            (
                "human",
                """
                Tarea:

                {tarea}

                Trabajo realizado hasta ahora:

                {estado}

                Investigá concretamente el tema.
                """
            )
        ])

        self.cadena = (
            prompt
            | modelo.with_structured_output(
                DecisionInvestigador
            )
        )

    def ejecutar(self, tarea, estado):

        return self.cadena.invoke({
            "tarea": tarea,
            "estado": estado
        })


# =========================================
# ANALISTA
# =========================================

class Analista:

    def __init__(self):

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                Sos el ANALISTA.

                Debés analizar concretamente
                la información disponible.

                Tu resultado debe contener:

                - relaciones encontradas;
                - ventajas;
                - riesgos;
                - consecuencias;
                - conclusiones.

                IMPORTANTE:

                NO digas:

                "Se procederá a analizar"
                "Es necesario analizar"
                "Hay información suficiente"

                HACÉ el análisis.

                Cuando termines:

                - si falta información importante:
                  siguiente = "investigador"

                - si el análisis está completo:
                  siguiente = "redactor"

                - si existe un problema global:
                  siguiente = "coordinador"

                Nunca podés elegirte a vos mismo.
                """
            ),
            (
                "human",
                """
                Tarea original:

                {tarea}

                Información disponible:

                {estado}

                Realizá ahora el análisis.
                """
            )
        ])

        self.cadena = (
            prompt
            | modelo.with_structured_output(
                DecisionAnalista
            )
        )

    def ejecutar(self, tarea, estado):

        return self.cadena.invoke({
            "tarea": tarea,
            "estado": estado
        })


# =========================================
# REDACTOR
# =========================================

class Redactor:

    def __init__(self):

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                Sos el REDACTOR.

                Utilizá la investigación y el análisis
                disponibles para escribir una respuesta
                completa para el usuario.

                Tu campo resultado debe contener
                LA RESPUESTA redactada.

                No describas lo que vas a hacer.
                Hacelo.

                Cuando termines:

                normalmente:
                    siguiente = "revisor"

                Si detectás que falta análisis:
                    siguiente = "analista"

                Si existe un problema global:
                    siguiente = "coordinador"
                """
            ),
            (
                "human",
                """
                Tarea original:

                {tarea}

                Trabajo disponible:

                {estado}

                Redactá ahora la respuesta.
                """
            )
        ])

        self.cadena = (
            prompt
            | modelo.with_structured_output(
                DecisionRedactor
            )
        )

    def ejecutar(self, tarea, estado):

        return self.cadena.invoke({
            "tarea": tarea,
            "estado": estado
        })


# =========================================
# REVISOR
# =========================================

class Revisor:

    def __init__(self):

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                Sos el REVISOR.

                Debés revisar la respuesta preparada.

                Evaluá:

                - exactitud;
                - claridad;
                - coherencia;
                - información faltante;
                - cumplimiento de la tarea.

                Tu resultado debe contener
                una revisión concreta.

                Si todo está correcto:
                    siguiente = "coordinador"

                Si falta información:
                    siguiente = "investigador"

                Si falta análisis:
                    siguiente = "analista"

                Si hay problemas de redacción:
                    siguiente = "redactor"
                """
            ),
            (
                "human",
                """
                Tarea original:

                {tarea}

                Trabajo realizado:

                {estado}

                Revisá el resultado.
                """
            )
        ])

        self.cadena = (
            prompt
            | modelo.with_structured_output(
                DecisionRevisor
            )
        )

    def ejecutar(self, tarea, estado):

        return self.cadena.invoke({
            "tarea": tarea,
            "estado": estado
        })


# =========================================
# INSTANCIAS DE LOS AGENTES
# =========================================

investigador = Investigador()
analista = Analista()
redactor = Redactor()
revisor = Revisor()


agentes = {
    "investigador": investigador,
    "analista": analista,
    "redactor": redactor,
    "revisor": revisor
}


# =========================================
# EJECUCIÓN HÍBRIDA
# =========================================

def ejecutar_hibrido(tarea):

    coordinador = CoordinadorHibrido()

    estado = "No se realizó ningún trabajo todavía."

    siguiente = "coordinador"

    historial = []

    max_pasos = 12


    for paso in range(max_pasos):

        print("\n======================")
        print("PASO", paso + 1)
        print("======================")


        # ====================================
        # COORDINADOR
        # ====================================

        if siguiente == "coordinador":

            decision = coordinador.decidir(
                tarea,
                estado
            )

            print(
                "coordinador →",
                decision.agente
            )

            print(
                "Motivo:",
                decision.motivo
            )


            if decision.agente == "finalizar":

                print("\nPROCESO FINALIZADO")
                break


            siguiente = decision.agente

            continue


        # ====================================
        # AGENTE
        # ====================================

        agente = agentes[siguiente]

        nombre_actual = siguiente

        print(
            f"\n--- {nombre_actual.upper()} ---"
        )


        decision = agente.ejecutar(
            tarea,
            estado
        )


        print(
            nombre_actual,
            "→",
            decision.siguiente
        )

        print(
            "Motivo:",
            decision.motivo
        )

        """ print("\nResultado:")
        print(decision.resultado) """


        # ====================================
        # ACTUALIZAR ESTADO
        # ====================================

        estado += f"""
        ================================
        AGENTE: {nombre_actual}
        RESULTADO:
        {decision.resultado}
        """

        historial.append(nombre_actual)

        siguiente = decision.siguiente


    return estado


# =========================================
# PROGRAMA PRINCIPAL
# =========================================

if __name__ == "__main__":

    tarea = """
    Explicar las ventajas y riesgos
    del uso de inteligencia artificial
    en educación.
    """

    resultado = ejecutar_hibrido(tarea)

    print("\n\n======================")
    print("RESULTADO FINAL")
    print("======================")

    print(resultado)
