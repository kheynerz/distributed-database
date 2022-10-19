from nodos import checkCentral
from register import registerNodes
from segment import segmentMain

import os

menu1 = "1.Registrar Nodos\n2.Crear tabla y segmentar\n3.Salir\n"

def main():
    while True:
        os.system('cls')
        opt = input(menu1)
        match(opt):
            case "1": registerNodes()
            case "2": 
                if(checkCentral()):
                    segmentMain()
                else:
                    print("Tiene que registrar al menos el nodo central")
            case "3": break
            case other: pass

    print("BYE")


if __name__ == "__main__":
    main()