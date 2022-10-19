import json
import sys
from PyQt5.QtWidgets import (QLabel,QVBoxLayout,QComboBox , QGroupBox, QApplication, QWidget, QPushButton, QGridLayout)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QStandardItem

class CheckableComboBox(QComboBox):
	def __init__(self):
		super().__init__()
		self.setEditable(True)
		self.lineEdit().setReadOnly(True)
		self.closeOnLineEditClick =False

		self.lineEdit().installEventFilter(self)

		self.view().viewport().installEventFilter(self)

		self.model().dataChanged.connect(self.updateLineEditField)

	def eventFilter(self, widget,event):
		if widget == self.lineEdit():
			if event.type() == QEvent.MouseButtonRelease:
				if self.closeOnLineEditClick:
					self.hidePopup() #TODO
				else:
					self.showPopup()
				return True	
			return super().eventFilter(widget,event)

		if widget == self.view().viewport():
			if event.type() == QEvent.MouseButtonRelease:
				indx = self.view().indexAt(event.pos())
				item = self.model().item(indx.row())

				if item.checkState() == Qt.Checked:
					item.setCheckState(Qt.Unchecked)
				else:
					item.setCheckState(Qt.Checked)
				return True
			return super().eventFilter(widget,event)

	def hidePopup(self):
		super().hidePopup()
		self.startTimer(100)
	
	def addItems(self,items, itemList=None):
		for indx, text in enumerate(items):
			try:
				data=itemList[indx]
			except(TypeError,IndexError):
				data=None
			self.addItem(text,data)

	def addItem(self,text,userData=None):
		item = QStandardItem()
		item.setText(text)
		if not userData is None:
			item.setData(userData)
		
		#enable checkbox setting
		item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
		item.setData(Qt.Unchecked, Qt.CheckStateRole)
		self.model().appendRow(item)

	def updateLineEditField(self):
		text_container = []
		for i in range(self.model().rowCount()):
			if self.model().item(i).checkState() == Qt.Checked:
				text_container.append(self.model().item(i).text())
		text_string = ', '.join(text_container)
		self.lineEdit().setText(text_string)


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

		for x in range (len(self.tablas)):
			label_nodo = QLabel(self.tablas[x])
			self.nodo = CheckableComboBox()
			self.nodo.addItems(self.nodosLocales)
			self.arrayComboBoxs.append(self.nodo)
			vbox.addWidget(label_nodo)
			vbox.addWidget(self.nodo)
			self.nodo.setEditText('| Todos |')
		
		for x in self.arrayComboBoxs:
			print(x)
		
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

	def	mandarDatos(self):
		configuracion={}
		json= self.getData()
		for x in range (len(self.tablas)):
			nodoAcutual = self.arrayComboBoxs[x]
			tabla = {self.tablas[x]:nodoAcutual.currentText()}
			configuracion.update(tabla)
		json["Mixta"]=configuracion
		self.saveData(json) 
	

if __name__ == '__main__':
	app = QApplication(sys.argv)

	vista = Horizontal()
	vista.show()

	sys.exit(app.exec_())