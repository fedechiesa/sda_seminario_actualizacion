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
# PLANIFICADOR
# ==================================================

class AgentePlanificador(Agente):

    def __init__(self):

        super().__init__(
            "Planificador",
            """
            Sos un agente especializado en
            planificación de viajes.

            Analizá el viaje solicitado.

            Debés proponer:

            - duración del viaje;
            - distribución de los días;
            - actividades;
            - lugares para visitar;
            - organización general.

            No calcules todavía el presupuesto.

            Respondé exclusivamente en español. No utilices palabras de otros idiomas.
            Todos los campos de salida, incluido 'motivo', deben estar escritos únicamente en español.
            """
        )


# ==================================================
# PRESUPUESTADOR
# ==================================================

class AgentePresupuestador(Agente):

    def __init__(self):

        super().__init__(
            "Presupuestador",
            """
            Sos un agente especializado en
            presupuestos de viajes.

            Utilizando la planificación recibida,
            realizá una estimación general de gastos.

            Considerá:

            - alojamiento;
            - transporte;
            - comidas;
            - actividades;
            - gastos adicionales.

            Los valores son solamente estimativos.

            Respondé exclusivamente en español. No utilices palabras de otros idiomas.
            Todos los campos de salida, incluido 'motivo', deben estar escritos únicamente en español.
            """
        )


# ==================================================
# RECOMENDADOR
# ==================================================

class AgenteRecomendador(Agente):

    def __init__(self):

        super().__init__(
            "Recomendador",
            """
            Sos un agente especializado en viajes.

            Utilizando la planificación y el presupuesto,
            prepará una propuesta final para el viajero.

            Debés incluir:

            1. Resumen del viaje
            2. Itinerario
            3. Presupuesto estimado
            4. Recomendaciones
            5. Consejos importantes

            Respondé exclusivamente en español. No utilices palabras de otros idiomas.
            Todos los campos de salida, incluido 'motivo', deben estar escritos únicamente en español.
            """
        )


# ==================================================
# DECISIÓN DEL COORDINADOR
# ==================================================

class Decision(BaseModel):

    agente: Literal[
        "planificador",
        "presupuestador",
        "recomendador",
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

        self.planificador = AgentePlanificador()
        self.presupuestador = AgentePresupuestador()
        self.recomendador = AgenteRecomendador()


        self.modelo_coordinador = modelo.with_structured_output(
            Decision,
            method="json_schema"
        )

        self.prompt_coordinador = (
            ChatPromptTemplate.from_messages([
                (
                    "system",
                    """
                    Sos el coordinador de un sistema
                    multiagente especializado en viajes.

                    Agentes disponibles:

                    planificador:
                    crea el itinerario del viaje.

                    presupuestador:
                    estima los gastos utilizando
                    la planificación.

                    recomendador:
                    genera la propuesta final utilizando
                    la planificación y el presupuesto.

                    finalizar:
                    seleccionar cuando la propuesta
                    final ya está completa.


                    Reglas:

                    - Si todavía no existe planificación,
                      utilizar planificador.

                    - Si existe planificación pero todavía
                      no existe presupuesto,
                      utilizar presupuestador.

                    - Si existe planificación y presupuesto
                      pero todavía no existe propuesta final,
                      utilizar recomendador.

                    - Si la propuesta final ya existe,
                      seleccionar finalizar.

                    Analizá el estado actual y decidí
                    qué agente debe actuar.

                    No hagas vos mismo el trabajo.
                    """
                ),
                (
                    "human",
                    """
                    Solicitud del viaje:
                    {solicitud}

                    Planificación:
                    {planificacion}

                    Presupuesto:
                    {presupuesto}

                    Propuesta final:
                    {propuesta}
                    """
                )
            ])
        )

        self.cadena_coordinador = self.prompt_coordinador | self.modelo_coordinador


    def decidir(self, solicitud, planificacion, presupuesto, propuesta):

        return self.cadena_coordinador.invoke({
            "solicitud": solicitud,
            "planificacion": planificacion,
            "presupuesto": presupuesto,
            "propuesta": propuesta
        })


    def ejecutar(self, solicitud):

        planificacion = ""
        presupuesto = ""
        propuesta = ""

        max_pasos = 10


        for paso in range(max_pasos):

            print("\n================================")
            print(f"PASO {paso + 1}")
            print("================================")


            decision = self.decidir(solicitud, planificacion, presupuesto, propuesta)

            print(f"Coordinador decidió: {decision.agente}")

            print(f"Motivo: {decision.motivo}")


            # ==========================================
            # PLANIFICADOR
            # ==========================================

            if decision.agente == "planificador":

                planificacion = self.planificador.ejecutar(solicitud)


            # ==========================================
            # PRESUPUESTADOR
            # ==========================================

            elif decision.agente == "presupuestador":

                entrada = f"""
                Solicitud:

                {solicitud}

                Planificación:

                {planificacion}
                """

                presupuesto = self.presupuestador.ejecutar(entrada)


            # ==========================================
            # RECOMENDADOR
            # ==========================================

            elif decision.agente == "recomendador":

                entrada = f"""
                Solicitud:
                {solicitud}

                Planificación:
                {planificacion}

                Presupuesto:
                {presupuesto}
                """

                propuesta = self.recomendador.ejecutar(entrada)


            # ==========================================
            # FINALIZAR
            # ==========================================

            elif decision.agente == "finalizar":

                print("\n✅ Sistema finalizado")

                return propuesta


        print("\n⚠ Se alcanzó el máximo de pasos")

        return propuesta


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    sistema = Coordinador()

    solicitud = """
    Organizar un viaje de 5 días a Bariloche
    para dos personas.
    """

    resultado = sistema.ejecutar(solicitud)

    print("\n")
    print("================================")
    print("PROPUESTA FINAL")
    print("================================")

    print(resultado)