import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DrawRegions(QWidget):

	def __init__(self):
		super(DrawRegions,self).__init__()
		self.initUI()
		self.spaceArray=[]

	def initUI(self):
		self.setFixedSize(500,500)
		self.setWindowTitle("DrawRegions")
		self.show()

	def paintEvent(self,event):
		paint=QPainter()
		paint.begin(self)
		self.drawSpace(paint)
		paint.end()

	def keyPressEvent(self,event):
		if event.key()==Qt.Key_Escape:
			self.close()

	def drawSpace(self,paint):
		paint.setPen(Qt.NoPen)
		paint.setBrush(QColor(255,0,0,125))
		for coor in self.spaceArray:
			paint.drawRect(coor[0],coor[1],12,12)

	def mousePressEvent(self,event):
		self.x=event.pos().x()
		self.y=event.pos().y()
		if self.notRepeat(self.x,self.y):
			self.spaceArray.insert(0,[self.x,self.y])
			self.repaint()
			# self.update()

	def notRepeat(self,x,y):
		for i in self.spaceArray:
			if (i[0] == x) and (i[1]==y):
				return False
		return True

def main():        
    app=QApplication(sys.argv)
    ex=DrawRegions()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()		

