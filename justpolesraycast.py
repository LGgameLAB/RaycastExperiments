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
    def __init__(self, p1, p2, **kwargs): #takes in positional tuples etc. (10, 0) (0, 0)
        self.groups = ()
        self.color = (50, 255, 255)
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.point1 = Vec(p1)
        self.point2 = Vec(p2)
        self.points = [self.point1, self.point2]
        self.allPoints = []
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.render()

    
    def render(self):
        vec = self.point2-self.point1
        for x in range(1, 100):
            x1 = self.point1.x+vec.x*(x/100)
            y1 = self.point1.y+vec.y*(x/100)
            vec2 = Vec((x1, y1))
            self.allPoints.append(vec2)

        self.allPoints.append(self.point1)
        self.allPoints.append(self.point2)


class pole:
    def __init__(self, wall, dist, angle):
        self.wall = wall
        self.dist = dist
        self.angle = angle
    
    def render(self):
        poleHeight = max(stgs.winHeight - 30*self.dist, 1)
        poleRect = pygame.Rect((self.angle+stgs.FOV/2)/stgs.FOV*stgs.winWidth, 0, 1, poleHeight)
        poleRect.centery = stgs.winHeight/2
        return poleRect.topleft, poleRect.bottomleft

def get_point_poles(player, walls):
    poles = []
    if not player.dir.is_normalized():
        player.dir.normalize_ip()
        print("player dir is normalized")

    for wall in walls:
        for p in wall.allPoints:
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

            if abs(offSet) <= stgs.FOV/2:
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
    walls = [wall( (0, 0), (0, 10), color = (23, 200, 157) ), wall( (0, 10), (10, 10) ), wall( (10, 10), (10, 0) ), wall( (10, 0), (0, 0) )]
    p1 = player((1, 1), 0.1, 0.1)
    
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

        for p in get_point_poles(p1, walls):
            start, end = p.render() 
            pygame.draw.line(win, p.wall.color, start, end, 5)

        pygame.display.update()

game()
