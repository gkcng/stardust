import math
from numpy.linalg import inv

from matrix import *

class Camera():

    def __init__(self):

        self.camera = c = {
            'roll'     : 0, # degrees,
            'pitch'    : 30, # degrees,
            'yaw'      : 0, # degrees,
            'x_offset' : 0,
            'y_offset' : 3, # 0.5,
            'z_offset' : 2, # 13.5
        }
        self.camera_matrix = None
        
        self.cal_camera_matrix(
           rot_matrix(r=c['roll'], p=c['pitch'], y=c['yaw'],
                      xo=c['x_offset'], yo=c['y_offset'], zo=c['z_offset'])
        )


    def cal_camera_matrix(self, delta_matrix):
        """
        Camera/View Space := v_camera = V⋅M⋅v_model
        """
        # V = = C−1 - inverse
        self.camera_matrix = delta_matrix if self.camera_matrix is None else matmul(self.camera_matrix, delta_matrix)

        # Inverse
        # linalg inv is very CPU intensive unless setting this in the environment: $ export OPENBLAS_NUM_THREADS=1        
        self.view_matrix   = inv(self.camera_matrix) 

        self.camera_changed = True       


    def set_camera_delta(self,
                         r_delta=0, p_delta=0, y_delta=0,
                         xo_delta=0, yo_delta=0, zo_delta=0,
                         d=None):
        if d is not None:
            r_delta = d.r_delta
            p_delta = d.p_delta
            y_delta = d.y_delta
            xo_delta = d.xo_delta
            yo_delta = d.yo_delta
            zo_delta = d.zo_delta

        if any([r_delta != 0, 
                p_delta != 0, 
                y_delta != 0, 
                xo_delta != 0, 
                yo_delta != 0, 
                zo_delta != 0]):
            delta = rot_matrix(r= r_delta, 
                               p= p_delta,
                               y= y_delta,
                               xo= xo_delta,
                               yo= yo_delta,
                               zo= zo_delta)        

            self.cal_camera_matrix(delta)
        
    def get_view_matrix(self):
        self.camera_changed = False
        return self.view_matrix

    def view_has_changed(self):
        """Since last get_view_matrix()"""
        return self.camera_changed
    

class Delta():

    def __init__(self):
        self.reset()

    def reset(self):
        self.r_delta  = 0
        self.p_delta  = 0
        self.y_delta   = 0
        self.xo_delta = 0
        self.yo_delta = 0
        self.zo_delta = 0
        self.changed = False

    def set_delta(self, r=0, p=0, y=0, xo=0, yo=0, zo=0):
        if r != 0:
            self.r_delta = r
            self.changed = True
        if p != 0:
            self.p_delta = p
            self.changed = True
        if y != 0:
            self.y_delta = y
            self.changed = True
        if xo != 0:
            self.xo_delta = xo
            self.changed = True
        if yo != 0:
            self.yo_delta = yo
            self.changed = True
        if zo != 0:
            self.zo_delta = zo
            self.changed = True
            
