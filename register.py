from operator import itemgetter
import os

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
        updateCentral(createNode())
        return

    print(f"Datos actuales:\nNodo: {name}\nMotor: {motor}\nHost: {host}\nDatabase: {database}\nPort: {port}\nUsername: {user}\nPassword: XXXXXXXXX")
    
    opt = input("Desea cambiar los datos del nodo central? y/n: ").lower()

    menuCentral = "1.Nombre\n2.Host\n3.Database\n4.Port\n5.Username\n6.Password\n7.Salir\n"

    if (opt == 'y' or opt == 'ye' or opt == 'yes'):
        while True:
            os.system('cls')
            mcOpt = input(menuCentral)
            os.system('cls')
            match(mcOpt):
                case "1": name = input("Nombre: ")
                case "2": host = input("Host: ")
                case "3": database = input("Database: ")
                case "4": 
                    while True:
                        try:
                            port = int(input("Port:"))
                            break
                        except ValueError:
                            pass
                case "5": user = input("Username: ")
                case "6": password = input("Password: ")
                case "7": break

        params = {"name" : name, "host" : host, "database" : database, "port" : port, "user" : user, "password" : password }
        updateCentral(params)

def deleteNodes():
    _, locals = getNodes()

    print("Nodos:")
    for node in locals:
        print(f"{node['name']}")

    node = input("Nombre del nodo a borrar: ")
    removeLocal(node)  
    
def locals():
    menuLocals = "1.Nuevo nodo\n2.Borrar nodos\n3.Salir\n"

    while True:
        os.system('cls')
        opt = input(menuLocals)
        os.system('cls')
        match(opt):
            case "1": newLocal(createNode())
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
            case other: pass