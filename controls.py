class FlightControls():

    degree = 0.01745
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

        self.s_max = 28.0
        self.a_max = 360.0 / self.full_roll_s  / fps * self.degree
        self.b_max = 360.0 / self.full_pitch_s / fps * self.degree

        self.s_step = 2.0
        self.a_step = self.a_max / 16
        self.b_step = self.b_max / 16
        # print(self.a_step, self.b_step)
        
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
        self.speed = max(round( self.speed - self.s_step, 2), 0)
