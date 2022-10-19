from cProfile import label
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QGridLayout)

class MenuSegmentacion(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('TJ')
		self.resize(500, 200)

		layout = QGridLayout()

		button_horizontal = QPushButton('Segmentacion horizontal')
		#button_horizontal.clicked.connect(self.printDatos)
		layout.addWidget(button_horizontal, 2, 0, 1, 2)
        
		button_vertical = QPushButton('Segmentacion vertical')
        #button_vertical.clicked.connect(self.printDatos)
		layout.addWidget(button_vertical, 3, 0, 1, 2)

		button_hibrida = QPushButton('Segmentacion hibrida')
		#button_hibrida.clicked.connect(self.printDatos)
		layout.addWidget(button_hibrida, 4, 0, 1, 2)

		button_menu = QPushButton('Volver al menu')
		#button_menu.clicked.connect(self.printDatos)
		layout.addWidget(button_menu, 5, 0, 1, 2)    

		self.setLayout(layout)


if __name__ == '__main__':
	app = QApplication(sys.argv)

	vista = MenuSegmentacion()
	vista.show()

	sys.exit(app.exec_())