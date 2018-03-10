import MyAlg

import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import io

class Tomograph:
    orginal_image = []
    sinogram = []
    sin_filtred = []
    reconst_image = []
    width = 0
    alpha = 0
    detector_amount = 0

    def __init__(self, img, width_, alpha_, detector_amount_):
        self.orginal_image = img
        self.width = width_
        self.alpha = alpha_
        self.detector_amount = detector_amount_

    def work(self):
        self.sinogram, self.lines = MyAlg.make_sinogram(self.orginal_image, self.width, self.alpha, self.detector_amount)
        fig, plots = plt.subplots(1,2)
        plt.savefig("sinogram.png")
        return self.sinogram

def main(width, alpha, detector_amount):
    image = np.zeros([200, 200])
    image[24:174, 24:174] = rgb2gray(io.imread('data/shepp_logan.png'))
    ct = Tomograph(image, width, alpha, detector_amount)
    ct.work()

if __name__ == "__main__":
    main(90, 2, 180);
