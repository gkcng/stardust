from enum import Enum
import pygame
import numpy as np
from numpy.random import random, randint

WIDTH =800
HEIGHT=600
np.seterr(all='raise') # For development

class View(Enum):
    FRONT = 1
    REAR  = 2
    LEFT  = 3
    RIGHT = 4
    
class Stardust():
    
    max_dust_z    = 500
    num_dusts     = 15
    epsilon       = 1e-10

    def __init__(self, width, height):
        self.width, self.height      = width, height
        self.origin_x, self.origin_y = np.rint(width/2), np.rint(height/2)
        self.qtr_x, self.qtr_y       = np.rint(width/4), np.rint(height/4)
        self.set_view(View.FRONT)
        
    def set_view(self, view):
        self.travel_view = view
        self.reset_dusts()
        
    def reset_dusts(self):
        self.dusts      = np.array([ self.spawn_dust() for i in range( self.num_dusts )])

    def spawn_dust(self):
        # dusts can orginate anywhere on the screen
        w, h, z, ox, oy = self.width, self.height, self.max_dust_z, self.origin_x, self.origin_y
        nums = np.random.rand(3) * [w, h, z] - [ox, oy, 0]
        nums = np.append( nums, 1) # For matrix multiplication
        return np.rint(nums).astype(int) 

    def is_off_screen(self, dust):
        return any([
        dust[0] >  self.origin_x -1,
        dust[0] <= self.origin_x*-1,
        dust[1] >  self.origin_y -1,
        dust[1] <= self.origin_y*-1,
        dust[2] >  self.max_dust_z,
        dust[2] < 1
    ])

    def _move_dust(self, dust, alpha, beta, speed):
        nd = dust
        x, y, z, _ = dust
        z += self.epsilon # Prevent DBZ
        x += self.epsilon # Prevent DBZ

        s  = speed * -1 if self.travel_view == View.REAR else speed
        r_mod = -1 if self.travel_view == View.REAR or self.travel_view == View.RIGHT else 1

        if self.travel_view in (View.FRONT, View.REAR):

            x_roll = -alpha * y * 2.4 * r_mod
            y_roll =  alpha * x * 2.4 * r_mod
            x_pitch = 2 * pow(beta * y / 256, 2)
            y_pitch = -beta * 1024 * r_mod
            q = s / z + 1

            matrix = np.array([
                [q, 0,   0, 0],
                [0, q,   0, 0],
                [0, 0, 1/q, 0],
                [x_roll + x_pitch, y_roll + y_pitch, 0, 1]
            ])

        else:
            # Different to https://elite.bbcelite.com/            
            x_roll  =  0 
            y_roll  = -alpha * 1024 * r_mod
            
            x_pitch =  beta * y * r_mod
            y_pitch = -beta * x * r_mod
            d = -128 * s / z  * r_mod
            
            matrix = np.array([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [d + x_roll + x_pitch, y_roll + y_pitch, 0, 1]
            ])

        nd = np.rint(np.matmul(dust, matrix)).astype(int)

        if self.is_off_screen(nd):
            nd = self.spawn_dust()

        return nd
        
    def move_dusts(self, alpha, beta, speed):
        for i in range(len(self.dusts)):
            nd = self._move_dust( self.dusts[i], alpha, beta, speed )
            self.dusts[i] = nd
            
    def get_dust_size(self, dust):
        return 5/self.max_dust_z *(self.max_dust_z-dust[2])

class FlightControls():

    degree = 0.0175
    full_pitch_s = 12
    full_roll_s  = 6
    
    def __init__(self, fps):
        """
        pitch:= 12 seconds per full rotation 360
              = 30 deg per second
              = 1 deg / frame at 30 fps

        roll := 6 seconds per full rotation 360
              = 60 per second
              = 2 deg / frame at 30 fps
        """
        
        self.speed = 10.0
        self.alpha = 0.0
        self.beta  = 0.0 

        self.s_max = 10.0
        self.a_max = 360.0 / self.full_roll_s  / fps * self.degree
        self.b_max = 360.0 / self.full_pitch_s / fps * self.degree

        self.s_step = 0.5
        self.a_step = self.a_max / 16
        self.b_step = self.b_max / 16
        print(self.a_step, self.b_step)
        
    def roll_left(self):
        self.alpha = min(round(self.alpha + self.a_step, 5), self.a_max) if self.alpha >= 0 else 0
        
    def roll_right(self):
        self.alpha = max(round(self.alpha - self.a_step, 5), -self.a_max) if self.alpha <= 0 else 0

    def pitch_up(self):
        self.beta = max(round(self.beta - self.b_step, 5), -self.b_max) if self.beta <= 0 else 0

    def pitch_down(self):
        self.beta = min(round( self.beta + self.b_step, 5), self.b_max) if self.beta >= 0 else 0

    def faster(self):
        self.speed = min(round( self.speed + self.s_step, 2), self.s_max)

    def slower(self):
        self.speed = max(round( self.speed - self.s_step, 2), self.s_step)

def main():

    pygame.init()
    pygame.display.set_caption("Stardust")

    screen   = pygame.display.set_mode((WIDTH, HEIGHT))
    stardust = Stardust(WIDTH, HEIGHT)
    center   = np.array([stardust.origin_x, stardust.origin_y, 0, 0])
    font     = pygame.font.SysFont('Courier New, courier, monospace', 20, bold=True)
    fps = 30
    controls = FlightControls(fps)
    
    running = True
    clock = pygame.time.Clock()
    text = font.render('fps: ?', False, (255, 255, 0))
    pygame.event.clear()

    key_mappings = {
        pygame.K_1:      [ stardust, lambda s: s.set_view(View.FRONT) ],
        pygame.K_2:      [ stardust, lambda s: s.set_view(View.REAR) ],
        pygame.K_3:      [ stardust, lambda s: s.set_view(View.LEFT) ],
        pygame.K_4:      [ stardust, lambda s: s.set_view(View.RIGHT) ],
        pygame.K_COMMA:  [ controls, lambda c: c.roll_left() ],
        pygame.K_PERIOD: [ controls, lambda c: c.roll_right() ],
        pygame.K_s:      [ controls, lambda c: c.pitch_down() ],
        pygame.K_x:      [ controls, lambda c: c.pitch_up() ],
        pygame.K_SPACE:  [ controls, lambda c: c.faster() ],
        pygame.K_SLASH:  [ controls, lambda c: c.slower() ],
    }
    
    # main loop
    while running:

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue
            elif event.type == pygame.KEYDOWN:
                if event.key in key_mappings:
                    target_obj = key_mappings[event.key][0]
                    func = key_mappings[event.key][1]
                    func(target_obj)
        
        # Update states
        stardust.move_dusts(controls.alpha, controls.beta, controls.speed)
        
        #
        # Screen update cycle
        #
        screen.fill((0, 0, 0))
        pixels = pygame.surfarray.pixels3d(screen)        
        screen_points = stardust.dusts + center
        for p in screen_points:
            pygame.draw.circle(screen, (255,255,255), (p[0],p[1]), stardust.get_dust_size(p) )
        del pixels

        # it makes sense to throttle the framerate (which is what the 30 in
        # clock.tick(30) achieves) because it is pointless to have a framerate
        # higher than the screen refresh rate (which is usually 60). To run at
        # full speed, remove the 30
        clock.tick(30)
        text = font.render(f'fps: {clock.get_fps():.1f}, view: {stardust.travel_view.name}, s: {controls.speed}, a: {controls.alpha}, b: {controls.beta}', True, (255, 255, 0))
        screen.blit(text, (10, 10))
        
        # pygame.display.update()        
        pygame.display.flip()


if __name__ == '__main__':
    main()

