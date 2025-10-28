import pygame as pg
import random

pg.init()
WIDTH, HEIGHT = 1920, 1080
FPS = 60
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
RAIN_LENGTH = 10
RAIN_WIDTH = 1
RAIN_SPEED = 500
RAIN_AMOUNT = 5 # less is more
RAIN_SPEED_RANDOMNESS = 0.25
HORIZONTAL_RAIN_VELOCITY = -250 # negative is left, positive is right
RAIN_COLOR_R, RAIN_COLOR_G, RAIN_COLOR_B = 255, 255, 255
color_by_depth_factor = 0.25
uhhhh_idk = 0.98
DIM_REFLECTION = 0.5
ENABLE_REFLECTIONS = True

class Splash():
    def __init__(self, x, y, color, rotation, depth, do_spawn_wave):
        self.x = x
        self.y = y
        self.dots = []
        self.color = color
        self.spawn_time = pg.time.get_ticks()
        self.depth = depth
        self.do_spawn_wave = do_spawn_wave
        if self.do_spawn_wave:
            self.waves = []
            self.waves.append([self.x, self.y, 0, 0, 0.25, 100*dt, 0, 50, self.color])
        self.depth_for_color = 1-(self.depth*color_by_depth_factor)
        for i in range(random.randint(2, 4)):
            if rotation!=0:splash_rotation = vec2((random.random()*2-1)*50, -100).rotate(rotation)
            else:splash_rotation = vec2((random.random()*2-1)*100+HORIZONTAL_RAIN_VELOCITY/2, -100).rotate(rotation)
            dot = [self.x, self.y-2, splash_rotation]
            self.dots.append(dot)

    def update(self, dt):
        if self.do_spawn_wave:
            for wave in self.waves:
                wave[2] += wave[5]
                wave[3] = wave[2]*wave[4]
                wave[6] += 1
                wave[8] = (RAIN_COLOR_R*self.depth_for_color*(1-(wave[6]/wave[7])), RAIN_COLOR_G*self.depth_for_color*(1-(wave[6]/wave[7])), RAIN_COLOR_B*self.depth_for_color*(1-(wave[6]/wave[7])))
                if wave[6] > wave[7]:
                    self.waves.remove(wave)

        for dot in self.dots:
            dot[0] += dot[2].x * dt
            dot[1] += dot[2].y * dt
            dot[2].y += 500 * dt
        self.dots = [dot for dot in self.dots if dot[1] <= HEIGHT*(depth*(1-uhhhh_idk)+uhhhh_idk)]

    def draw(self):
        if self.do_spawn_wave:
            for wave in self.waves:
                pg.draw.ellipse(screen, wave[8], (wave[0]-wave[2]/2, wave[1]-wave[3]/2, wave[2], wave[3]), 1)
        for dot in self.dots:
            pg.draw.circle(screen, self.color, (dot[0], dot[1]), 1)

#        if ENABLE_REFLECTIONS:
#            if self.do_spawn_wave:
#                for wave in self.waves:
#                    pg.draw.ellipse(screen, wave[8], (wave[0]-wave[2]/2, wave[1]-wave[3]/2, wave[2], wave[3]), 1)
#            for dot in self.dots:
#                pg.draw.circle(screen, self.color, (dot[0], dot[1]), 1)
                

    def __del__(self):
        pass

spawn_interval = random.random()*RAIN_AMOUNT+RAIN_AMOUNT

pg.mouse.set_visible(False)

mouse_image = pg.image.load("mouse.png").convert_alpha()
mouse_image_rect = mouse_image.get_rect()
mouse_mask = pg.mask.from_surface(mouse_image)

RAINDROP_MASK = pg.mask.from_surface(pg.Surface((1, 1)))

while run:
    fall_time = HEIGHT / (RAIN_SPEED*dt)
    horizontal_range = int(abs(HORIZONTAL_RAIN_VELOCITY*dt) * fall_time)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    dt = clock.tick(FPS) / 1000.0
    time = pg.time.get_ticks()
    mouse_x, mouse_y = pg.mouse.get_pos()

    if time - last_spawn_time >= spawn_interval:
        if HORIZONTAL_RAIN_VELOCITY < 0:
            raindrop_x = random.randint(0, int(WIDTH+horizontal_range))
        elif HORIZONTAL_RAIN_VELOCITY > 0:
            raindrop_x = random.randint(-horizontal_range, WIDTH)
        else:
            raindrop_x = random.randint(0, WIDTH)
        depth = random.random()
        depth_for_color = depth*color_by_depth_factor
        raindrop_y = 0
        rain_color = (RAIN_COLOR_R-RAIN_COLOR_R*depth_for_color, RAIN_COLOR_G-RAIN_COLOR_G*depth_for_color, RAIN_COLOR_B-RAIN_COLOR_B*depth_for_color)
        rain_self_speed = RAIN_SPEED + (random.random()*RAIN_SPEED_RANDOMNESS-(RAIN_SPEED_RANDOMNESS/2))
        raindrops.append([raindrop_x, raindrop_y, rain_self_speed, False, rain_color, depth]) # random color value determination
        spawn_interval = random.random()*RAIN_AMOUNT+RAIN_AMOUNT
        last_spawn_time = time
    
    screen.fill(BACKGROUND_COLOR)

    raindrops_to_remove = []
    for raindrop in raindrops:
        prev_pos = vec2(raindrop[0], raindrop[1])
        raindrop[1] += raindrop[2] * dt
        raindrop[0] += HORIZONTAL_RAIN_VELOCITY * dt
        raindrop_pos = vec2(raindrop[0], raindrop[1])
        pg.draw.aaline(screen, raindrop[4], vec2(raindrop_pos.x, raindrop_pos.y), vec2(raindrop_pos.x-((HORIZONTAL_RAIN_VELOCITY*dt)/(raindrop_pos.y - prev_pos.y))*RAIN_LENGTH, raindrop_pos.y-RAIN_LENGTH), RAIN_WIDTH)
        if raindrop[1] > HEIGHT*(raindrop[5]*(1-uhhhh_idk)+uhhhh_idk) and not raindrop[3]:
            raindrop[3] = True
            splash = Splash(raindrop_pos.x, raindrop_pos.y, raindrop[4], 0, raindrop[5], True)
            splashes.append(splash)
            raindrops_to_remove.append(raindrop)
        if abs(mouse_x - raindrop[0]) < 12 and abs(mouse_y - raindrop[1]) < 19:
            if RAINDROP_MASK.overlap(mouse_mask, (mouse_x - raindrop[0], mouse_y - raindrop[1])) and not raindrop[3]:
                raindrop[3] = True
                if HORIZONTAL_RAIN_VELOCITY <= 0 :
                    splash = Splash(raindrop_pos.x, raindrop_pos.y, raindrop[4], 45, raindrop[5], False)
                else:
                    splash = Splash(raindrop_pos.x, raindrop_pos.y, raindrop[4], -90, raindrop[5], False)
                splashes.append(splash)
                raindrops_to_remove.append(raindrop)
    raindrops = [r for r in raindrops if r not in raindrops_to_remove]

    for splash in splashes:
        splash.update(dt)
        splash.draw()

    screen.blit(mouse_image, (mouse_x, mouse_y))

    pg.display.flip()
pg.quit