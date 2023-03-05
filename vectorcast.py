import pygame
import math
import settings as stgs

pygame.init()

def Vec(tup):
    return pygame.Vector2(tup)

class player(pygame.sprite.Sprite):
    def __init__(self, pos, w, h):
        self.rect = pygame.Rect(pos[0], pos[1], w ,h)
        self.dir = Vec((0.707107, 0.707107))
        self.pos = Vec(pos)

    def get_pos(self):
        return self.pos
    
    def get_angle(self):
        return math.degrees(math.atan2(-self.dir.y, self.dir.x))

    def move(self, speed):
        vel = 0.1*(self.dir*speed)
        self.pos += vel

class wall(pygame.sprite.Sprite):
    def __init__(self, p1, p2): #takes in positional tuples etc. (10, 0) (0, 0)
        self.groups = ()
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.point1 = Vec(p1)
        self.point2 = Vec(p2)
        self.points = [self.point1, self.point2]
    
    def render(self, win, poles):
        myPoles = []
        tops = []
        bottoms = []
        for p in poles:
            if p.wall == self:
                myPoles.append(p)
                tops.append(p.top)
                bottoms.append(p.bottom)
        
        if len(myPoles) > 1:
            if abs(myPoles[0].angle) > stgs.FOV/2 and abs(myPoles[1].angle) > stgs.FOV/2:
                pass
            else:
                if len(tops) > 1:
                    pygame.draw.line(win, (50, 255, 255), tops[0], tops[1], 1)
                    pygame.draw.line(win, (50, 255, 255), bottoms[0], bottoms[1], 1)

class pole:
    def __init__(self, wall, dist, angle):
        self.wall = wall
        self.dist = dist
        self.angle = angle
    
    def render(self):
        poleHeight = max(900-40*self.dist, 1)
        poleRect = pygame.Rect((self.angle+stgs.FOV/2)/stgs.FOV*stgs.winWidth, 0, 1, poleHeight)
        poleRect.centery = stgs.winHeight/2
        self.top, self.bottom = poleRect.topleft, poleRect.bottomleft
        return self.top, self.bottom

def get_point_poles(player, walls):
    poles = []
    if not player.dir.is_normalized():
        player.dir.normalize_ip()
        print("player dir is normalized")

    for wall in walls:
        for p in wall.points:
            pointAng = p-player.pos
            pointAng.normalize_ip()
            pointAng = math.degrees(math.atan2(-pointAng.y, pointAng.x)) + 180

            pAng = math.degrees(math.atan2(-player.dir.y, player.dir.x)) + 180
            offSet = pointAng - pAng

            if abs(offSet) > 180:
                if pAng >= 180:
                    offSet = (pointAng+360) - pAng
                else:
                    offSet = (pointAng-360) - pAng

            #if abs(offSet) <= stgs.FOV/2:
            poles.append( pole(wall, player.pos.distance_to(p), offSet) )
            

    returnList = []
    for x in range(0, len(poles)):
        val = max(poles, key=lambda k: k.angle)
        returnList.append(poles.pop(poles.index(val)))

    return returnList

def runEvents():
    ## Catch all events here
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
    
def game():
    win = pygame.display.set_mode((stgs.winWidth, stgs.winHeight))
    walls = [wall( (0, 0), (0, 10) ), wall( (0, 10), (10, 10) ), wall( (10, 10), (10, 0) ), wall( (10, 0), (0, 0) )]
    p1 = player((-1, -1), 0.1, 0.1)
    
    while True:
        pygame.time.delay(60)
        runEvents()
        win.fill((0, 0, 0))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            p1.dir.rotate_ip(5)
        if keys[pygame.K_d]:
            p1.dir.rotate_ip(-5)
        if keys[pygame.K_w]:
            p1.move(4)
        if keys[pygame.K_s]:
            p1.move(-4)
        if keys[pygame.K_RIGHT]:
            p1.pos += 0.4*p1.dir.rotate(-90)
        if keys[pygame.K_LEFT]:
            p1.pos += 0.4*p1.dir.rotate(90)

        poles = get_point_poles(p1, walls)
        for p in poles:
            start, end = p.render() 
            if abs(p.angle) <= stgs.FOV/2:
                pygame.draw.line(win, (50, 255, 255), start, end, 1)

        for w in walls:
            w.render(win, poles)

        pygame.display.update()

game()


