# x1 , y1 - współrzędne początku odcinka
# x2 , y2 - współrzędne końca odcinka
def bresenham_line(x1, y1, x2, y2):
    # zmienne pomocnicze
    d = 0
    dx = 0
    dy = 0
    ai = 0
    bi = 0
    xi = 0
    yi = 0
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
