import pygame
import random
import math

pygame.init()

SIZE = (1200, 900)

screen = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()

running = True

class field_generator:

    def __init__(self, coords, screen):

        self.coords = coords

        self.original_coords = coords

        self.screen = screen

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def render(self):

        pygame.draw.aacircle(screen, self.color, self.coords, 4)

    def update_position(self, time):

        self.coords = (self.original_coords[0] + 100 * math.sin(self.original_coords[0] + time), self.original_coords[1] + 100 * math.cos(self.original_coords[1] + time))

    def return_value(self, position):

        return 2000 / (((position[0] - self.coords[0])**2) + ((position[1] - self.coords[1])**2) + 1)


POINTS = 20

points = [field_generator((random.randint(0, SIZE[0]), random.randint(0, SIZE[1])), screen) for p in range(POINTS)]




RESOLUTION = 10

scan = {}

for y in range(SIZE[1] // RESOLUTION):

    for x in range(SIZE[0] // RESOLUTION):

        scan[(x, y)] = (255, 255, 255)


def render_scan(screen, resolution, scan : dict[tuple[int, int], tuple[int, int, int]]):

    for coord in scan.keys():

        pygame.draw.aacircle(screen, scan[coord], (resolution * coord[0], resolution * coord[1]), resolution//2 - 1)

        #pygame.draw.rect(screen, scan[coord], (resolution * coord[0], resolution * coord[1], resolution, resolution))


def calculate_scan(resolution, scan, points : list[field_generator]):

    for coord in scan.keys():

        field_value = 0
    
        for p in points:

            field_value += p.return_value((coord[0] * resolution, coord[1] * resolution))

        field_value /= 1

        #if field_value > 1:

        #    field_value = 0.1

        red = 0.485 + 0.29 * math.cos(2*math.pi*(1*field_value + 4.9))

        green = 0.496 + 0.537 * math.cos(2*math.pi*(1*field_value + 2.8))

        blue = 0.683 + 0.14 * math.cos(2*math.pi*(2*field_value - 0.2))

        red = min(255 * max(0, red), 255)

        green = min(255 * max(0, green), 255)

        blue = min(255 * max(0, blue), 255)

        scan[coord] = (red, green, blue)



calculate_scan(RESOLUTION, scan, points)

time = 0

while running:

    dt = clock.tick(30)/1000

    time += dt

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    calculate_scan(RESOLUTION, scan, points)

    screen.fill((40,40,40))

    render_scan(screen, RESOLUTION, scan)

    for p in points:

        p.update_position(time)
        
        #p.render()

    pygame.display.flip()