import sys
from PyQt5.QtWidgets import QComboBox, QPushButton,QApplication, QWidget,QHBoxLayout,QVBoxLayout
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

class Mixta(QWidget):

	nodosLocales=['con leche','arroz','chompipe','eeee','sss','dddd','aaa','dadw','todos']
	tablas=['pellejo','perro']

	def printDatos(self):
		print(self.combobox.currentText())

	def __init__(self):
		super().__init__()
		self.setWindowTitle('TJ')
		self.resize(500, 200)

		nodosLocales=['con leche','arroz','chompipe','eeee','sss','dddd','aaa','dadw','todos']
		tablas=['pellejo','perro']

		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		self.combobox = CheckableComboBox()
		self.combobox.addItems(nodosLocales)
		self.layout.addWidget(self.combobox)

		btn = QPushButton('Ver data')
		btn.clicked.connect(self.printDatos)
		self.layout.addWidget(btn)
	

if __name__ == '__main__':

	
	app = QApplication(sys.argv)

	vista = Mixta()
	vista.show()

	sys.exit(app.exec_())