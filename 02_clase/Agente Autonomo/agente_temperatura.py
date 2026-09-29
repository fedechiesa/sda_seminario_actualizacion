import random
import time

#======================================================
#              AGENTE DE TEMPERATURA
#======================================================
class AgenteTemperatura:
    def __init__(self, temperatura_objetivo):
        # OBJETIVO
        self.temperatura_objetivo = temperatura_objetivo

        # CONTEXTO / ESTADO ACTUAL
        self.temperatura_actual = None
        self.calefactor_encendido = False
        self.ventilador_encendido = False

        # MEMORIA
        self.memoria = []


    #======================================================
    #                    PERCEPCIÓN
    #======================================================
    def percibir(self):
        self.temperatura_actual = random.randint(10,30)
        return self.temperatura_actual


    #======================================================
    #                     DECISIÓN
    #======================================================
    def decidir(self, temperatura):
        if temperatura < self.temperatura_objetivo:
            return 'ENCENDER CALEFACCIÓN'
        elif temperatura > self.temperatura_objetivo:
            return 'ENCENDER VENTILADOR'
        else:
            return 'MANTENER'


    #======================================================
    #                     ACCIONES
    #======================================================
    def ejecutar(self, accion):
        if accion == 'ENCENDER CALEFACCIÓN':
            self.calefactor_encendido = True
            self.ventilador_encendido = False

        elif accion == 'ENCENDER VENTILADOR':
            self.calefactor_encendido = False
            self.ventilador_encendido = True
        else:
            self.calefactor_encendido = False
            self.ventilador_encendido = False

    

    #======================================================
    #                     MEMORIA
    #======================================================
    def recordar(self, accion):
        registro = {
            'temperatura': self.temperatura_actual,
            'accion': accion
        }

        self.memoria.append(registro)
    

    #======================================================
    #                     EJECUCIÓN
    #======================================================
    def run(self):

        for ciclo in range(1, 11):
            print(ciclo)

            temperatura = self.percibir()
            accion = self.decidir(temperatura)
            self.ejecutar(accion)
            self.recordar(accion)

            time.sleep(1)


#======================================================
#                     PROGRAMA
#======================================================

agente = AgenteTemperatura(temperatura_objetivo=22)
agente.run()


