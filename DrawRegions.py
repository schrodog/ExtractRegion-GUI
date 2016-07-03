import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DrawRegions(QGraphicsPixmapItem):

	def __init__(self,pixmap=None,parent=None,scene=None):
		super(DrawRegions,self).__init__()
		self.spaceArray=[]

	def paint(self,painter,options,widget=None):
		painter.drawPixmap(0,0,self.pixmap())

		radius=30
		painter.setPen(Qt.NoPen)
		painter.setBrush(QColor(255,0,0,125))
		for coor in self.spaceArray:
			painter.drawEllipse(coor[0]-radius,coor[1]-radius,2*radius,2*radius)

	def keyPressEvent(self,event):
		if event.key()==Qt.Key_Escape:
			self.close()

	def mousePressEvent(self,event):
		self.mouseClicking=True
		self.update()

	def mouseMoveEvent(self,event):
		if self.mouseClicking:
			self.x=event.pos().x()
			self.y=event.pos().y()
			if self.notRepeat(self.x,self.y):
				self.spaceArray.insert(0,[self.x,self.y])
				self.update()			

	def mouseReleaseEvent(self,event):
		self.mouseClicking=False
		self.update()


	def notRepeat(self,x,y):
		for i in self.spaceArray:
			if (i[0] == x) and (i[1]==y):
				return False
		return True

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow,self).__init__()

		self.scene=QGraphicsScene()
		self.scene.setSceneRect(0, 0, 800, 600)

		pixmap=self.openImage()
		self.imagePanel=DrawRegions(scene=self.scene)
		self.imagePanel.setPixmap(pixmap)
		self.scene.addItem(self.imagePanel)

		self.view = QGraphicsView(self.scene)
		layout=QHBoxLayout()
		layout.addWidget(self.view)

		self.widget=QWidget()
		self.widget.setLayout(layout)

		self.setCentralWidget(self.widget)
		self.setWindowTitle("Draw Regions")

	def openImage(self):
		fname=QFileDialog.getOpenFileName(self,"Open image",
			"/home/lkit/Pictures","Image Files (*.bmp *.jpg *.png *.xpm)")
		if fname.isEmpty(): return None
		return QPixmap(fname)



def main():        
    app=QApplication(sys.argv)
    ex=MainWindow()
    ex.show()
    app.exec_()
    app.deleteLater()
    sys.exit()

if __name__=='__main__':
    main()		

