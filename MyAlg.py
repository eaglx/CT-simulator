import numpy as np
from skimage.exposure import rescale_intensity
import skimage.morphology as mp
from skimage import filters
import matplotlib.pyplot as plt

# https://pl.wikipedia.org/wiki/Algorytm_Bresenhama
# x1 , y1 - współrzędne początku odcinka
# x2 , y2 - współrzędne końca odcinka
def bresenham_line(x1, y1, x2, y2):
    # zmienne pomocnicze
    d = dx = dy = ai = bi = 0
    xi = yi = 0
    x = x1
    y = y1
    line = []

    # ustalenie kierunku rysowania
    if (x1 < x2):
        xi = 1
        dx = x2 - x1
    else:
        xi = -1;
        dx = x1 - x2;

    # ustalenie kierunku rysowania
    if (y1 < y2):
        yi = 1
        dy = y2 - y1
    else:
        yi = -1
        dy = y1 - y2

    # pierwszy piksel
    line.append([x, y])
    # oś wiodąca OX
    if (dx > dy):
        ai = (dy - dx) * 2
        bi = dy * 2
        d = bi - dx
        # pętla po kolejnych x
        while (x != x2):
            # test współczynnika
            if (d >= 0):
                x = x + xi
                y = y + yi
                d = d + ai
            else:
                d = d + bi
                x = x + xi
            line.append([x, y])
    # oś wiodąca OY
    else:
        ai = ( dx - dy ) * 2
        bi = dx * 2
        d = bi - dy
        # pętla po kolejnych y
        while (y != y2):
            #test współczynnika
            if (d >= 0):
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                y += yi
            line.append([x, y])

    return line

class Pixel:
    def __init__(self):
        self.count = int(0)
        self.average = np.float(0)
        self.value = np.float(0)

def get_normalised_pixel(image, line):
    pixel = Pixel()
    for pos in line:
        if pos[0]>=0 and pos[1]>=0 and pos[0]<len(image) and pos[1]<len(image):
            pixel.value += float(image[int(pos[0]), int(pos[1])])
            pixel.count += 1
    pixel.average = pixel.value / pixel.count
    return pixel

def make_sinogram(image, **kwargs):
    settings = {
        'width': 90,
        'alpha': 2,
        'detector_amount': 180
    }

    settings.update(kwargs)

    width = settings['width']
    alpha = settings['alpha']
    detector_amount = settings['detector_amount']
    picture_size = len(image[0])
    r = int(np.ceil(picture_size))

    sinogram = []
    lines = []

    snapschot = 0;

    for i in range(0, 360, alpha):
        sinogram.append([])
        lines.append([])
        for detector in range(0, detector_amount):
            x1 = r * np.cos(i * np.pi / 180)
            y1 = r * np.sin(i * np.pi / 180)                                    #ilosc detektorów
            x2 = r * np.cos((i + 180 - (width / 2) + detector * (width / (detector_amount))) * np.pi / 180)
            y2 = r * np.sin((i + 180 - (width / 2) + detector * (width / (detector_amount))) * np.pi / 180)
            x1 = int(x1) + np.floor(picture_size / 2)
            y1 = int(y1) + np.floor(picture_size / 2)
            x2 = int(x2) + np.floor(picture_size / 2)
            y2 = int(y2) + np.floor(picture_size / 2)

            line = bresenham_line(x1, y1, x2, y2)
            pixel = get_normalised_pixel(image, line)
            sinogram[-1].append(pixel.average)
            lines[-1].append([x1, y1, x2, y2])

        #snapschot+=1
        #fig, plots = plt.subplots(1,1)
        #plots.imshow(sinogram, cmap='gray')
        #plt.savefig("out_sin/snapschot_sinogram_" + str(snapschot) + ".png")

    return sinogram, lines

def filtering_picture(img) : # maska na sinogram convolve, http://www.dspguide.com/ch25/5.htm
    new_img = filters.gaussian(img, sigma=1)
    new_img = mp.dilation(mp.erosion(new_img))
    return new_img

def normalizing_picture(reconstructed, helper):
    normalized = np.copy(reconstructed)
    picture_shape = np.shape(normalized)
    width = picture_shape[0]
    height = picture_shape[1]

    for i in range (0, width, 1):
        for j in range (0, height, 1):
            if helper[i][j] != 0:
                normalized[i][j] = normalized[i][j]/helper[i][j]
    return normalized

def reconstruct_img(image, sinogram, lines):
    # wymiary zdjęcia końcowego
    picture_shape = np.shape(image)
    width = picture_shape[0]
    height = picture_shape[1]
    # dane o projekcjach i detektorach
    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detectors = sinogram_shape[1]
    # dane do rekonstrukcji zdjęcia
    reconstructed = np.zeros(shape = picture_shape)
    helper = np.zeros(shape = picture_shape)

    snapschot = 0;

    # rekonstrukcja zdjęcia
    for projection in range (0, number_of_projections, 1):
        for detector in range (0, number_of_detectors, 1):
            x1, y1, x2, y2 = lines[projection][detector]
            line = bresenham_line(x1, y1, x2, y2)
            value = sinogram[projection][detector]
            for i in range (0, len(line), 1):
                    x, y = line[i]
                    if x >= 0 and y >= 0 and x < width and y < height:
                        reconstructed[int(x)][int(y)] += value
                        helper[int(x)][int(y)] += 1

        #fragment = normalizing_picture(reconstructed, helper)
        #fragment[fragment[:,:] < 0] = 0
        #fragment = rescale_intensity(fragment)
        #reconstructed2 = filtering_picture(fragment)

        #snapschot+=1
        #fig, plots = plt.subplots(1,1)
        #plots.imshow(reconstructed2, cmap='gray')
        #plt.savefig("out_recv/snapschot_reconstructed_" + str(snapschot) + ".png")

    fragment = normalizing_picture(reconstructed, helper)
    fragment[fragment[:,:] < 0] = 0
    fragment = rescale_intensity(fragment)
    reconstructed = filtering_picture(fragment)

    return reconstructed
