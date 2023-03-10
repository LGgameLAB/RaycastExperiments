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
           self.ang -= 0.01*delta
        if keys[pygame.K_LEFT]:
            self.ang += 0.01*delta
        
        if keys[pygame.K_a]:
            self.pos += (cos(self.ang+pi/2), sin(self.ang+pi/2))
        if keys[pygame.K_d]:
            self.pos += (cos(self.ang-pi/2), sin(self.ang-pi/2))
        
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

player = Player()
while True:
    clock.tick(60)
    win.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    player.update()

    origin = player.pos#Vec(pygame.mouse.get_pos())
    fovLim = [ (player.ang+radians(FOV/2)) % (2*math.pi) , (player.ang-radians(FOV/2)) % (2*math.pi)]
    angs = fovLim.copy()
    for poly in Map:
        poly.render(win)
        for p in poly.points:
            ang = atan2(p.y-origin.y, p.x-origin.x)
            for x in [-0.00001,0,0.00001]:
                angs.append(ang+x)
    
    print(fovLim)
    intersects = []
    for a in angs:
        collide = checkIntersect(origin, a)
        if collide:
            # pygame.draw.line(win, (190, 30, 30), mouse, collide)
            intersects.append((collide, a))

    # The intersects are stored with a point collision value and an angle (note that angle sorting will get awfully complicated)
    # intersects.append(((400, 250), atan2(250-origin.y, 270-origin.x)))
    intersects.sort(key=lambda x: x[1])
    
    Poly([i[0] for i in intersects], False, (0, 90, 200, 0.1)).render(win)
    
    # The code below finds finds the index values of the outermost ray projections 
    # I believe what this helps is finding the index values between the fov limits so the player only sees what it should
    indices = sorted([[intersects.index(i) for i in intersects if i[1] == fovLim[0]][0], [intersects.index(i) for i in intersects if i[1] == fovLim[1]][0]])

    # Draw the mini map and shift over points to right half of screen
    [pygame.draw.line(win, (40, 200, 30), player.pos+(winWidth, 0), i[0]+(winWidth, 0)) for i in intersects]
    
    poles = []
    #print(indices[0]-indices[1], len(intersects))
    for i in range(indices[0],indices[1]+1):
        poleHeight = max(winHeight/player.pos.distance_to(intersects[i][0]), 2)
        x = abs((intersects[i][1]-fovLim[0])/radians(FOV))*winWidth
        # print(x)
        poleRect = pygame.Rect(x, 0, 1, poleHeight)
        poleRect.centery = winHeight/2
        poles.append(poleRect)
        pygame.draw.line(win, (255,255,255), poleRect.midbottom, poleRect.topleft)
        pygame.draw.line(win, (240, 100, 30), player.pos+(winWidth, 0), intersects[i][0]+(winWidth, 0))

    for p in range(len(poles)-1):
        pygame.draw.line(win, (255,255,255), poles[p].midtop, poles[p+1].midtop)
        pygame.draw.line(win, (255,255,255), poles[p].midbottom, poles[p+1].midbottom)

    pygame.draw.circle(win, (5, 140, 34), pygame.mouse.get_pos(), 2)

    pygame.display.update()
