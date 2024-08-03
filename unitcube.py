import math
import numpy as np
from matrix import *

class UnitCube():
    vertices = np_array([
        [ -0.5, -0.5, -0.5, 1],
        [  0.5,  0.5, -0.5, 1],
        [  0.5, -0.5, -0.5, 1],
        [ -0.5,  0.5, -0.5, 1],

        [ -0.5, -0.5, 0.5, 1],
        [  0.5,  0.5, 0.5, 1],
        [  0.5, -0.5, 0.5, 1],
        [ -0.5,  0.5, 0.5, 1],
    ])
    
    verticesT = vertices.transpose()
    
    edges = [
        [ 0, 2 ],
        [ 0, 3 ],
        [ 2, 1 ],
        [ 3, 1 ],

        [ 0, 4 ], 
        [ 1, 5 ],
        [ 2, 6 ],
        [ 3, 7 ],

        [ 4, 6 ],
        [ 4, 7 ],
        [ 6, 5 ],
        [ 7, 5 ]

    ]

    def __init__(self, x, y, z):
        self.model_matrix = rot_matrix(xo=x, yo=y, zo=z)

    def update(self):
        deg = np.random.uniform(1,5) # A single value
        self.model_matrix = matmul(self.model_matrix, rot_matrix(r=deg,p=deg,y=0))
    
    def draw(self, painter):
        painter.push_matrix(self.model_matrix, "Model(Cube)")
        pv = painter.project(self.verticesT)

        colors = [(0,0,255),(90,90,0),(255,0,0)]
        count = 0
        for edge in self.edges:
            p1, p2 = edge
            # larger z is red, # sides is yellow, smaller z is blue
            color = colors[1]
            if count<4:
                color = colors[0] 
            elif count>=8:
                color = colors[2]
            painter.draw_line(pv[p1], pv[p2], color)
            count+=1
        painter.pop_matrix()

