import threading
import time

contador = 0


class Incrementador(threading.Thread):

    def __init__(self, repeticiones):
        super().__init__()
        self.repeticiones = repeticiones

    def run(self):
        global contador
        for _ in range(self.repeticiones):
            valor = contador
            time.sleep(0)
            contador = valor + 1


hilos = [Incrementador(1000) for _ in range(4)]
for hilo in hilos:
    hilo.start()
for hilo in hilos:
    hilo.join()

print('Esperado: 4000')
print('Obtenido:', contador)
