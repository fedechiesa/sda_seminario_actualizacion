class AgenteTemperatura:

    def __init__(self, temperatura_objetivo):

        # OBJETIVO
        self.objetivo = temperatura_objetivo

        # CONTEXTO / ESTADO ACTUAL
        self.temperatura = 0

        # MEMORIA
        self.memoria = []


    # ----------------------------------
    # PERCEPCIÓN
    # ----------------------------------
    def percibir(self, temperatura):
        self.temperatura = temperatura
        print(f"[PERCEPCIÓN] temperatura detectada: {temperatura}")

    # ----------------------------------
    # CONTEXTO
    # ----------------------------------
    def obtener_contexto(self):
        ultima_accion = None

        if self.memoria:
            ultima_accion = self.memoria[-1]["accion"]

        return {
            "temperatura": self.temperatura,
            "temperatura_objetivo": self.objetivo,
            "ultima_accion": ultima_accion
        }
    
    # ----------------------------------
    # DECISIÓN
    # ----------------------------------
    def decidir(self):

        contexto = self.obtener_contexto()

        temperatura = contexto["temperatura"]
        temperatura_objetivo = contexto["temperatura_objetivo"]
        ultima_accion = contexto["ultima_accion"]

        if temperatura > temperatura_objetivo + 2:
            return 'REFRIGERAR'

        if temperatura < temperatura_objetivo - 2:
            return 'CALEFACCIÓN'

        # cerca del objetivo uso la memoria
        if temperatura > temperatura_objetivo:
            if ultima_accion == "REFRIGERAR":
                return 'REFRIGERAR'

        if temperatura < temperatura_objetivo:
            if ultima_accion == "CALEFACCIÓN":
                return 'CALEFACCIÓN'

        return "MANTENER"


    # ----------------------------------
    # CAPACIDAD DE EJECUCIÓN
    # ----------------------------------
    def ejecutar(self, accion):
        print(f"[EJECUCIÓN] Acción: {accion}")


    # ----------------------------------
    # MEMORIA
    # ----------------------------------
    def recordar(self, accion):
        experiencia = {
            "temperatura": self.temperatura,
            "accion": accion
        }

        self.memoria.append(experiencia)


    # ----------------------------------
    # CICLO DEL AGENTE
    # ----------------------------------
    def ejecutar_ciclo(self, temperatura):

        # Percibir
        self.percibir(temperatura)

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

            try:
                temperatura = float(
                    input("Ingrese la temperatura actual: ")
                )

                agente.ejecutar_ciclo(temperatura)

                ciclo += 1
            except:
                break

# ----------------------------------
# CREAR AGENTE
# ----------------------------------
agente = AgenteTemperatura(temperatura_objetivo=22)
agente.run()
