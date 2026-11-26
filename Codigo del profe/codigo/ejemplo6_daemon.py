import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


class HiloInfinito(threading.Thread):

    def __init__(self, nombre_hilo, daemon):
        super().__init__(name=nombre_hilo, daemon=daemon)

    def run(self):
        while True:
            logging.debug('Esto se escribe infinitamente')
            time.sleep(1)


hilo = HiloInfinito('hilo_infinito', daemon=True)
hilo.start()

time.sleep(3)
logging.debug('El hilo principal terminó')
