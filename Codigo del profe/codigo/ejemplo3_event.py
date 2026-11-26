import threading
import time


class Cronometro(threading.Thread):

    def __init__(self, evento_parar):
        super().__init__()
        self.evento_parar = evento_parar

    def run(self):
        segundos = 0
        while not self.evento_parar.is_set():
            print('Segundos:', segundos)
            segundos += 1
            self.evento_parar.wait(1)
        print('Cronómetro detenido.')


evento_parar = threading.Event()
cronometro = Cronometro(evento_parar)
cronometro.start()

time.sleep(5)
evento_parar.set()
cronometro.join()
print('Programa terminado.')
