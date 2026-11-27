import queue
import threading
import time
import tkinter as tk


class Ventana():

    def __init__(self):
        self.ventana = tk.Tk()
        self.cola = queue.Queue()
        self.segundos = 0

    def consulta_lenta(self):
        time.sleep(5)
        return 'Llegaron los datos'

    def accion_sin_hilo(self):
        self.label_resultado.config(text=self.consulta_lenta())

    def accion_con_hilo(self):
        self.label_resultado.config(text='Consultando…')
        hilo = threading.Thread(target=self.trabajo_del_hilo, daemon=True)
        hilo.start()

    def trabajo_del_hilo(self):
        self.cola.put(self.consulta_lenta())

    def revisar_cola(self):
        try:
            resultado = self.cola.get_nowait()
        except queue.Empty:
            pass
        else:
            self.label_resultado.config(text=resultado)
        self.ventana.after(100, self.revisar_cola)

    def contar(self):
        self.segundos += 1
        self.label_reloj.config(text='Segundos: ' + str(self.segundos))
        self.ventana.after(1000, self.contar)

    def mostrar(self):
        self.ventana.title('¿Se congela?')
        self.ventana.geometry('320x200')

        self.label_reloj = tk.Label(self.ventana, text='Segundos: 0', font=('Segoe UI', 14))
        boton_sin_hilo = tk.Button(self.ventana, text='Consultar sin hilo', command=self.accion_sin_hilo)
        boton_con_hilo = tk.Button(self.ventana, text='Consultar con hilo', command=self.accion_con_hilo)
        self.label_resultado = tk.Label(self.ventana, text='')

        self.label_reloj.pack(pady=10)
        boton_sin_hilo.pack(pady=4)
        boton_con_hilo.pack(pady=4)
        self.label_resultado.pack(pady=10)

        self.contar()
        self.revisar_cola()
        self.ventana.mainloop()


if __name__ == '__main__':
    Ventana().mostrar()
