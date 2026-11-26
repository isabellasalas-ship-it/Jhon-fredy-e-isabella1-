import queue
import threading
import time


class Productor(threading.Thread):

    def __init__(self, cola):
        super().__init__()
        self.cola = cola

    def run(self):
        for numero in range(5):
            print('Produciendo', numero)
            self.cola.put(numero)
            time.sleep(1)
        self.cola.put(None)


class Consumidor(threading.Thread):

    def __init__(self, cola):
        super().__init__()
        self.cola = cola

    def run(self):
        while True:
            dato = self.cola.get()
            if dato is None:
                break
            print('Consumido:', dato)


cola = queue.Queue()
productor = Productor(cola)
consumidor = Consumidor(cola)

productor.start()
consumidor.start()
productor.join()
consumidor.join()
print('Terminado.')
