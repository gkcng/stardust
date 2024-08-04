import numpy as np

import yaml
import math

import pygame

from stardust import Stardust, View
from controls import FlightControls
from renderer import Renderer
from unitcube import UnitCube
from camera   import Delta, Camera
from matrix import *

WIDTH =800
HEIGHT=600

def handle_keys(keys, d):
    if keys[pygame.K_UP      ]:
        d.set_delta(yo=+0.1)
    if keys[pygame.K_DOWN    ]:
        d.set_delta(yo=-0.1)
    if keys[pygame.K_RIGHT   ]:
        d.set_delta(xo=+0.1)
    if keys[pygame.K_LEFT    ]:
        d.set_delta(xo=-0.1)
    if keys[pygame.K_SPACE   ]:
        d.set_delta(zo=+0.1)
    if keys[pygame.K_SLASH   ]:
        d.set_delta(zo=-0.1)
    if keys[pygame.K_COMMA   ]:
        d.set_delta(r=+5)
    if keys[pygame.K_PERIOD  ]:
       d.set_delta(r=-5)
    if keys[pygame.K_s       ]:
        d.set_delta(p=+5)
    if keys[pygame.K_x       ]:
        d.set_delta(p=-5)
    if keys[pygame.K_RIGHTBRACKET ]:
        d.set_delta(y=+5)
    if keys[pygame.K_LEFTBRACKET  ]:
        d.set_delta(y=-5)

def display_help(screen, font, center):
    usages = [
        "UP, DOWN, LEFT, RIGHT - Move",
        "s / x - Pitch",
        "< / > - Roll",
        "[ / ] - Yaw",
        "h - Help toggle"
    ]

    for i in range(len(usages)):
        msg = usages[i]
        text = font.render(msg, True, (255, 255, 0))
        text_rect = text.get_rect(center=center)
        text_rect = text_rect.move(0, -(len(usages)/2*36)+i*36)
        screen.blit(text, text_rect)

def create_cubes(cubes):
    # The code quite comfortably maintain 132 cubes which is 1056 points @ 30 FPS
    # 90 cubes which is 720 points 
    left=-9
    front=1.5
    step=2
    for i in range(10):
        x = i*step+left
        for j in range(11):
            z = j*step+front
            cubes.append( UnitCube(x, 0.5, z) )
    return cubes

def main():

    pygame.init()
    pygame.display.set_caption("Stardust")

    screen   = pygame.display.set_mode((WIDTH, HEIGHT))
    font     = pygame.font.SysFont('Courier New, courier, monospace', 20, bold=True)
    fps      = 30

    controls = FlightControls(fps)
    paint    = Renderer(screen, WIDTH/2, HEIGHT/2)

    dt=0
    help_screen = False
    delta = Delta()

    cubes = create_cubes([])

    key_mappings = {
    }

    running = True
    clock = pygame.time.Clock()
    pygame.event.clear()
    
    # main loop
    while running:

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    help_screen = not help_screen
                elif event.key in key_mappings:
                    target_obj = key_mappings[event.key][0]
                    func = key_mappings[event.key][1]
                    func(target_obj)

        if help_screen:
            screen.fill((0, 0, 0))            
            display_help(screen, font, (WIDTH/2, HEIGHT/2))
            clock.tick(5)            
        else:
            # Handle keys pressed
            if dt == 0:
                handle_keys(pygame.key.get_pressed(), delta)
                # delta.set_delta(y=+2)
                # Update states
                if delta.changed:
                    paint.camera.set_camera_delta( d=delta )
                    delta.reset()
            
            #
            # Screen update cycle
            #
            screen.fill((0, 0, 0))
    
            paint.begin_draw()
            for cube in cubes:
                cube.update()
                cube.draw(paint)
            paint.end_draw()
    
            # it makes sense to throttle the framerate (which is what the 30 in
            # clock.tick(30) achieves) because it is pointless to have a framerate
            # higher than the screen refresh rate (which is usually 60). To run at
            # full speed, remove the 30
            clock.tick(30)
            text = font.render(f'fps: {clock.get_fps():.1f}; h - HELP', True, (255, 255, 0))
            screen.blit(text, (10, 10))
            
            dt = (dt + 1) % 2

        pygame.display.flip()        
        
if __name__ == '__main__':
    main()
