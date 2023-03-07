import pygame
from math import atan2, cos, sin, radians
from settings import *

pygame.init()
win = pygame.display.set_mode((winWidth, winHeight))
clock = pygame.time.Clock()

class Poly:
    def __init__(self, points, noFill=True, color=(255,255,255)):
        self.points = [Vec(p) for p in points]
        self.faces = []
        for p in range(len(points)):
            self.faces.append((self.points[p-1],self.points[p]))
        self.noFill = noFill
        self.color = color

    def render(self,win):
        if len(self.points) > 2:
            pygame.draw.polygon(win, self.color, self.points, 2) if self.noFill else pygame.draw.polygon(win, self.color, self.points)


Map = [Poly([(160,470),(60,300),(120,470)]), Poly([(60,270),(60,150),(120,270)]), Poly([(90,120),(90,150),(120,120)]), Poly([(320,320),(370,210),(210,420)]),Poly([(0,0),(winWidth-1,0), (winWidth-1, winHeight-1), (0, winHeight-1)])]
print(Map[0].faces)

def checkIntersect(origin, ang):
    global Map

    x,y = origin
    dx, dy = cos(ang), sin(ang)
    collides = []
    for poly in Map:
        for f in poly.faces:
            try:
                sx, sy = f[0]
                sdx, sdy = f[1]-f[0]
                t2 = (dx*(sy-y) + dy*(x-sx))/(sdx*dy - sdy*dx)
                t1 = (sx+sdx*t2-x)/dx
                if t1 >= 0 and t2 >= 0 and t2 <= 1:
                    collides.append(Vec((x+dx*t1, y+dy*t1)))
            except ZeroDivisionError:
                continue

    if len(collides) == 0:
        return False  
    else:
        collides.sort(key=lambda x: origin.distance_to(x))
        return collides[0]


while True:
    clock.tick(60)
    win.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    mouse = Vec(pygame.mouse.get_pos())
    fovLim = [radians(45)+radians(FOV/2), radians(45)-radians(FOV/2)]
    angs = fovLim.copy()
    for poly in Map:
        poly.render(win)
        for p in poly.points:
            ang = atan2(p.y-mouse.y, p.x-mouse.x)
            for x in [-0.00001,0,0.00001]:
                angs.append(ang+x)
    
    # angs = [135]
    # print(mouse)
    intersects = []
    for a in angs:
        collide = checkIntersect(mouse, a)
        if collide:
            intersects.append((collide, a))

    intersects.sort(key=lambda x: x[1])

    Poly([i[0] for i in intersects], False, (0, 90, 200, 0.1)).render(win)
    [pygame.draw.line(win, (40, 200, 30), mouse, i[0]) for i in intersects]
    pygame.draw.circle(win, (5, 140, 34), pygame.mouse.get_pos(), 2)

    pygame.display.update()
