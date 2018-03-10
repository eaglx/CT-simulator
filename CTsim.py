import Logic

from PIL import Image

def main():
    image = Image.open('data/test.png')

    #sinogram, lines = picture2sinogram(image)
    pixels = image.getpixel((0,0))
    print(pixels)
    #return

if __name__ == "__main__":
    main();
