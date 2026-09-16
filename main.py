import pygame
import random
import math

pygame.init()

#Size of the window
SIZE = (1200, 900)

#Size of the "pixels" for rendering. I recommend starting with 20, feel free to decrease the size if your computer allows for it
#or increase the number if the framerate is too low.
RESOLUTION = 20

screen = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()

#Each cell stores its "field value" as a float
grid = {}

for y in range(SIZE[1] // RESOLUTION + 1):

    for x in range(SIZE[0] // RESOLUTION + 1):

        grid[(x, y)] = 0.

#This is a class that represents the "field sources", its main method is "return_value", 
#which calculates the inverse squared distance for each passed coordinate

class field_generator:

    def __init__(self, coords, screen):

        self.coords = coords

        self.original_coords = coords

        self.screen = screen

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    #Optional (if you need to see the centers)
    def render(self):

        pygame.draw.aacircle(screen, self.color, self.coords, 4)

    #This one is for animation, feel free to toggle as you see fit
    def update_position(self, time):

        self.coords = (self.original_coords[0] + 100 * math.sin(self.original_coords[0] + time), self.original_coords[1] + 100 * math.cos(self.original_coords[1] + time))

    #This is the actual Metaballs calculation. Choose either metric.
    def return_value(self, position):

        #Euclidian distance (default)

        return 2000 / (((position[0] - self.coords[0])**2) + ((position[1] - self.coords[1])**2) + 1)

        #Manhattan distance (quite a cool topic, I suggest to look it up! It allows for MULTIPLE "shortest paths",
        #compared to a single straight line in Euclidian space. Oh, and the "manhattan" circle is a square btw, haha)

        #return 50 / (abs(position[0] - self.coords[0]) + abs(position[1] - self.coords[1]) + 1)


#The amount of "field sources" you want. The higher the number, the more computation per pixel per frame it needs. Don't overdo!
POINTS = 15

points = [field_generator((random.randint(0, SIZE[0]), random.randint(0, SIZE[1])), screen) for p in range(POINTS)]


def render_grid(screen, resolution, grid : dict[tuple[int, int], float]):

    for coord in grid.keys():

        # The formula here can be condensed into A + B*cos(2pi*(C*input + D)), where each capital letter is a vec3

        red = 0.485 + 0.29 * math.cos(2*math.pi*(1*grid[coord] + 4.9))
        
        green = 0.496 + 0.537 * math.cos(2*math.pi*(1*grid[coord] + 2.8))

        blue = 0.683 + 0.14 * math.cos(2*math.pi*(2*grid[coord] - 0.2))


        #Clamping the channels to prevent rendering issues

        red = min(255 * max(0, red), 255)

        green = min(255 * max(0, green), 255)

        blue = min(255 * max(0, blue), 255)


        #Here are 2 rendering styles, upper is circles, the lower is squares. Feel free to comment and uncomment either!

        pygame.draw.aacircle(screen, (red, green, blue), (resolution * coord[0], resolution * coord[1]), resolution//2 - 1)

        #pygame.draw.rect(screen, (red, green, blue), (resolution * coord[0], resolution * coord[1], resolution, resolution))


def calculate_grid(resolution, grid, points : list[field_generator]):

    for coord in grid.keys():

        field_value = 0
    
        for p in points:

            field_value += p.return_value((coord[0] * resolution, coord[1] * resolution))

        grid[coord] = field_value



calculate_grid(RESOLUTION, grid, points)

time = 0

running = True

while running:

    dt = clock.tick(30)/1000

    time += dt

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

    calculate_grid(RESOLUTION, grid, points)

    screen.fill((40,40,40))

    render_grid(screen, RESOLUTION, grid)

    for p in points:

        p.update_position(time)
        
        #p.render()

    pygame.display.flip()