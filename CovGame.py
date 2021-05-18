import pygame
import pymunk
import random
import matplotlib.pyplot as plt

pygame.init()

display = pygame.display.set_mode((2400, 1200))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 90
radius = 10
population = 900
recovery_time = random.randint(300, 800)

class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = pymunk.Body()
        self.body.position = x,y
        self.body.velocity = random.uniform(-100, 100), random.uniform(-100, 100)
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.infected_time = 0
        self.infected = False
        self.recovered = False
        space.add(self.body, self.shape)
    def pass_time(self):
        if self.infected:
            self.infected_time +=1
        if self.infected_time >= recovery_time:
            self.infected = False
            self.recovered = True
            self.shape.collision_type = population+2
            self.shape.density = 0.1
    def draw(self):
        x, y=self.body.position
        if self.infected:
            pygame.draw.circle(display, (255, 0, 0), (int(x), int(y)), radius)
        elif self.recovered:
            pygame.draw.circle(display, (0, 0, 255), (int(x), int(y)), radius)
        else:
            pygame.draw.circle(display, (255, 255, 255), (int(x), int(y)), radius)
    def infect(self, space=0, arbiter=0, data=0):
        self.infected = True
        self.shape.collision_type = population + 1
        self.body.velocity = 0, 0
        self.shape.density = random.gauss(1.3, 0.1)

class Wall():
    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, int(radius/2))
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

infected_count = []
recovered_count = []

def game():
    balls = [Ball(random.randint(0,2400), random.randint(0,1200)) for i in range(population)]
    for i in range(1, population+1):
        balls[i-1].shape.collision_type = i
        handler = space.add_collision_handler(i, population+1)
        handler.separate = balls[i-1].infect
    random.choice(balls).infect()
    walls = [Wall((0,0), (0, 1200)), Wall((0,0), (2400, 0)), Wall((0, 1200), (2400, 1200)), Wall((2400, 0), (2400, 1200))]



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        display.fill((0,0,0))
        infected_count_thisframe = 0
        recovered_count_thisframe = 0
        for ball in balls:
            ball.draw()
            ball.pass_time()
            if ball.infected:
                infected_count_thisframe +=1
                ball.shape.elasticity = random.uniform(0,1)
            if ball.recovered:
                recovered_count_thisframe +=1
                ball.shape.elasticity = 1
        if len(infected_count) <=10000:
            infected_count.append(infected_count_thisframe)
            recovered_count.append(recovered_count_thisframe)

        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)

game()
pygame.quit()
plt.plot(range(0, len(infected_count), 1), infected_count)
plt.plot(range(0, len(infected_count), 1), recovered_count)
plt.show()