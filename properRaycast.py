import pygame
import math
from math import atan2, cos, sin, radians, pi
from settings import *

pygame.init()

win = pygame.display.set_mode((winWidth*2, winHeight))
clock = pygame.time.Clock()

class Player:
    def __init__(self, start=(winWidth/2, winHeight/2)):
        self.pos = Vec(start)
        self.ang = radians(0)
    
    def update(self):
        self.move()
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.pos += (cos(self.ang), sin(self.ang))
        if keys[pygame.K_DOWN]:
            self.pos -= (cos(self.ang), sin(self.ang))
        if keys[pygame.K_RIGHT]:
           self.ang += 0.05*delta
        if keys[pygame.K_LEFT]:
            self.ang -= 0.05*delta
        
        if keys[pygame.K_a]:
            self.pos -= (cos(self.ang+pi/2), sin(self.ang+pi/2))
        if keys[pygame.K_d]:
            self.pos -= (cos(self.ang-pi/2), sin(self.ang-pi/2))
        
        global FOV
        
        if keys[pygame.K_z]:
            FOV += 1
        if keys[pygame.K_x]:
            FOV -= 1
        # if keys[pygame.K_UP]:
        #     self.pos.y -= 1*delta
        # if keys[pygame.K_DOWN]:
        #     self.pos.y += 1*delta
        # if keys[pygame.K_RIGHT]:
        #     self.pos.x += 1*delta
        # if keys[pygame.K_LEFT]:
        #     self.pos.x -= 1*delta
        
        # if keys[pygame.K_a]:
        #     self.ang -= 0.01*delta
        # if keys[pygame.K_d]:
    #     self.ang += 0.01*delta

# Nice little object to store the polygon information on the map
class Poly:
    def __init__(self, points, noFill=True, color=(255,255,255)):
        self.points = [Vec(p) for p in points]
        self.faces = []
        for p in range(len(points)):
            self.faces.append((self.points[p-1],self.points[p]))
        self.noFill = noFill
        self.color = color

    def render(self,win):
        pts2 = [p + (winWidth, 0) for p in self.points]
        pygame.draw.polygon(win, self.color, pts2, 1) if self.noFill else pygame.draw.polygon(win, self.color, pts2)

# Given the angle of the ray and position of the player, returns the first collision point with the map
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
        # Returns closest collision
        collides.sort(key=lambda p: origin.distance_to(p))
        return collides[0]

# This stores the information for the "colliders" on the map
Map = [Poly([(90,120),(90,150),(120,120)]), Poly([(320,320),(370,210),(210,420)]),Poly([(0,0),(winWidth-1,0), (winWidth-1, winHeight-1), (0, winHeight-1)])]
for x in range(40,200, 10):
    Map.append(Poly([(x, 20), (x+4, 20), (x+4, 80), (x, 80)]))

quality = 100
player = Player()
correct = 1
while True:
    clock.tick(60)
    win.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    player.update()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        correct = 0 if correct else 1

    origin = player.pos
    intersects = []
    step = math.radians(FOV)/quality
    for i in range(1,quality+1):
        ang = player.ang-math.radians(FOV/2) + step*i
        collide = checkIntersect(origin, ang)
        # This "if" is solely error-proofing
        if collide:
            intersects.append((collide, ang))
            dist = player.pos.distance_to(collide)
            correction = math.cos(ang - player.ang)**correct
            print(ang - player.ang)
            poleHeight = max(winHeight/(dist*correction), 2)
            poleRect = pygame.Rect(winWidth/quality*i, 0, winWidth/quality, poleHeight)
            poleRect.centery = winHeight/2
            col = min(255, 255/(dist*0.1))
            pygame.draw.rect(win, (col, col, col), poleRect)

    # The intersects are stored with a point collision value and an angle (note that angle sorting will get awfully complicated)
    
    # Draw the mini map and shift over points to right half of screen
    for p in Map:
        p.render(win)
    [pygame.draw.line(win, (40, 200, 30), player.pos+(winWidth, 0), i[0]+(winWidth, 0)) for i in intersects]
    print(correct)
    pygame.display.update()
