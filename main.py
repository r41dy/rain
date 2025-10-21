import pygame as pg
import random

pg.init()
WIDTH, HEIGHT = 1280, 720
FPS = 60
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Rain")

vec2 = pg.Vector2

run = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

raindrops = []
splashes = []

last_spawn_time = pg.time.get_ticks()
rain_length = 10
rain_width = 1
rain_speed = 1.5
rain_amount = 5 # more is less
rain_speed_randomness = 0.25
horz = 0.5

class Splash():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dots = []
        self.spawn_time = pg.time.get_ticks()

    def anim(self):
        for i in range(random.randint(0, 4)):
            self.dots.append([self.x, self.y, ((random.random()*2)-1), random.random()*-1-0.1])
        for dot in self.dots:
            dot_pos = vec2(dot[0], dot[1])
            dot_y_vel = dot[3]
            while True:
                dot_pos.x += dot[2]
                dot_pos.y += dot_y_vel
                dot_y_vel += 0.1

    def timer(self):
        timer = pg.time.get_ticks() - self.spawn_time
        if timer > 1000:
            return True

    def debug_draw(self):
        pg.draw.line(screen, WHITE, vec2(self.x, self.y), vec2(self.x, self.y-10))

    def __del__(self):
        pass

spawn_interval = random.random()*rain_amount+rain_amount

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    time = pg.time.get_ticks()

    if time - last_spawn_time >= spawn_interval:
        raindrop_x = random.randint(0, int(WIDTH+HEIGHT))
        raindrop_y = 0
        rain_self_speed = rain_speed + (random.random()*rain_speed_randomness-(rain_speed_randomness/2))
        raindrops.append([raindrop_x, raindrop_y, rain_self_speed])
        spawn_interval = random.random()*rain_amount+rain_amount
        last_spawn_time = time
    
    screen.fill(BLACK)

    for raindrop in raindrops:
        prev_pos = vec2(raindrop[0], raindrop[1])
        raindrop[1] += raindrop[2]
        raindrop[0] -= horz
        raindrop_pos = vec2(raindrop[0], raindrop[1])
        pg.draw.aaline(screen, WHITE, vec2(raindrop_pos.x, raindrop_pos.y), vec2(raindrop_pos.x+(horz/(raindrop_pos.y - prev_pos.y))*rain_length, raindrop_pos.y-rain_length), rain_width)
        if raindrop[1] > HEIGHT+rain_length or raindrop[0]+(horz/(raindrop_pos.y - prev_pos.y))*rain_length < -1:
            raindrops.remove(raindrop)
        if raindrop[1] > HEIGHT and raindrop[1] < HEIGHT+3:
            splash = Splash(raindrop_pos.x, HEIGHT)
            splashes.append(splash)

    for splash in splashes:
        splash.debug_draw()
        if splash.timer():
            splashes.remove(splash)
            del splash

    pg.display.flip()
pg.quit