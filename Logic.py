from BresenhamLine import bresenham_line
import numpy as np

def get_pixel_value(image, line):
    pixels = image.load()
    for pos in line:
        if pos[0]>=0 and pos[1]>=0 and pos[0]<=image.size[0] and pos[1]<=image.size[1]:
            pixel_raw += float(pixels[int(pos[0]), int(pos[1])])
            pixel_max += 1
    if pixel_max != 0:
        raise AssertionError()
    pixel_normalize = pixel_raw / pixel_max
    return pixel_normalize

def picture2sinogram(image, **kwargs):
    options = {
        'width': 90,
        'alpha': 2,
        'detector_amount': 360
    }

    options.update(kwargs)
    width = options['width']        # szrokość rozstawu detektorów
    alpha = options['alpha']        # kąt obrotu
    detector_amount = options['detector_amount'] # ilość detektorów

    sinogram = []
    lines = []
    image_width = image.size[0]
    image_hight = image.size[1]

    for i in range(0, 360, alpha):
        sinogram.append([])
        lines.append([])
        for detector in range(0, detector_amount):

            line = bresenham_line(x1, y1, x2, y2)

            sinogram[-1].append(get_pixel_value(image, line))
            lines[-1].append([x1, y1, x2, y2])

    return sinogram, lines
