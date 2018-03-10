import numpy as np

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
    if not pixel.count != 0:
        raise AssertionError()
    pixel.average = pixel.value / pixel.count
    return pixel

def make_sinogram(image, **kwargs):
    settings = {
        'width': 90,
        'alpha': 2,
        'detector_amount': 360
    }

    settings.update(kwargs)

    width = settings['width']
    alpha = settings['alpha']
    detector_amount = settings['detector_amount']
    picture_size = len(image[0])
    r = int(np.ceil(picture_size))

    sinogram = []
    lines = []

    for i in range(0, 360, alpha):
        sinogram.append([])
        lines.append([])
        for detector in range(0, detector_amount):
            x1 = r * np.cos(i * np.pi / 180)
            y1 = r * np.sin(i * np.pi / 180)
            x2 = r * np.cos((i + 180 - (width / 2) + detector * (width / (detector_amount - 1))) * np.pi / 180)
            y2 = r * np.sin((i + 180 - (width / 2) + detector * (width / (detector_amount - 1))) * np.pi / 180)
            x1 = int(x1) + np.floor(picture_size / 2)
            y1 = int(y1) + np.floor(picture_size / 2)
            x2 = int(x2) + np.floor(picture_size / 2)
            y2 = int(y2) + np.floor(picture_size / 2)

            line = bresenham_line(x1, y1, x2, y2)
            pixel = get_normalised_pixel(image, line)
            sinogram[-1].append(pixel.average)
            lines[-1].append([x1, y1, x2, y2])
    return sinogram, lines

def reconstruct_img(image, sinogram, lines):
    img_shape = np.shape(image)
    width - img_shape[0]
    height = img_shape[1]
    sinogram_shape = np.shape(sinogram)
    number_of_projections = sinogram_shape[0]
    number_of_detector = sinogram_shape[1]
