import random

class AgenteRed:

    def __init__(self, objetivo):

        # OBJETIVO
        self.objetivo = objetivo

        # CONTEXTO / ESTADO ACTUAL
        self.latencia = 0
        self.estado = ""

        # MEMORIA
        self.memoria = []


    # ----------------------------------
    # PERCEPCIÓN
    # ----------------------------------
    def percibir(self):
        latencia = random.randint(10, 300)
        self.latencia = latencia

        estado = random.choice(["UP", "DOWN"])
        self.estado = estado

        print(f"[PERCEPCIÓN] Latencia: {latencia}ms | Estado: {estado}")

    # ----------------------------------
    # CONTEXTO
    # ----------------------------------
    def obtener_contexto(self):
        ultima_accion = None

        if self.memoria:
            ultima_accion = self.memoria[-1]["accion"]

        return {
            "latencia": self.latencia,
            "estado": self.estado,
            "objetivo": self.objetivo,
            "ultima_accion": ultima_accion
        }
    
    # ----------------------------------
    # DECISIÓN
    # ----------------------------------
    def decidir(self):

        contexto = self.obtener_contexto()

        estado = contexto["estado"]
        latencia = contexto["latencia"]
        ultima_accion = contexto["ultima_accion"]

        if estado == "DOWN":
            return "REINICIAR_CONEXION"
        elif latencia > 200:
            if ultima_accion == "CAMBIAR_RUTA":
                return "REINICIAR_CONEXION"
            return "CAMBIAR_RUTA"
        return "MANTENER"


    # ----------------------------------
    # CAPACIDAD DE EJECUCIÓN
    # ----------------------------------
    def ejecutar(self, accion):
        print(f"[EJECUCIÓN] {accion}")


    # ----------------------------------
    # MEMORIA
    # ----------------------------------
    def recordar(self, accion):
        experiencia = {
            "estado": self.estado,
            "latencia": self.latencia,
            "accion": accion
        }

        self.memoria.append(experiencia)


    # ----------------------------------
    # CICLO DEL AGENTE
    # ----------------------------------
    def ejecutar_ciclo(self):

        # Percibir
        self.percibir()

        # Obtener contexto
        contexto = self.obtener_contexto()

        print("Contexto:", contexto)

        # Decidir
        accion = self.decidir()

        print("Decisión:", accion)

        # Ejecutar
        self.ejecutar(accion)

        # Recordar
        self.recordar(accion)

    # ----------------------------------
    # EJECUTAR VARIOS CICLOS
    # ----------------------------------
    def run(self):
        ciclo = 0

        while True:

            print("\n-------------------------")
            print("Ciclo", ciclo + 1)
            print("-------------------------")

            agente.ejecutar_ciclo()

            ciclo += 1
            if ciclo >= 20: break

# ----------------------------------
# CREAR AGENTE
# ----------------------------------
agente = AgenteRed("Mantener la red operativa con latencia menor o igual a 200 ms")
agente.run()


