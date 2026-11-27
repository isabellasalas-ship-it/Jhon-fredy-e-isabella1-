import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


class HiloConsulta(threading.Thread):

    def __init__(self, nombre_hilo, nombre_persona):
        super().__init__(name=nombre_hilo)
        self.nombre_persona = nombre_persona
        self.resultado = None

    def run(self):
        logging.debug('Consultando: ' + self.nombre_persona)
        time.sleep(3)
        self.resultado = self.nombre_persona + ' tiene 3 asignaturas'


hilo = HiloConsulta('hilo_consulta', 'Raúl')
hilo.start()
logging.debug('El hilo principal sigue trabajando')
hilo.join()
logging.debug('Resultado: ' + hilo.resultado)
