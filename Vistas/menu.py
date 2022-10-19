from cProfile import label
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QGridLayout)

class Menu(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('TJ')
		self.resize(500, 200)

		layout = QGridLayout()

		button_nodo = QPushButton('Registrar Nodos')
		#button_nodo.clicked.connect(self.printDatos)
		layout.addWidget(button_nodo, 2, 0, 1, 2)
        
		button_tabla = QPushButton('Crear tabla y segmentar')
        #button_tabla.clicked.connect(self.printDatos)
		layout.addWidget(button_tabla, 3, 0, 1, 2)

		self.setLayout(layout)


if __name__ == '__main__':
	app = QApplication(sys.argv)

	vista= Menu()
	vista.show()

	sys.exit(app.exec_())