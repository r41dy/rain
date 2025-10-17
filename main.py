import pygame as pg
import random

pg.init()
WIDTH, HEIGHT = 1280, 720
FPS = 75
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Rain")

vec2 = pg.Vector2

run = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

particles = []
splashes = []

last_spawn_time = pg.time.get_ticks()
rain_length = 10
rain_width = 1
rain_speed = 10
rain_amount = 1
rain_speed_randomness = 0.25
horz = 5

spawn_interval = random.random()*rain_amount+rain_amount

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    clock.tick(FPS)
    time = pg.time.get_ticks()

    if time - last_spawn_time >= spawn_interval:
        particle_x = random.randint(0, int(WIDTH+HEIGHT))
        particle_y = 0
        rain_self_speed = rain_speed + (random.random()*rain_speed_randomness-(rain_speed_randomness/2))
        particles.append([particle_x, particle_y, rain_self_speed])
        spawn_interval = random.random()*rain_amount+rain_amount
        last_spawn_time = time
    
    screen.fill(BLACK)

    for particle in particles:
        prev_pos = vec2(particle[0], particle[1])
        particle[1] += particle[2]
        particle[0] -= horz
        particle_pos = vec2(particle[0], particle[1])
        pg.draw.aaline(screen, WHITE, vec2(particle_pos.x, particle_pos.y), vec2(particle_pos.x+(horz/(particle_pos.y - prev_pos.y))*rain_length, particle_pos.y-rain_length), rain_width)
        if particle[1] > HEIGHT+rain_length or particle[0] < 0:
            particles.remove(particle)
        if particle[1] == HEIGHT:
            print("splash")

    pg.display.flip()
pg.quit