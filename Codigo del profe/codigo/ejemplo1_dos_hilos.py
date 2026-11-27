import logging
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')


def numeros():
    for numero in [1, 2, 3, 4, 5]:
        logging.debug(numero)
        time.sleep(1)


def letras():
    for letra in ['a', 'b', 'c', 'd', 'e']:
        logging.debug(letra)
        time.sleep(2)


def consultar(nombre):
    logging.debug('Consultando: ' + nombre)
    time.sleep(5)
    logging.debug('Consulta terminada')


inicio = time.time()

hilo_1 = threading.Thread(name='hilo_1', target=numeros)
hilo_2 = threading.Thread(name='hilo_2', target=letras)
hilo_3 = threading.Thread(name='hilo_3', target=consultar, args=('Raúl',))

hilo_1.start()
hilo_2.start()
hilo_3.start()

hilo_1.join()
hilo_2.join()
hilo_3.join()

logging.debug('Tiempo transcurrido: %.1f segundos', time.time() - inicio)
