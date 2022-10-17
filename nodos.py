import json
from operator import itemgetter

def getNodes() -> tuple:
    nodos = open('nodos.json', 'r')
    data = json.load(nodos)
    nodos.close()
    return data['central'], data['locals']

def saveNodes(newData) -> None:
    jsonData = json.dumps(newData)
    nodos = open("nodos.json", "w")
    nodos.write(jsonData)
    nodos.close()

def checkData(data : dict) -> bool:
    try:
        itemgetter('name','host', 'database', 'port', 'user', 'password')(data)
    except KeyError:
        print("ERROR")    
        return False
    return True


def updateCentral(newCentral: dict) -> None:
    if not checkData(newCentral): return

    _,  locals = getNodes()
    newData = {"central": newCentral, "locals": locals}
    saveNodes(newData)

def newLocal(data: dict) -> bool: 
    if not checkData(data): return

    central,  locals = getNodes()

    for node in locals:
        if node['name'] == data['name']:
            return False

    locals.append(data)
    newData = {"central": central, "locals": locals}
    saveNodes(newData)

    return True

def removeLocal(name: str) -> bool:
    central,  locals = getNodes()
    deleted = False
    for i, node in enumerate(locals):
        if node['name'] == name:
            locals.pop(i)
            deleted = True
            break

    if not deleted: return False

    newData = {"central": central, "locals": locals}
    saveNodes(newData)

    return True

def getParams(name):
    central, locals = getNodes()
    if name == central['name']: return central
    for node in locals:
        if node['name'] == name: return node








#updateCentral({"name": "INSTANCIA 1", "host": "localhost", "database": "postgres", "port": 5433, "user": "postgres", "password": "1234"})



#print(removeLocal('INSTANCIA 2'))

#newLocal({"name": "INSTANCIA 2", "host": "localhost", "database": "postgres", "port": 5434, "user": "postgres", "password": "1234"})
newLocal({"name": "INSTANCIA 3", "host": "localhost", "database": "postgres", "port": 5435, "user": "postgres", "password": "1234"})