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


class DecisionDistribuida(BaseModel):

    siguiente: Literal[
        "investigador",
        "analista",
        "redactor",
        "revisor",
        "finalizar"
    ]

    resultado: str

    motivo: str


class AgenteDistribuido:

    def __init__(self, nombre, rol):

        self.nombre = nombre

        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                f"""
                Sos el agente {nombre} dentro de
                un sistema multiagente distribuido.

                Tu función es:

                {rol}

                No existe un coordinador central.

                Después de realizar tu trabajo,
                debés decidir quién debe continuar.

                Agentes disponibles:

                investigador:
                obtiene y organiza información.

                analista:
                analiza la información y obtiene conclusiones.

                redactor:
                redacta una respuesta final clara.

                revisor:
                revisa errores, calidad y omisiones.

                finalizar:
                elegilo solamente cuando consideres
                que la tarea está completamente resuelta.

                Respondé siempre en español.
                """
            ),
            (
                "human",
                """
                Tarea original:

                {tarea}

                Estado actual del trabajo:

                {estado}

                Realizá tu tarea y decidí quién
                debe continuar.
                """
            )
        ])

        self.cadena = (
            prompt
            | modelo.with_structured_output(
                DecisionDistribuida
            )
        )


    def ejecutar(self, tarea, estado):

        print(f"\n--- {self.nombre} ---")

        return self.cadena.invoke({
            "tarea": tarea,
            "estado": estado
        })




investigador = AgenteDistribuido(
    "Investigador",
    """
    Buscar, organizar y explicar información
    relevante sobre el problema.

    Si ya existe suficiente información,
    normalmente podés pasar el trabajo
    al analista.
    """
)


analista = AgenteDistribuido(
    "Analista",
    """
    Analizar la información disponible,
    relacionar conceptos y obtener conclusiones.

    Si falta información, podés devolver
    el trabajo al investigador.

    Si el análisis está completo,
    podés enviarlo al redactor.
    """
)


redactor = AgenteDistribuido(
    "Redactor",
    """
    Construir una respuesta final clara,
    ordenada y didáctica.

    Si detectás que falta análisis,
    podés enviarlo al analista.

    Si considerás que la respuesta está lista,
    podés enviarla al revisor.
    """
)


revisor = AgenteDistribuido(
    "Revisor",
    """
    Revisar el trabajo realizado.

    Detectar errores, omisiones,
    inconsistencias o problemas de claridad.

    Podés enviar nuevamente el trabajo
    al investigador, analista o redactor.

    Si todo está correcto,
    podés elegir finalizar.
    """
)


agentes = {
    "investigador": investigador,
    "analista": analista,
    "redactor": redactor,
    "revisor": revisor
}



def ejecutar_distribuido(tarea):

    estado = """
    Todavía no se realizó ningún trabajo.
    """

    # Elegimos únicamente el agente inicial.
    siguiente = "investigador"

    max_pasos = 10


    for paso in range(max_pasos):

        print("\n======================")
        print("PASO", paso + 1)
        print("======================")


        # =================================
        # EJECUTAR AGENTE ACTUAL
        # =================================

        agente = agentes[siguiente]

        decision = agente.ejecutar(
            tarea,
            estado
        )


        print(
            f"{agente.nombre} →",
            decision.siguiente
        )

        print(
            "Motivo:",
            decision.motivo
        )


        # =================================
        # GUARDAR RESULTADO
        # =================================

        estado += f"""

        ==============================

        Agente:
        {agente.nombre}

        Resultado:

        {decision.resultado}

        """


        # =================================
        # FINALIZAR
        # =================================

        if decision.siguiente == "finalizar":

            print("\nProceso finalizado.")

            break


        # =================================
        # EL AGENTE DECIDE QUIÉN CONTINÚA
        # =================================

        siguiente = decision.siguiente


    return estado



resultado = ejecutar_distribuido(
    """
    Explicar las ventajas y riesgos
    del uso de inteligencia artificial
    en educación.
    """
)

print("\n===== RESULTADO =====")

print(resultado)