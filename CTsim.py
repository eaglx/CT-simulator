import MyAlg

from PyQt4 import QtGui, QtCore
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import io
from skimage.transform import rescale
import sys

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

        self.reconst_image = MyAlg.reconstruct_img(self.orginal_image, self.sinogram, self.lines)
        fig, plots = plt.subplots(1,1)
        plots.imshow(self.reconst_image, cmap='gray')
        plt.savefig("out/reconst_image.png")

def main(width, alpha, detector_amount):
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

    def __home__(self):
        self.show()


if __name__ == "__main__":
    #main(90, 2, 180)
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
