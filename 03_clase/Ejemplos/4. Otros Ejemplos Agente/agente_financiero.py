class AgenteFinanciero:

    def __init__(self, presupuesto):

        # OBJETIVO
        self.objetivo = presupuesto

        # CONTEXTO / ESTADO ACTUAL
        self.gasto = 0

        # MEMORIA
        self.memoria = []


    # ----------------------------------
    # PERCEPCIÓN
    # ----------------------------------
    def percibir(self, gasto):
        self.gasto = gasto
        print(f"[PERCEPCIÓN] Gasto detectado: ${gasto:.2f}")

    # ----------------------------------
    # CONTEXTO
    # ----------------------------------
    def obtener_contexto(self):
        ultima_accion = None

        if self.memoria:
            ultima_accion = self.memoria[-1]["accion"]

        return {
            "gasto": self.gasto,
            "objetivo": self.objetivo,
            "ultima_accion": ultima_accion
        }
    
    # ----------------------------------
    # DECISIÓN
    # ----------------------------------
    def decidir(self):

        contexto = self.obtener_contexto()

        gasto = contexto["gasto"]
        presupuesto = contexto["objetivo"]
        ultima_accion = contexto["ultima_accion"]

        if gasto > presupuesto:
            if ultima_accion == "ALERTA":
                return "REDUCIR_GASTOS"
            return "ALERTA"
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
            "gasto": self.gasto,
            "accion": accion
        }

        self.memoria.append(experiencia)


    # ----------------------------------
    # CICLO DEL AGENTE
    # ----------------------------------
    def ejecutar_ciclo(self, gasto):

        # Percibir
        self.percibir(gasto)

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
                gasto = float(
                    input("Ingrese el gasto actual: ")
                )

                agente.ejecutar_ciclo(gasto)

                ciclo += 1
            except:
                break

# ----------------------------------
# CREAR AGENTE
# ----------------------------------
agente = AgenteFinanciero(presupuesto=1000)
agente.run()
