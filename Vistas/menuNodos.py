from cProfile import label
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QGridLayout)

class MenuNodos(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('TJ')
		self.resize(500, 200)

		layout = QGridLayout()

		button_nodoC = QPushButton('Nodo central')
		#button_nodo.clicked.connect(self.printDatos)
		layout.addWidget(button_nodoC, 2, 0, 1, 2)
		  
		button_nodoL = QPushButton('Nodos locales')
        #button_nodoL.clicked.connect(self.printDatos)
		layout.addWidget(button_nodoL, 3, 0, 1, 2)

		button_menu = QPushButton('Volver al menu')
		#button_menu.clicked.connect(self.printDatos)
		layout.addWidget(button_menu, 4, 0, 1, 2)    

		self.setLayout(layout)


if __name__ == '__main__':
	app = QApplication(sys.argv)

	vista = MenuNodos()
	vista.show()

	sys.exit(app.exec_())