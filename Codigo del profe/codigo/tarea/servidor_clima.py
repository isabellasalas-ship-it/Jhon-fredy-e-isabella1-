import random
import time
from datetime import datetime

CIUDADES = ['Caicedonia', 'Sevilla', 'Tuluá', 'Armenia', 'Cali']

PROBABILIDAD_FALLA = 0.2


class ServidorCaido(Exception):
    pass


def consultar_clima(ciudad):
    time.sleep(random.uniform(1, 4))
    if random.random() < PROBABILIDAD_FALLA:
        raise ServidorCaido('El servidor del clima no respondió al consultar ' + ciudad + '.')
    return {
        'hora': datetime.now().strftime('%H:%M:%S'),
        'ciudad': ciudad,
        'temperatura': round(random.uniform(17, 33), 1),
        'humedad': random.randint(40, 95),
    }
