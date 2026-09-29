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
# PROGRAMADOR
# ==================================================

class AgenteProgramador(Agente):

    def __init__(self):

        super().__init__(
            "Programador",
            """
            Sos un agente programador.

            Tu tarea es generar una solución
            de programación para el problema recibido.

            Debés:
            - escribir código claro;
            - utilizar buenas prácticas;
            - mantener la solución simple;
            - resolver exactamente lo solicitado.

            No hagas una revisión del código.
            No hagas una explicación extensa.

            Respondé exclusivamente en español. No utilices palabras de otros idiomas.
            """
        )


# ==================================================
# REVISOR
# ==================================================

class AgenteRevisor(Agente):

    def __init__(self):

        super().__init__(
            "Revisor",
            """
            Sos un agente revisor de código.

            Analizá el código recibido.

            Debés verificar:
            - errores de sintaxis;
            - errores lógicos;
            - claridad;
            - buenas prácticas;
            - posibles mejoras.

            Si encontrás errores, proponé una
            versión corregida del código.

            No hagas una explicación educativa
            extensa.

            Respondé exclusivamente en español. No utilices palabras de otros idiomas.
            """
        )


# ==================================================
# EXPLICADOR
# ==================================================

class AgenteExplicador(Agente):

    def __init__(self):

        super().__init__(
            "Explicador",
            """
            Sos un agente especializado en explicar código.

            Utilizando el problema, el código generado
            y la revisión realizada, prepará una explicación
            clara y educativa.

            La respuesta debe incluir:

            1. Qué hace el programa
            2. Código final
            3. Cómo funciona
            4. Explicación de las partes importantes
            5. Ejemplo de uso

            Respondé exclusivamente en español. No utilices palabras de otros idiomas.
            """
        )


# ==================================================
# SALIDA ESTRUCTURADA DEL COORDINADOR
# ==================================================

class Decision(BaseModel):

    agente: Literal[
        "programador",
        "revisor",
        "explicador",
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

        self.programador = AgenteProgramador()
        self.revisor = AgenteRevisor()
        self.explicador = AgenteExplicador()


        self.modelo_coordinador = modelo.with_structured_output(
            Decision,
            method="json_schema"
        )


        self.prompt_coordinador = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                Sos el coordinador de un sistema multiagente
                especializado en programación.

                Agentes disponibles:

                programador:
                genera una solución de código para
                el problema solicitado.

                revisor:
                revisa el código generado, detecta
                errores y propone mejoras.

                explicador:
                genera la respuesta final explicando
                el código y utilizando la revisión.

                finalizar:
                seleccionar cuando la explicación final
                ya está completa.

                Reglas:

                - Si todavía no hay código, utilizar programador.
                - Si hay código pero todavía no fue revisado,
                  utilizar revisor.
                - Si hay código y revisión pero todavía no hay
                  explicación final, utilizar explicador.
                - Si la explicación final ya existe,
                  seleccionar finalizar.

                Analizá el estado actual y decidí
                qué agente debe actuar.

                No hagas vos mismo el trabajo.
                """
            ),
            (
                "human",
                """
                Problema:
                {problema}

                Código generado:
                {codigo}

                Revisión:
                {revision}

                Explicación final:
                {explicacion}
                """
            )
        ])

        self.cadena_coordinador = self.prompt_coordinador | self.modelo_coordinador


    def decidir(self, problema, codigo, revision, explicacion):

        return self.cadena_coordinador.invoke({
            "problema": problema,
            "codigo": codigo,
            "revision": revision,
            "explicacion": explicacion
        })


    def ejecutar(self, problema):

        codigo = ""
        revision = ""
        explicacion = ""

        max_pasos = 10


        for paso in range(max_pasos):

            print("\n================================")
            print(f"PASO {paso + 1}")
            print("================================")


            decision = self.decidir(problema, codigo, revision, explicacion)

            print(f"Coordinador decidió: {decision.agente}")

            print(f"Motivo: {decision.motivo}")


            # ==========================================
            # PROGRAMADOR
            # ==========================================

            if decision.agente == "programador":

                codigo = self.programador.ejecutar(problema)


            # ==========================================
            # REVISOR
            # ==========================================

            elif decision.agente == "revisor":

                entrada = f"""
                Problema:
                {problema}

                Código generado:
                {codigo}
                """

                revision = self.revisor.ejecutar(entrada)


            # ==========================================
            # EXPLICADOR
            # ==========================================

            elif decision.agente == "explicador":

                entrada = f"""
                Problema:
                {problema}

                Código generado:
                {codigo}

                Revisión:
                {revision}
                """

                explicacion = self.explicador.ejecutar(entrada)


            # ==========================================
            # FINALIZAR
            # ==========================================

            elif decision.agente == "finalizar":

                print("\n✅ Sistema finalizado")

                return explicacion


        print("\n⚠ Se alcanzó el máximo de pasos")

        return explicacion


# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    sistema = Coordinador()

    problema = """
    Crear una función en JavaScript
    que reciba dos números y devuelva
    la suma de ambos.
    """

    resultado = sistema.ejecutar(problema)

    print("\n")
    print("================================")
    print("RESPUESTA FINAL")
    print("================================")

    print(resultado)