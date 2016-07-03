import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DrawRegions(QGraphicsPixmapItem):

	def __init__(self,pixmap=None,parent=None,scene=None):
		super(DrawRegions,self).__init__()
		self.spaceArray=[]
		self.setFlags(QGraphicsPixmapItem.ItemIsFocusable)
		self.scale=1.0
		self.mouseLeftClicking, self.mouseRightClicking=False, False
		# self.setTransformOriginPoint(self.pixmap().height()/2,self.pixmap().height()/2)
		self.scaleX, self.scaleY = 0,0
		self.brushSize=30
		# self.setX(-250)
		# self.setY(-50)


	def paint(self,painter,options,widget=None):
		painter.drawPixmap(0,0,self.pixmap())

		radius=self.brushSize
		painter.setPen(Qt.NoPen)
		painter.setBrush(QColor(125,125,125,20))
		for coor in self.spaceArray:
			radius=coor[2]
			painter.drawEllipse(coor[0]-radius,coor[1]-radius,2*radius,2*radius)

	def mousePressEvent(self,event):
		# print self.boundingRect()
		if event.button()==Qt.LeftButton:
			self.mouseLeftClicking=True
		elif event.button()==Qt.RightButton:
			# self.mouseRightClicking=True
			# print event.pos().x(),event.pos().y()
			self.scaleX=event.pos().x()
			self.scaleY=event.pos().y()
			self.setX(self.pixmap().width()/2-self.scaleX)
			self.setY(self.pixmap().height()/2-self.scaleY)
			
		self.update()

	def mouseMoveEvent(self,event):
		if self.mouseLeftClicking:
			self.x=event.pos().x()
			self.y=event.pos().y()
			r=self.brushSize
			if self.notRepeat(self.x,self.y):
				self.spaceArray.insert(0,[self.x,self.y,r])
				self.update()			

	def mouseReleaseEvent(self,event):
		self.mouseLeftClicking=False
		self.mouseRightClicking=False
		self.update()
		print self.spaceArray

	def keyPressEvent(self,event):
		super(DrawRegions,self).keyPressEvent(event) 	#need this,can press esc
		if event.key()==Qt.Key_Q:
			self.setTransformOriginPoint(self.scaleX,self.scaleY)
			if self.scale>=1 and self.scale<10:
				self.scale += 0.5
			elif self.scale<1:
				self.scale += 0.2
			self.setScale(self.scale)
		elif event.key()==Qt.Key_W:
			self.setTransformOriginPoint(self.scaleX,self.scaleY)
			if self.scale > 1:
				self.scale -= 0.5
			elif self.scale>=0.4:
				self.scale -= 0.2
			self.setScale(self.scale)
		elif event.key()==Qt.Key_E:
			self.setTransformOriginPoint(0,0)
			self.setScale(1.0)
		elif event.key()==Qt.Key_D:
			if self.brushSize<=55:
				self.brushSize +=5
		elif event.key()==Qt.Key_C:
			if self.brushSize >=10:
				self.brushSize -= 5
			elif self.brushSize <=5 and self.brushSize>1:
				self.brushSize -= 1


	def notRepeat(self,x,y):
		for i in self.spaceArray:
			if (i[0] == x) and (i[1]==y):
				return False
		return True

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow,self).__init__()

		self.scene=QGraphicsScene()
		pixmap=self.openImage()

		self.scene.setSceneRect(0, 0, pixmap.width(),pixmap.height())

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

	def keyPressEvent(self,event):
		if event.key()==Qt.Key_Escape:
			self.close()

def main():        
    app=QApplication(sys.argv)
    ex=MainWindow()
    ex.show()
    app.exec_()
    app.deleteLater()
    sys.exit()

if __name__=='__main__':
    main()		

