import pygame
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A scroller to scroll through the image")

    parser.add_argument('-f', dest='file', type=str, default=None,
                        help='Set image path')

    args = parser.parse_args()

    pygame.init()


    display_width = 800
    display_height = 600

    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('Scroller')

    black = (0,0,0)
    white = (255,255,255)

    clock = pygame.time.Clock()
    exit = False

    mazeImg = pygame.image.load(args.file)

    size = mazeImg.get_rect().size
    new_size = (size[0]*4,size[1]*4)
    mazeImg = pygame.transform.scale(mazeImg, new_size)
    def maze(x,y):
        gameDisplay.blit(mazeImg, (int(x),int(y)))


    x = 0
    y = 0

    speed = 0.75

    down = True

    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True

        gameDisplay.fill(black)
        maze(x,y)

        if down:
            y-=speed
        else:
            y+=speed


        if y < (-new_size[1]+display_height):
            down = False
        elif y > 0:
            down  = True

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()
