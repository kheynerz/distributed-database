import json
import os


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
    json_central, json_locals = getNodes()
    nodos=[json_central["name"]]

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
    createTable()

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