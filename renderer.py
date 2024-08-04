import math
import numpy as np
import pygame

from matrix import *
from camera import Camera

class Renderer():

    def __init__(self, screen, origin_x, origin_y):
        """
        Every point must be transformed from local model coordinates into screen coordinates.
        
        First transforming a vertex into clip space: vclip = P⋅V⋅M⋅v
        A vertex position is transformed by a model matrix (to world space), then a view matrix (to camera space),
        followed by a projection matrix (to clip space), hence the name Model View Projection, or MVP

        Then, performs perspective division, dividing the [x,y,z] components by the w value turning the 4D vector back
        into a 3D vector, resulting in the vertex finally being in normalized device coordinates.

        Finally, turn the normalized device coordinates into screen coordinates for rendering.
        """

        self.screen   = screen
        self.origin_x = origin_x
        self.origin_y = origin_y

        self.stack          = [] # Storing a stack of transformation matrices
        self.depth          = 0  # Number of matrices in the stack

        self.render_matrix  = None # The current composite transformation matrix
        self.last_render    = []   # Previous composite transformation matrices to restore during stack pops

        #
        # Camera. View Matrix
        #
        self.camera = Camera()
        
        #
        # Perspective Projection Matrix
        #
        n = self.near = 1
        f = self.far  = 1000
        aspect = origin_x / origin_y
        fov = 60*DEGREES
        self.set_perspective_projection_matrix(n, f, aspect, fov)

        #
        # Device Matrix - Maps the near window / portal to screen
        #
        self.set_device_projection_matrix( origin_x, origin_y )

        # self._test_matrices()


    def set_device_projection_matrix(self, w, h):
        self.device = np_array([
            [-w,  0,  0,       w],
            [ 0,  h,  0,       h],
            [ 0,  0,  1,       0],
            [ 0,  0,  0,       1],
        ])
        # The two transformations will make +Y Up, +X Right, +Z Into Screen
        # self.device = matmul(self.device, rot_matrix(r=180))

        
    def set_perspective_projection_matrix(self, n, f, aspect, fov):

        e = 1 / math.tan(fov / 2)
        t = n * math.tan(fov / 2)
        r = aspect * t

        # Equivalent:
        # self.perspective = np.array([
        #    [ n/r,          0,             0,            0 ],
        #    [   0,        n/t,             0,            0 ],
        #    [   0,          0,   (f+n)/(n-f), (2*f*n)/(f-n)], # Note the signs of m22 and m23
        #    [   0,          0,            -1,            0 ],
        # ])

        self.perspective = np_array([
           [ e/aspect,     0,             0,            0 ],
           [   0,          e,             0,            0 ],
           [   0,          0,   (f+n)/(n-f),  2*f*n/(f-n) ], # Note the signs of m22 and m23
           [   0,          0,            -1,            0 ],
        ])

        self.push_matrix(self.perspective, "Perspective") # Perspective Views


    def _test_matrices(self):
        print("Perspective\n", self.perspective)
        vT = np_array([
            [0,0,self.far,1],
            [0,0,self.near,1]
        ]).transpose()
        print(vT)
        vC=matmul(self.perspective, vT)
        print("Projected\n",np.round(vC/vC[3,], 3))


    def cal_render_matrix(self):
        if self.depth == 1:
            self.render_matrix = self.stack[0]
        elif self.depth > 1:
            b = None        
            for s in reversed(self.stack):
                b = s if b is None else matmul(s, b)
            self.render_matrix = b


    def push_matrix(self, matrix, label=None):
        if label and False:
            print("Push ", label)
        self.stack.append(matrix)
        if self.render_matrix is not None:
            self.last_render.append(self.render_matrix)
        self.depth +=1
        self.cal_render_matrix()


    def pop_matrix(self):
        m = self.stack.pop()
        self.depth -= 1
        if self.depth > 1:
            self.render_matrix = self.last_render.pop()
        # return m

        
    def begin_draw(self):
        if self.camera.view_has_changed():
          if self.depth == 2: # Lazy pop; Handle a previous View Matrix
              self.pop_matrix()
          self.push_matrix(self.camera.get_view_matrix(), label="View")
        return
    
    def end_draw(self):        
        # Lazy pop handle in begin_draw
        # no need to change if the view matrix hasn't changed
        # self.pop_matrix()
        return

    def project(self, vectors):
        """
        matmul render_matrix against the vertices in bulk.
        vertices shall be in column format (4, <num_vertices>)
        returns results after perspective division in device coords
        """
        v = np.copy(vectors)
        # Add a small z to avoid division by zero
        v[2,:] += epsilon
        q = matmul(self.render_matrix, v)
        q = q / q[(3,)] # perspective division
        s = matmul(self.device, q)

        return s.transpose()
        
    def draw_line(self, v1, v2, color=(255,255,255)):

        # Clipping
        if v1[2] < -1 or v2[2] < -1 or v1[2] > 1 or v2[2] > 1: 
            return  # Do not draw

        s1 = np.rint(v1[:2]).astype(int)
        s2 = np.rint(v2[:2]).astype(int)

        pygame.draw.line(self.screen, color, s1, s2, 2)


    def draw_point(self, pt=[0,0,0,1], color=(255,255,255)):
        p1 = np.rint( matmul(self.render_matrix, pt)).astype(int)
        pygame.draw.circle(self.screen, color, p1[:2], 2)

