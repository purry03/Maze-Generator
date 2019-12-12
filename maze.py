import numpy as np
from noise import pnoise2
import random
import argparse


def make_png(pixels):
    from PIL import Image

    im = Image.new('RGBA', size, 0)
    im_pixels = im.load()
    im_arr = np.zeros(size).astype("ubyte")
    im_arr[pixels <= threshold] = 255
    for x in range(size[0]):
        for y in range(size[1]):
            im_pixels[x, y] = (im_arr[x, y], im_arr[x, y], im_arr[x, y])
    return im


def save_png(file_name: str, im) -> None:
    import os

    if os.path.splitext(file_name)[-1] != ".png":
        file_name += ".png"
        print("save_png: Automatically appended .png to file_name")
    im.save(file_name, 'PNG')


def make_im_from_arr(image_arr):
    image_arr[image_arr < threshold] = 255
    image_arr[image_arr >= threshold] = 0
    image_arr = image_arr.astype(np.ubyte)
    white_pixels = np.dstack((image_arr, image_arr, image_arr))
    print(white_pixels.shape)
    return pygame.surfarray.make_surface(np.dstack(white_pixels))


def generate_noise_array(size):
    pixels = np.zeros(size)

    offset_x = random.randint(0, 10000)
    offset_y = random.randint(0, 10000)

    for i in range(size[0]):
        i1 = i / 10 + offset_x
        for j in range(size[1]):
            j1 = j / 10 + offset_y
            pixels[i][j] = pnoise2(i1, j1)
    np.abs(pixels, out=pixels)
    return pixels


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate perlin noise mazes")
    parser.add_argument('file_name', type=str, default=None, nargs='?',
                        help='Output filename.')
    parser.add_argument('-im_w', dest='width', type=int, default=500,
                        help='Set the image width')
    parser.add_argument('-im_h', dest='height', type=int, default=500,
                        help='Set the image height')
    parser.add_argument('-t', dest='threshold', type=int, default=0.1,
                        help='Set the perlin noise threshold.')
    parser.add_argument('-s', dest='seed', type=int, default=random.random(),
                        help='Provide a seed to generate perlin maps.')

    args = parser.parse_args()

    random.seed(args.seed)
    threshold = args.threshold
    size = (args.width, args.height)
    pixels = generate_noise_array(size)

    if args.file_name:
        save_png(args.file_name, make_png(pixels))
    else:
        im = make_png(pixels)
        im.show()
        file_name = str(args.seed).replace(".", "_") + ".png"
        save_png(file_name, make_png(pixels))
