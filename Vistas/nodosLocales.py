from cProfile import label
import sys
from PyQt5.QtWidgets import (QVBoxLayout,QCheckBox , QGroupBox, QApplication, QWidget, QPushButton, QCheckBox, QGridLayout)

class NodosLocales(QWidget):
	def __init__(self):

		nodosLocales=['con leche','arroz','chompipe','eeee','sss','dddd','aaa','dadw']

		super().__init__()
		self.setWindowTitle('TJ')
		self.resize(500, 200)

		layout = QGridLayout()

		fieldGroup = QGroupBox("Nodos Locales")
		fieldGroup.setFlat(True)

		vbox = QVBoxLayout()

		layout.addWidget(fieldGroup, 0, 0)

		for x in nodosLocales:
			label_nodo = QCheckBox(x)
			vbox.addWidget(label_nodo)
		
		button_eliminar = QPushButton('Eliminar')
		#button_nuevoNodo.clicked.connect(self.printDatos)
		vbox.addWidget(button_eliminar)  

		vbox.addStretch(1)
		fieldGroup.setLayout(vbox)

		button_nuevoNodo = QPushButton('Nuevo nodo local')
		#button_nuevoNodo.clicked.connect(self.printDatos)
		layout.addWidget(button_nuevoNodo, 3, 1, 1, 1)  

		button_volver = QPushButton('Volver')
		#button_volder.clicked.connect(self.printDatos)
		layout.addWidget(button_volver, 3, 0, 1, 1)   

		self.setLayout(layout)

if __name__ == '__main__':
	app = QApplication(sys.argv)

	vista = NodosLocales()
	vista.show()

	sys.exit(app.exec_())