import json
import sys
from PyQt5.QtWidgets import (QLabel,QVBoxLayout,QComboBox , QGroupBox, QApplication, QWidget, QPushButton, QCheckBox, QGridLayout)

class Horizontal(QWidget):
	def __init__(self):

		jsonData=self.getData()
		self.nodosLocales=jsonData["NodosLocales"]
		self.tablas=jsonData["Tablas"]

		super().__init__()
		self.setWindowTitle('TJ')
		self.resize(500, 200)

		layout = QGridLayout()

		fieldGroup = QGroupBox("Atributos")
		fieldGroup.setFlat(True)

		vbox = QVBoxLayout()

		layout.addWidget(fieldGroup, 0, 0)

		self.arrayComboBoxs = []

		for x in self.tablas:
			label_nodo = QLabel(x)
			nodo = QComboBox()
			for y in self.nodosLocales:
				nodo.addItem(y)
			self.arrayComboBoxs.append(nodo)
			vbox.addWidget(label_nodo)
			vbox.addWidget(nodo)
		
		vbox.addStretch(1)
		fieldGroup.setLayout(vbox)

		button_segmentar = QPushButton('Segmentar')
		button_segmentar.clicked.connect(self.mandarDatos)
		layout.addWidget(button_segmentar, 3, 1, 1, 1)  

		button_volver = QPushButton('Volver')
		#button_volder.clicked.connect(self.printDatos)
		layout.addWidget(button_volver, 3, 0, 1, 1)   

		self.setLayout(layout)
	
	def getData(self):
		jsonData=open('data.json','r')
		data =json.load(jsonData)
		jsonData.close()
		return data
	
	def saveData(self,newData):
		jsonData = json.dumps(newData)
		configuracion = open('data.json','w')
		configuracion.write(jsonData)
		configuracion.close()
	
	def mandarDatos(self):
		configuracion={}
		json= self.getData()
		for x in range (len(self.tablas)):
			nodoAcutual = self.arrayComboBoxs[x]
			tabla = {self.tablas[x]:nodoAcutual.currentText()}
			configuracion.update(tabla)
		json["Horizontal"]=configuracion
		self.saveData(json)

if __name__ == '__main__':
	app = QApplication(sys.argv)

	vista = Horizontal()
	vista.show()

	sys.exit(app.exec_())