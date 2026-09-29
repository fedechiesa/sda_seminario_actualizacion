from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ------------------------------------------------
# Cargar variables de entorno
# ------------------------------------------------

load_dotenv()


# ------------------------------------------------
# Modelo OpenAI
# ------------------------------------------------

modelo = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0.2
)


# ------------------------------------------------
# Clase base Agente
# ------------------------------------------------

class Agente:

    def __init__(self, nombre, prompt):

        self.nombre = nombre
        self.prompt = ChatPromptTemplate.from_template(prompt)
        self.parser = StrOutputParser()
        self.cadena = self.prompt | modelo | self.parser


    def ejecutar(self, entrada):

        print(f"\n--- Ejecutando agente: {self.nombre} ---")

        resultado = self.cadena.invoke({
            "entrada": entrada
        })

        return resultado



class AgenteInvestigador(Agente):

    def __init__(self):

        prompt = """
        Sos un agente investigador.

        Tu tarea es investigar conceptualmente el siguiente tema:

        {entrada}

        Identificá:

        - conceptos principales;
        - características importantes;
        - ventajas;
        - desventajas;
        - posibles aplicaciones.

        Respondé exclusivamente en español. No utilices palabras de otros idiomas.

        No redactes todavía un informe final.
        Generá solamente información que después pueda utilizar otro agente.
        """

        super().__init__(
            "Investigador",
            prompt
        )


class AgenteAnalista(Agente):

    def __init__(self):

        prompt = """
        Sos un agente analista.

        Recibiste la siguiente investigación:

        {entrada}

        Analizá la información.

        Tu tarea es:

        - identificar los puntos más importantes;
        - eliminar información redundante;
        - relacionar los conceptos;
        - detectar ventajas y riesgos;
        - extraer conclusiones.

        Respondé exclusivamente en español. No utilices palabras de otros idiomas.

        No redactes todavía el informe final.
        """

        super().__init__(
            "Analista",
            prompt
        )


class AgenteRedactor(Agente):

    def __init__(self):

        prompt = """
        Sos un agente redactor profesional.

        Recibiste el siguiente análisis:

        {entrada}

        Escribí un informe final claro y organizado.

        El informe debe incluir:

        1. Introducción
        2. Desarrollo
        3. Ventajas
        4. Riesgos o limitaciones
        5. Conclusión

        Utilizá lenguaje claro y profesional.

        Respondé exclusivamente en español. No utilices palabras de otros idiomas.
        """

        super().__init__(
            "Redactor",
            prompt
        )


class Coordinador:

    def __init__(self):

        self.investigador = AgenteInvestigador()
        self.analista = AgenteAnalista()
        self.redactor = AgenteRedactor()


    def ejecutar(self, tema):

        print("\n================================")
        print("INICIANDO SISTEMA MULTIAGENTE")
        print("================================")


        # 1. Investigar
        investigacion = self.investigador.ejecutar(tema)

        #print("\nINVESTIGACIÓN:")
        #print(investigacion)


        # 2. Analizar
        analisis = self.analista.ejecutar(investigacion)

        #print("\nANÁLISIS:")
        #print(analisis)


        # 3. Redactar
        informe = self.redactor.ejecutar(analisis)


        return informe



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