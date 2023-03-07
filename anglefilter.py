import math
from math import sin, cos
from pygame import Vector2 as Vec

def pseudoangle(dx, dy):
    p = dx/(abs(dx)+abs(dy)) # -1 .. 1 increasing with x
    if dy < 0:
        return p - 1  # -2 .. 0 increasing with x
    else:
        return 1 - p  #  0 .. 2 decreasing with x

def inSight(playerDir, vecs):
    adjusted = [Vec(vec).rotate_rad(playerDir) for vec in vecs]
    
    return abs(pseudoangle(adjusted.x, adjusted.y)) < 0.8

# print(pseudoangle(1,0))
# print(pseudoangle(-1,0))
# print(pseudoangle(0,1))
# print(pseudoangle(0,-1))
angs = [(sin(x),cos(x)) for x in range(1,10)]
angs.sort(key=lambda x: pseudoangle(x[0],x[1]))
math.tan(0)
print(inSight(0, (0.1,0.71)))
