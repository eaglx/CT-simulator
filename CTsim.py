import MyAlg

import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import io
from skimage.transform import rescale

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

    def work(self):
        self.sinogram, self.lines = MyAlg.make_sinogram(self.orginal_image,
                width=self.width, alpha=self.alpha, detector_amount=self.detector_amount)
        fig, plots = plt.subplots(1,2)
        plots[0].imshow(self.orginal_image, cmap='gray')
        plots[1].imshow(self.sinogram, cmap='gray')
        plt.savefig("sinogram.png")
        return self.sinogram

def main(width, alpha, detector_amount):
    image = np.zeros([200, 200])
    image[24:174, 24:174] = rgb2gray(io.imread('data/shepp_logan.png'))
    ct = Tomograph(image, width, alpha, detector_amount)
    ct.work()

if __name__ == "__main__":
    main(90, 2, 180);
