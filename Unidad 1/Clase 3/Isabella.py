from tkinter import Frame, Tk
from tkinter.messagebox import  askyesno

ventana = Tk()
ventana.title("isabella y jhon")

def digitar_letra(event):
    print("digitaste la letra",repr(event.char))

def click_izquierdo(event):
    frame.focus_set()
    print("clikeado en: ",event.x,event.y)


frame = Frame(ventana, width=500, height=500)
frame.bind("<Key>", digitar_letra)
frame.bind("<Button-1>", click_izquierdo)
frame.pack()
frame.focus_set()



ventana.mainloop()


