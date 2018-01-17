import pygame, sys, json, time
import random

def get_settings():
    try:
        file = open("settings.json")
        settings = json.load(file)
        return settings
    except:
        settings = {
            "README": [
                "width and height - window width and height",
                "n_balls - number of balls",
                "r - IF a single number: the constant radius of all balls, IF in format [min:max]: random radius for every circle",
                "k - IF -1: random spawn coordinates, IF [x,y]: set spawn for all circes",
                "k_direction - IF -1: random direction , IF \"NE\", \"NW\", \"SE\", \"SW\": set initial direction",
                "speed - IF single number:(pixel per frame) speed for circles, IF [min,max]: random speed for each circle",
                "color - IF [R,G,B]: red,green and blue values for color of circles, IF -1: random colors for circles",
                "fps - frames per second of simulation, WARNING: speed of circles is defined as pixel per frame"
            ],
            "width" : 800,
            "height": 600,
            "n_balls": 1,
            "r": 20,
            "k": -1,
            "k_direction": -1,
            "speed":5,
            "color":(0, 0, 0),
            "fps": 60,
        }
        file = open("settings.json","w")
        json.dump(settings, file, indent=2)
        file = open("settings.json", "r")
        settings = json.load(file)
        return settings

settings = get_settings()
class Ball():

    def __init__(self, screen, r, k, dir, speed, color):
        global width
        global height
        self.screen = screen
        # Radius
        if isinstance(r, int):
            self.r = r
        elif isinstance(r, list):
            self.r = random.randint(r[0],r[1])
        else:
            print("invalid radius setting")
        # Spawn position
        if k == -1:
            self.x = random.randint(self.r, width)
            self.y = random.randint(self.r, height)
        elif isinstance(k, list):
            self.x = k[0]
            self.y = k[1]
        else:
            print("invalid spawn setting")
        # Spawn direction
        if dir == -1:
            list1 = ["SE", "SW", "NE", "NW"]
            self.direction = random.choice(list1)
        else:
            self.direction = dir
        # Speed
        if isinstance(speed, int):
            self.speed = speed
        elif isinstance(speed, list):
            self.speed = random.randint(speed[0], speed[1])
        else:
            print("invalid speed setting")
        # Color
        if color == -1:
            self.color = (random.randint(0,250), random.randint(0,250), random.randint(0,250))
        elif isinstance(color, list):
            self.color = (color[0], color[1], color[2])
    def move(self):
        if self.direction == "SE":
            self.x += self.speed
            self.y += self.speed
        if self.direction == "NE":
            self.x += self.speed
            self.y -= self.speed
        if self.direction == "NW":
            self.x -= self.speed
            self.y -= self.speed
        if self.direction == "SW":
            self.x -= self.speed
            self.y += self.speed
        self.check_hit()

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def check_hit(self):
        # Check if hit bottom
        if self.y + self.r > height:
            if self.direction == "SE":
                self.direction = "NE"
            elif self.direction == "SW":
                self.direction = "NW"
        # Check if hit right
        elif self.x + self.r > width:
            if self.direction == "NE":
                self.direction = "NW"
            elif self.direction == "SE":
                self.direction = "SW"
        # Check if hit top
        elif self.y < self.r:
            if self.direction == "NW":
                self.direction = "SW"
            elif self.direction == "NE":
                self.direction = "SE"
        # Check if hit left
        elif self.x < self.r:
            if self.direction == "SW":
                self.direction = "SE"
            elif self.direction == "NW":
                self.direction = "NE"

pygame.init()
width = settings["width"]
height = settings["height"]
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Create a list of balls
balls = []
for i in range(settings["n_balls"]):
    balls.append(Ball(screen, r=settings["r"], k=settings["k"], dir=settings["k_direction"],
                      speed=settings["speed"], color=settings["color"]))

def getsize(ball):
    return ball.r
# Sort balls bigger one first so that they get rendered first
# This way smaller balls will be infront of big ones if the cross paths
balls = sorted(balls, key=getsize, reverse=True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(screen, "pic.png")
            sys.exit()

    screen.fill((200, 200, 200))
    try:
        for ball in balls:
            ball.draw()
            ball.move()
    except:
        time.sleep(100)

    #draw frame
    pygame.display.flip()
    clock.tick(settings["fps"])

