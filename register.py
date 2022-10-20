
from cgitb import text
from operator import itemgetter
import os
from connection import createExtension, createServer

from nodos import checkCentral, getNodes, newLocal, removeLocal, updateCentral

menu = "1.Nodo central\n2.Nodos locales\n3.Salir\n"

def createNode():
    name = input("Nombre del nodo:")
    motor = ""
    while (motor != "1" and motor != "2"):
        motor = input("Motor de BD\n1.PostgreSQL\n2.Sql Server\n")
    host = input("Host:")
    database = input("Database:")
    
    while True:
        try:
            port = int(input("Port:"))
            break
        except ValueError:
            pass

    user = input("Username:")
    password = input("Password:")

    motor = "PostgreSQL" if (motor == "1") else "Sql Server"
    params = {"name" : name, "host" : host, "database" : database, "port" : port, "user" : user, "password" : password }
    return params

def central():
    os.system('cls')
    central, _ = getNodes()
    try:
        name, host, database, port, user, password = itemgetter('name','host', 'database', 'port', 'user', 'password')(central)
        motor = "PostgreSQL"
    except KeyError:
        print("ERROR")    
        return False

    if (not checkCentral()):
        params = createNode()
        result, err = createExtension(params)

        text = "Conexion Exitosa..." if result else "Credenciales incorrectas..."
        if result:
            updateCentral(params)
        input(text)
        return

    print(f"Datos actuales:\nNodo: {name}\nMotor: {motor}\nHost: {host}\nDatabase: {database}\nPort: {port}\nUsername: {user}\nPassword: XXXXXXXXX")
    opt = input("Desea restablecer los datos del nodo central? y/n: ").lower()

    if (opt == 'y' or opt == 'ye' or opt == 'yes'):
        params = {"name" : "", "host" : "", "database" : "", "port" : 0, "user" : "", "password" : "" }
        updateCentral(params)
        
def deleteNodes():
    _, locals = getNodes()

    print("Nodos:")
    for node in locals:
        print(f"{node['name']}")

    node = input("Nombre del nodo a borrar: ")
    removeLocal(node)  
    
def createNewLocal():
    params = createNode()
    result, err = createExtension(params)
    text = "Conexion Exitosa..." if result else "Credenciales incorrectas..."
    if result:
        central, _ = getNodes()

        newLocal(params)
        createServer(params, central['name'])
        createServer(central, params['name'])


    input(text)
    return

def locals():
    menuLocals = "1.Nuevo nodo\n2.Borrar nodos\n3.Salir\n"

    while True:
        os.system('cls')
        opt = input(menuLocals)
        os.system('cls')
        match(opt):
            case "1": createNewLocal()
            case "2": deleteNodes()
            case "3": break

def registerNodes():
    while True:
        os.system('cls')
        opt = input(menu)
        match(opt):
            case "1": central()
            case "2": locals()
            case "3": break
