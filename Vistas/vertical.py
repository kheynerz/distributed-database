import json
import sys
from PyQt5.QtWidgets import (QVBoxLayout,QCheckBox , QGroupBox, QApplication, QWidget, QPushButton, QCheckBox, QGridLayout)

class Vertical(QWidget):
	def __init__(self):

		jsonData=self.getData()
		self.nodosLocales=jsonData["NodosLocales"]

		super().__init__()
		self.setWindowTitle('TJ')
		self.resize(500, 200)

		layout = QGridLayout()

		fieldGroup = QGroupBox("Nodos Locales")
		fieldGroup.setFlat(True)

		vbox = QVBoxLayout()

		layout.addWidget(fieldGroup, 1, 0,1,2)

		self.arrayCheckBoxs = []

		for x in self.nodosLocales:
			nodo = QCheckBox(x)
			self.arrayCheckBoxs.append(nodo)
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
	
	def getData(self) :
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
		for x in range (len(self.nodosLocales)):
			nodoAcutual = self.arrayCheckBoxs[x]
			tabla = {self.nodosLocales[x]:nodoAcutual.isChecked()}
			configuracion.update(tabla)
		json["Vertical"]=configuracion
		print(json)
		self.saveData(json)


if __name__ == '__main__':
	app = QApplication(sys.argv)

	vista = Vertical()
	vista.show()

	sys.exit(app.exec_())