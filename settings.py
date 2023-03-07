import pygame
winWidth, winHeight = 500, 500
FPS = 60
delta = 60/FPS
FOV = 90


def dist(vec1, vec2):
    dist1 = (vec1.x-vec2.x)**2
    dist2 = (vec1.y-vec2.y)**2
    return math.sqrt(dist1+dist2)

def Vec(tup):
    return pygame.Vector2(tup)
