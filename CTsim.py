import MyAlg

from PyQt4 import QtGui, QtCore
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import io
from skimage.transform import rescale
import os, sys
#import imageio

class Tomograph:
    orginal_image = []
    sinogram = []
    sin_filtred = []
    reconst_image = []

    def __init__(self, img, width_, alpha_, detector_amount_):
        self.orginal_image = img
        self.width = width_
        self.alpha = alpha_
        self.detector_amount = detector_amount_

        fig, plots = plt.subplots(1,1)
        plots.imshow(self.orginal_image, cmap='gray')
        plt.savefig("out/orginal.png")

    def work(self):
        self.sinogram, self.lines = MyAlg.make_sinogram(self.orginal_image,
                width=self.width, alpha=self.alpha, detector_amount=self.detector_amount)
        fig, plots = plt.subplots(1,1)
        plots.imshow(self.sinogram, cmap='gray')
        plt.savefig("out/sinogram.png")
        #images = []
        #for filename in os.listdir("out_sin/"):
        #    images.append(imageio.imread("out_sin/" + filename))
        #imageio.mimsave("out/sinogram.gif", images)


        self.reconst_image = MyAlg.reconstruct_img(self.orginal_image, self.sinogram, self.lines)
        fig, plots = plt.subplots(1,1)
        plots.imshow(self.reconst_image, cmap='gray')
        plt.savefig("out/reconst_image.png")
        #images = []
        #for filename in os.listdir("out_recv/"):
        #    images.append(imageio.imread("out_recv/" + filename))
        #imageio.mimsave("out/reconst_image.gif", images)

def main_tomograph(width, alpha, detector_amount):
    image = np.zeros([200, 200])
    image[24:174, 24:174] = rgb2gray(io.imread('data/shepp_logan.png'))
    ct = Tomograph(image, width, alpha, detector_amount)
    ct.work()

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(150, 150, 700, 600)
        self.setWindowTitle("CTsim")
        self.fixSizeString = False
        self.__home__()

    def tomograph_start(self):
        arg1 = int(self.textbox1.text())
        arg2 = int(self.textbox2.text())
        arg3 = int(self.textbox3.text())

        main_tomograph(arg1, arg2, arg3)

        self.l4 = QtGui.QLabel(self)
        self.l4.setText("Input")
        self.l4.move(20,140)
        self.l4.show()

        self.pic = QtGui.QLabel(self)
        self.pic.setGeometry(20, 160, 400, 400)
        self.pixmap = QtGui.QPixmap("out/orginal.png")
        self.pixmap = self.pixmap.scaledToHeight(400)
        self.pixmap = self.pixmap.scaledToWidth(400)
        self.pic.setPixmap(self.pixmap)
        self.pic.show()

        self.l5 = QtGui.QLabel(self)
        self.l5.setText("Sinogram")
        self.l5.move(430,140)
        self.l5.show()

        self.pic2 = QtGui.QLabel(self)
        self.pic2.setGeometry(430, 160, 400, 400)
        self.pixmap2 = QtGui.QPixmap("out/sinogram.gif")
        self.pixmap2 = self.pixmap2.scaledToHeight(400)
        self.pixmap2 = self.pixmap2.scaledToWidth(400)
        self.pic2.setPixmap(self.pixmap2)
        self.pic2.show()

        self.l5 = QtGui.QLabel(self)
        self.l5.setText("Reconstructed")
        self.l5.move(840,140)
        self.l5.show()

        self.pic3 = QtGui.QLabel(self)
        self.pic3.setGeometry(840, 160, 400, 400)
        self.pixmap3 = QtGui.QPixmap("out/reconst_image.gif")
        self.pixmap3 = self.pixmap3.scaledToHeight(400)
        self.pixmap3 = self.pixmap3.scaledToWidth(400)
        self.pic3.setPixmap(self.pixmap3)
        self.pic3.show()

    def on_click(self):
        self.tomograph_start()

    def __home__(self):
        self.button = QtGui.QPushButton('Start scan', self)
        self.button.move(20,100)
        self.button.clicked.connect(self.on_click)

        self.l1 = QtGui.QLabel(self)
        self.l1.setText("width")
        self.l1.move(10,10)
        self.textbox1 = QtGui.QLineEdit(self)
        self.textbox1.move(20, 40)
        self.textbox1.resize(100,40)
        self.textbox1.setText("90")

        self.l2 = QtGui.QLabel(self)
        self.l2.setText("alpha")
        self.l2.move(130,10)
        self.textbox2 = QtGui.QLineEdit(self)
        self.textbox2.move(140, 40)
        self.textbox2.resize(100,40)
        self.textbox2.setText("2")

        self.l3 = QtGui.QLabel(self)
        self.l3.setText("detect_amount")
        self.l3.move(230,10)
        self.textbox3 = QtGui.QLineEdit(self)
        self.textbox3.move(260, 40)
        self.textbox3.resize(100,40)
        self.textbox3.setText("180")

        self.showMaximized()

def main():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
