import pygame
from math import atan2, cos, sin, radians, pi
from settings import *

pygame.init()

win = pygame.display.set_mode((winWidth, winHeight))
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

class Poly:
    def __init__(self, points, noFill=True, color=(255,255,255)):
        self.points = [Vec(p) for p in points]
        self.faces = []
        for p in range(len(points)):
            self.faces.append((self.points[p-1],self.points[p]))
        self.noFill = noFill
        self.color = color

    def render(self,win):
        pygame.draw.polygon(win, self.color, self.points, 1) if self.noFill else pygame.draw.polygon(win, self.color, self.points)

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
    fovLim = [player.ang+radians(FOV/2), player.ang-radians(FOV/2)]
    angs = fovLim.copy()
    for poly in Map:
        # poly.render(win)
        for p in poly.points:
            ang = atan2(p.y-origin.y, p.x-origin.x)
            for x in [-0.00001,0,0.00001]:
                angs.append(ang+x)
    
    # angs = [135]

    intersects = []
    for a in angs:
        collide = checkIntersect(origin, a)
        if collide:
            # pygame.draw.line(win, (190, 30, 30), mouse, collide)
            intersects.append((collide, a))

    # intersects.append(((400, 250), atan2(250-origin.y, 270-origin.x)))
    # print(intersects)
    intersects.sort(key=lambda x: x[1])
    
    
    # print([i[1] for i in intersects])
    indices = sorted([[intersects.index(i) for i in intersects if i[1] == fovLim[0]][0], [intersects.index(i) for i in intersects if i[1] == fovLim[1]][0]])

    poles = []
    print(indices[0]-indices[1], len(intersects))
    for i in range(indices[0],indices[1]+1):
        poleHeight = max(winHeight - 4*(min(player.pos.distance_to(intersects[i][0]), 550)), 2)
        x = abs((intersects[i][1]-fovLim[0])/radians(FOV))*winWidth
        # print(x)
        poleRect = pygame.Rect(x, 0, 1, poleHeight)
        poleRect.centery = winHeight/2
        poles.append(poleRect)
        pygame.draw.line(win, (255,255,255), poleRect.midbottom, poleRect.topleft)
    
    for p in range(len(poles)-1):
        pygame.draw.line(win, (255,255,255), poles[p].midtop, poles[p+1].midtop)
        pygame.draw.line(win, (255,255,255), poles[p].midbottom, poles[p+1].midbottom)


    pygame.draw.circle(win, (5, 140, 34), pygame.mouse.get_pos(), 2)

    pygame.display.update()