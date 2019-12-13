import numpy as np
from noise import pnoise2
import random
import argparse


def make_png(pixels):
    from PIL import Image

    size = pixels.shape
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


def make_im_from_arr(image_arr, screen_array):
    screen_array[:, :, 0][image_arr < threshold] = 255
    screen_array[:, :, 0][image_arr >= threshold] = 0
    screen_array[:, :, 1] = screen_array[:, :, 0]
    screen_array[:, :, 2] = screen_array[:, :, 0]
    return pygame.surfarray.make_surface(screen_array)


def update_matrix(pixels, row_index, true_index, offset_x, offset_y):
    # Needs to replace a row with the correct offset.
    # To do this, we need the row / column.
    if row_index == pixels.shape[0] // 2:
        # Update whole lower matrix.
        for i in range(size[0], size[0] * 2):
            i1 = (i + true_index) / 10 + offset_x
            for j in range(size[1], size[1] * 2):
                j1 = (j + true_index) / 10 + offset_y
                pixels[i][j] = pnoise2(i1, j1)
        return true_index + size[0]
    else:
        y = (row_index + true_index) / 10 + offset_y
        for j in range(row_index, size[0] + row_index):
            x = (j + true_index) / 10 + offset_x
            pixels[j][row_index] = pnoise2(x, y)
        x = (row_index + true_index) / 10 + offset_x
        for j in range(row_index, size[0] + row_index):
            y = (j + true_index) / 10 + offset_y
            pixels[row_index][j] = pnoise2(x, y)
        return true_index


def update_matrix_funky(pixels, row_index, true_index, offset_x, offset_y):
    # Needs to replace a row with the correct offset.
    # To do this, we need the row / column.
    if row_index == pixels.shape[0] // 2:
        # Update whole lower matrix.
        for i in range(size[0], size[0] * 2):
            i1 = i / 10 + offset_x
            for j in range(size[1], size[1] * 2):
                j1 = j / 10 + offset_y
                pixels[i][j] = pnoise2(i1, j1)
    else:
        for j in range(row_index, size[0] + row_index):
            x = j / 10 + offset_x
            pixels[j][row_index] = pnoise2(x, offset_y)
        for j in range(row_index, size[0] + row_index):
            y = j / 10 + offset_y
            pixels[row_index][j] = pnoise2(offset_x, y)
    return true_index + 1


def generate_diagonal_noise_array(size):
    pixels = np.zeros((size[0] * 2, size[1] * 2))

    offset_x = random.randint(0, 10000)
    offset_y = random.randint(0, 10000)
    true_index = 0
    for i in range(size[0] + 1):
        true_index = update_matrix(pixels, i, true_index, offset_x, offset_y)
    np.abs(pixels, out=pixels)
    return pixels, offset_x, offset_y, true_index


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


def run_pygame(size):
    import pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Maze generator")
    pixels, offset_x, offset_y, true_index = generate_noise_array(size)
    screen_array = np.zeros((size[0], size[1], 3), np.ubyte)
    run_game = True
    i = 0
    while run_game:
        # handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

        image = make_im_from_arr(pixels[i:i + size[0], i:i + size[0]], screen_array)
        # save_png("surf%i.png" % (i + true_index), make_png(pixels))
        screen.blit(image, (0, 0))
        pygame.display.update()
        true_index = update_matrix(pixels, i, true_index, offset_x, offset_y)
        i %= size[0]
        i += 1

        clock.tick(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate perlin noise mazes")
    image_or_scrolling = parser.add_mutually_exclusive_group()
    image_or_scrolling.add_argument('--scroll', action='store_true',
                                    help="Run a scrolling image")
    image_or_scrolling.add_argument('file_name', type=str, default=None, nargs='?',
                        help='Output filename.')
    parser.add_argument('-im_w', dest='width', type=int, default=500,
                        help='Set the image width')
    parser.add_argument('-im_h', dest='height', type=int, default=500,
                        help='Set the image height')
    parser.add_argument('-t', dest='threshold', type=float, default=0.1,
                        help='Set the perlin noise threshold.')
    parser.add_argument('-s', dest='seed', type=float, default=random.random(),
                        help='Provide a seed to generate perlin maps.')

    args = parser.parse_args()
    random.seed(args.seed)
    threshold = args.threshold
    size = (args.width, args.height)
    if args.scroll:
        run_pygame(size)
    else:
        pixels = generate_noise_array(size)

        if args.file_name:
            save_png(args.file_name, make_png(pixels))
        else:
            im = make_png(pixels)
            im.show()
            file_name = str(args.seed).replace(".", "_") + ".png"
            save_png(file_name, make_png(pixels))
