import json
import sys
from PyQt5.QtWidgets import (QComboBox,QCheckBox ,QGridLayout,QGroupBox,QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout)
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

class Segmentacion(QWidget):
	def __init__(self):

		tipoDato=['int','varchar','boolean','date']

		super().__init__()
		self.setWindowTitle('TJ')
		self.resize(500, 200)

		posicion = 1

		layout = QGridLayout()

		label_tabla = QLabel('<font size="4"> Nombre: </font>')
		self.txt_anfitrion = QLineEdit()
		self.txt_anfitrion.setPlaceholderText('Nombre de tabla')
		layout.addWidget(label_tabla, 0, 0)
		layout.addWidget(self.txt_anfitrion, 0, 1)

		fieldGroup = QGroupBox("Atributos")
		fieldGroup.setFlat(True)

		box = QGridLayout()

		#labels dentro del group
		label_nombre = QLabel('<font size="4"> Nombre </font>')
		label_tipo = QLabel('<font size="4"> Tipo de dato </font>')
		label_null = QLabel('<font size="4"> null </font>')
		label_pk = QLabel('<font size="4"> pk </font>')

		box.addWidget(label_nombre, 0,0)
		box.addWidget(label_tipo, 0,1)
		box.addWidget(label_null, 0,2)
		box.addWidget(label_pk, 0,3)

		self.arrayCheckBoxsPKs= []
		self.arrayTxtAtributos = []
		self.arrayCbxTipos = []
		self.arrayCheckBoxsNulls = []

		def agregar(posicion):
			self.txt_atributo = QLineEdit()
			self.arrayTxtAtributos.append(self.txt_atributo)
			self.cbx_tipo = QComboBox()
			for x in tipoDato:
				self.cbx_tipo.addItem(x)
			self.arrayCbxTipos.append(self.cbx_tipo)
			self.chk_null = QCheckBox ()
			self.arrayCheckBoxsNulls.append(self.chk_null)
			self.rdb_pk = QCheckBox ()
			self.arrayCheckBoxsPKs.append(self.rdb_pk)

			box.addWidget(self.txt_atributo,posicion,0)
			box.addWidget(self.cbx_tipo,posicion,1)
			box.addWidget(self.chk_null,posicion,2)
			box.addWidget(self.rdb_pk,posicion,3)

			posicion = posicion +1

			self.txt_atributo.returnPressed.connect(lambda: agregar(posicion))

			return posicion

			

		agregar(posicion)

		fieldGroup.setLayout(box)

		layout.addWidget(fieldGroup, 1, 0,1,2)


		button_siguiente = QPushButton('Siguiente')
		button_siguiente.clicked.connect(self.mandarDatos)
		layout.addWidget(button_siguiente, 3, 1, 1, 1)  

		button_cancelar = QPushButton('Cancelar')
		#button_cancelar.clicked.connect(self.printDatos)
		layout.addWidget(button_cancelar, 3, 0, 1, 1) 
		
		self.setLayout(layout)

		

	def mandarDatos(self):
		templateTable={"name":"","attributes":{}}
		templateAttribute=[]
		templateTable["name"]=self.txt_anfitrion.text()
		for x in range (len(self.arrayTxtAtributos)):
			templateAttribute.append({"name":self.arrayTxtAtributos[x].text(),"type":self.arrayCbxTipos[x].currentText(),"pk":self.arrayCheckBoxsPKs[x].isChecked(),"null":self.arrayCheckBoxsNulls[x].isChecked()})
		templateTable["attributes"]=templateAttribute
		self.saveData(templateTable)
	
	def saveData(self,newData):
		jsonData = json.dumps(newData)
		configuracion = open('segmentacion.json','w')
		configuracion.write(jsonData)
		configuracion.close()
		
			

					

if __name__ == '__main__':
	app = QApplication(sys.argv)

	vista = Segmentacion()
	vista.show()

	sys.exit(app.exec_())