from nodos import checkCentral
from register import registerNodes
from segment import segmentMain

import os

menu1 = "1.Registrar Nodos\n2.Crear tabla y segmentar\n3.Salir\n"

def main():
    err = ""
    while True:
        os.system('cls')
        if err != "":
            print(err)
        err = ""
        opt = input(menu1)
        match(opt):
            case "1": registerNodes()
            case "2": 
                if(checkCentral()):
                    segmentMain()
                else:
                    err = "Tiene que registrar al menos el nodo central\n"
            case "3": break
            case other: pass

    print("BYE")


if __name__ == "__main__":
    main()