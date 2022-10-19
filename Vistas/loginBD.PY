from cProfile import label
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout)

class LoginBD(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('TJ')
		self.resize(500, 200)

		layout = QGridLayout()

		label_nombre = QLabel('<font size="4"> Nombre Logico: </font>')
		self.txt_nombre = QLineEdit()
		self.txt_nombre.setPlaceholderText('Nombre logico del nodo')
		layout.addWidget(label_nombre, 0, 0)
		layout.addWidget(self.txt_nombre, 0, 1)

		label_anfitrion = QLabel('<font size="4"> Anfitrion: </font>')
		self.txt_anfitrion = QLineEdit()
		self.txt_anfitrion.setPlaceholderText('Nombre de anfitrion')
		layout.addWidget(label_anfitrion, 1, 0)
		layout.addWidget(self.txt_anfitrion, 1, 1)

		label_db= QLabel('<font size="4"> Base de Datos: </font>')
		self.txt_db = QLineEdit()
		self.txt_db.setPlaceholderText('Nombre de base de datos')
		layout.addWidget(label_db, 2, 0)
		layout.addWidget(self.txt_db, 2, 1)

		label_usuario = QLabel('<font size="4"> Usuario: </font>')
		self.txt_usuario  = QLineEdit()
		self.txt_usuario .setPlaceholderText('Nombre de usuario')
		layout.addWidget(label_usuario , 3, 0)
		layout.addWidget(self.txt_usuario , 3, 1)

		label_puerto = QLabel('<font size="4"> Puerto: </font>')
		self.txt_puerto  = QLineEdit()
		self.txt_puerto .setPlaceholderText('Numero de puerto')
		layout.addWidget(label_puerto , 4, 0)
		layout.addWidget(self.txt_puerto , 4, 1)

		label_clave = QLabel('<font size="4"> Clave: </font>')
		self.txt_clave  = QLineEdit()
		self.txt_clave .setPlaceholderText('Numero de clave')
		layout.addWidget(label_clave , 5, 0)
		layout.addWidget(self.txt_clave , 5, 1)

		button_login = QPushButton('Conectar')
		button_login.clicked.connect(self.printDatos)
		layout.addWidget(button_login, 6, 0, 1, 2)
		

		self.setLayout(layout)

	def printDatos (self):
		Datos = {
		"Anfitrion:": self.txt_anfitrion.text(),
		"Base de datos": self.txt_db.text(),
		"Usuario ": self.txt_usuario.text(),
		"Puerto ": self.txt_puerto.text(),
		"Clave ": self.txt_clave.text()
		}
		print(Datos)

if __name__ == '__main__':
	app = QApplication(sys.argv)

	vista = LoginBD()
	vista.show()

	sys.exit(app.exec_())