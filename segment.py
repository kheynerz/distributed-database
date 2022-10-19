import os
from nodos import getNodes
menu = "1.Vertical\n2.Horizontal\n3.Mixta\n4.Salir\n"

def createTable():
    tableName = input("Nombre de tabla: ")
    opt = 'y'

    dataTypes = ['INTEGER','VARCHAR','FLOAT','DATE']

    attributtes = []

    while (opt == 'y' or opt == 'ye' or opt == 'yes'):
        os.system('cls')
        print("Atributo:")
        name = input("Nombre: ")

        while True:
            try:
                dt = int(input("1.Integer\n2.Varchar\n3.Float\n4.Date\n"))
                print(dt)
                if (1 <= dt <= 4): break
            except ValueError as err:
                print(err)
                pass
        
        isPk = input("Es llave primaria? y/n: ")
        pk = True if (isPk == 'y' or isPk == 'ye' or isPk == 'yes') else False

        isNull = input("Puede ser Null? y/n: ")
        null = True if (isNull == 'y' or isNull == 'ye' or isNull == 'yes') else False
    

        attributtes.append({"nombre": name,"tipo": dataTypes[dt-1],"pk": pk,"null": null})
        opt = input("Continuar y/n")

    return tableName, attributtes

def chooseNodes():
    _, json_locals = getNodes()
    nodos=[]
    for x in json_locals:
        addNode=input("Segmentar en la tabla: "+x["name"]+" y/n?")
        option = True if (addNode == 'y' or addNode == 'ye' or addNode == 'yes') else False
        if option:
            nodos.append(x["name"])
    
    return nodos
    

def vertical():
    createTable()
    chooseNodes()

def horizontal():
    attributes = [{"nombre": "cedula", "tipo" : "varchar", "pk" : True, "null" : False },
                {"nombre": "nombre", "tipo" : "varchar", "pk" : False, "null" : False },
                {"nombre": "ape1", "tipo" : "varchar", "pk" : False, "null" : False },
                {"nombre": "ape2", "tipo" : "varchar", "pk" : False, "null" : False }]
    tableName = "personas"        #createTable()

    nodes = chooseNodes()
    centralNode, _ = getNodes()

    json = {"name": tableName}    

    central = {"name" : centralNode['name'], "attributes": []}
    locals = []

    for node in nodes:
        locals.append({"name": node, "attributes": []})

    for a in attributes:
        if (a['pk']):
            central["attributes"].append(a)
            for node in locals:
                node["attributes"].append(a)
            continue

        os.system('cls')
        print("Nodos: ")
        print(central["name"])
        for x in nodes:
            print(x)
            
        while True:
            node = input(f'Digite el nodo para el atributo "{a["nombre"]}" de tipo {a["tipo"]}: ')
            if (node in nodes) or (node == central["name"]): break
        if node == central["name"]:
            central["attributes"].append(a)
            continue

        for x in locals:
            if  x["name"] == node:
                x["attributes"].append(a)

    json["central"] = central
    json["locals"] = locals

    input(json)
def mix():
    createTable()

def segmentMain():
    while True:
        os.system('cls')
        opt = input(menu)
        os.system('cls')
        match(opt):
            case "1": vertical()
            case "2": horizontal()
            case "3": mix()
            case "4": break
            case other: pass