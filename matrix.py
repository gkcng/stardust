import math
import numpy as np

DEGREES = 0.0174533
epsilon=1.0e-6
sin = math.sin
cos = math.cos

def np_array(array):
    return np.array( array, dtype=np.float32 )

# Small angle approximations
#
#  sin a ~= a
#  cos a ~= 1 - (a^2 / 2) ~= 1
#  tan a ~= a
#
def roll_matrix(r):
    # roll - z axis
    return np_array([
        [cos(r), -sin(r), 0, 0],
        [sin(r),  cos(r), 0, 0],
        [     0,       0, 1, 0],
        [     0,       0, 0, 1],
    ])


def pitch_matrix(p):
    # pitch - x axis
    return np_array([
        [ 1,      0,       0, 0],
        [ 0, cos(p), -sin(p), 0],
        [ 0, sin(p),  cos(p), 0],
        [ 0,      0,       0, 1],
    ])


def yaw_matrix(y):
    # yaw  - y axis
    return np_array([
        [ cos(y), 0, sin(y), 0],
        [      0, 1,      0, 0],
        [-sin(y), 0, cos(y), 0],
        [     0,  0,      0, 1],
    ])

def composite_matrix(r, p, y, xo, yo, zo):
    c_r, s_r = cos(r), sin(r)
    c_p, s_p = cos(p), sin(p)
    c_y, s_y = cos(y), sin(y)

    return np_array([
        [  c_y*c_r+s_y*s_p*s_r,  c_y*-s_r+s_y*s_p*c_r,  s_y*c_p, xo],
        [              c_p*s_r,               c_p*c_r,     -s_p, yo],
        [ -s_y*c_r+c_y*s_p*s_r, -s_y*-s_r+c_y*s_p*c_r,  c_y*c_p, zo],
        [                    0,                     0,        0,  1]
    ])

def matmul(m1, m2):
    # return _matmul_long(m1, m2) # This is definiely slower, dropping framerate from 30 to 13
    return np.matmul(m1, m2)
  
def rot_matrix_short(r=0, p=0, y=0, xo=0, yo=0, zo=0):
    r *= DEGREES
    p *= DEGREES
    y *= DEGREES

    return composite_matrix(r, p, y, xo, yo, zo)

def _matmul_long(m1, m2):

    rows = 4
    columns = 4 if len(m2.shape) == 2 else 1

    m3 = np.zeros((rows, columns))

    for vsel in range(columns):
        for hsel in range(rows):
            cumul = 0
            for elem in range(4):
                val = m2[elem, vsel] if columns > 1 else m2[elem]
                cumul += m1[hsel,elem] * val
            m3[hsel,vsel] = cumul
                
    return m3.squeeze() if columns == 1 else m3

def rot_matrix(r=0, p=0, y=0, xo=0, yo=0, zo=0):

    r *= DEGREES
    p *= DEGREES
    y *= DEGREES

    roll = roll_matrix(r)
    pitch= pitch_matrix(p)
    yaw  = yaw_matrix(y)

    translation =  np_array([
        [     1,       0, 0, xo],
        [     0,       1, 0, yo],
        [     0,       0, 1, zo],
        [     0,       0, 0,  1],
    ])
    
    # Mvworld = T.R.S = Mvmodel
    # t,y,p,r
    result = matmul( matmul ( matmul( translation, yaw), pitch), roll)

    return result

