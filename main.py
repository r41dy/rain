import pygame as pg
import random

pg.init()
WIDTH, HEIGHT = 1920, 1080
FPS = 75
clock = pg.time.Clock()
dt = clock.tick(FPS) / 1000.0
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Rain")

vec2 = pg.Vector2

run = True

raindrops = []
splashes = []
last_spawn_time = pg.time.get_ticks()

# PARAMETERS
BACKGROUND_COLOR = (0, 0, 0)
rain_length = 10
rain_width = 1
rain_speed = 500
rain_amount = 5 # less is more
rain_speed_randomness = 0.25
horizontal_rain_velocity = 250
rain_color_R, rain_color_G, rain_color_B = 255, 255, 255
value_randomness_factor = 0.25

class Splash():
    def __init__(self, x, y, color, rotation):
        self.x = x
        self.y = y
        self.dots = []
        self.color = color
        self.spawn_time = pg.time.get_ticks()
        for i in range(4):
            splash_rotation = vec2((random.random()*2-1)*100, -100).rotate(rotation)
            dot = [self.x, self.y-1, splash_rotation]
            self.dots.append(dot)

    def update(self, dt):
        for dot in self.dots:
            dot[0] += dot[2].x * dt
            dot[1] += dot[2].y * dt
            dot[2].y += 500 * dt
            if dot[1] > HEIGHT+5:
                self.dots.remove(dot)

    def draw(self):
        for dot in self.dots:
            pg.draw.circle(screen, self.color, (dot[0], dot[1]), 1)

    def __del__(self):
        pass

spawn_interval = random.random()*rain_amount+rain_amount

pg.mouse.set_visible(False)

mouse_image = pg.image.load("mouse.png").convert_alpha()
mouse_image_rect = mouse_image.get_rect()
mouse_mask = pg.mask.from_surface(mouse_image)

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    dt = clock.tick(FPS) / 1000.0
    time = pg.time.get_ticks()
    mouse_x, mouse_y = pg.mouse.get_pos()

    if time - last_spawn_time >= spawn_interval:
        raindrop_x = random.randint(0, int(WIDTH+HEIGHT))
        raindrop_y = 0
        rain_value_randomness = random.random()*value_randomness_factor
        rain_color = (rain_color_R-rain_color_R*rain_value_randomness, rain_color_G-rain_color_G*rain_value_randomness, rain_color_B-rain_color_B*rain_value_randomness)
        rain_self_speed = rain_speed + (random.random()*rain_speed_randomness-(rain_speed_randomness/2))
        raindrops.append([raindrop_x, raindrop_y, rain_self_speed, False, rain_color]) # random color value determination
        spawn_interval = random.random()*rain_amount+rain_amount
        last_spawn_time = time
    
    screen.fill(BACKGROUND_COLOR)

    for raindrop in raindrops:
        raindrop_mask = pg.mask.from_surface(pg.Surface((1, 1)))
        prev_pos = vec2(raindrop[0], raindrop[1])
        raindrop[1] += raindrop[2] * dt
        raindrop[0] -= horizontal_rain_velocity * dt
        raindrop_pos = vec2(raindrop[0], raindrop[1])
        pg.draw.aaline(screen, raindrop[4], vec2(raindrop_pos.x, raindrop_pos.y), vec2(raindrop_pos.x+((horizontal_rain_velocity*dt)/(raindrop_pos.y - prev_pos.y))*rain_length, raindrop_pos.y-rain_length), rain_width)
        if raindrop[1] > HEIGHT and not raindrop[3]:
            raindrop[3] = True
            splash = Splash(raindrop_pos.x, raindrop_pos.y, raindrop[4], 0)
            splashes.append(splash)
            raindrops.remove(raindrop)
        if raindrop_mask.overlap(mouse_mask, (mouse_x - raindrop_pos.x, mouse_y - raindrop_pos.y)) and not raindrop[3]:
            raindrop[3] = True
            if horizontal_rain_velocity > 0:
                splash = Splash(raindrop_pos.x, raindrop_pos.y, raindrop[4], 45)
            else:
                splash = Splash(raindrop_pos.x, raindrop_pos.y, raindrop[4], -90)
            splashes.append(splash)
            raindrops.remove(raindrop)

    for splash in splashes:
        splash.update(dt)
        splash.draw()

    screen.blit(mouse_image, (mouse_x, mouse_y))

    pg.display.flip()
pg.quit