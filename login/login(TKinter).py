from tkinter import *
from functools import partial

def validateLogin(anfitrion, db, usuario, puerto, clave):
	Datos = {
		"Anfitrion:": anfitrion.get(),
		"Base de datos": db.get(),
		"Usuario ": usuario.get(),
		"Puerto ": puerto.get(),
		"Clave ": clave.get()
	}
	print(Datos)
	return

#ventana
tkWindow = Tk()  
tkWindow.geometry('250x150')  
tkWindow.title('distributed_database')

#Anfitrion 
anfitrionLabel = Label(tkWindow, text="Anfitrion").grid(row=0, column=0)
anfitrion = StringVar()
anfitrionEntry = Entry(tkWindow, textvariable=anfitrion).grid(row=0, column=1)  

#Data Base
dbLabel = Label(tkWindow, text="Base de datos").grid(row=1, column=0)
db = StringVar()
dbEntry = Entry(tkWindow, textvariable=db).grid(row=1, column=1)

#Usuario
usuarioLabel = Label(tkWindow, text="Usuario").grid(row=2, column=0)
usuario = StringVar()
usuarioEntry = Entry(tkWindow, textvariable=usuario).grid(row=2, column=1)

#Puerto 
puertoLabel = Label(tkWindow, text="Puerto").grid(row=3, column=0)
puerto = StringVar()
puertoEntry = Entry(tkWindow, textvariable=puerto).grid(row=3, column=1)

#Clave 
claveLabel = Label(tkWindow, text="Clave").grid(row=4, column=0)
clave = StringVar()
claveEntry = Entry(tkWindow, textvariable=clave, show='*').grid(row=4, column=1)



validateLogin = partial(validateLogin, anfitrion, db, usuario, puerto, clave)

#login button
loginButton = Button(tkWindow, text="Connect", command=validateLogin).grid(row=5, column=1)  

tkWindow.mainloop()


