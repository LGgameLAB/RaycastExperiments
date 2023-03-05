import pygame

class Poly:
    def __init__(self, points, noFill=True, color=(255,255,255)):
        self.points = [Vec(p) for p in points]
        self.faces = []
        for p in range(len(points)):
            self.faces.append((self.points[p-1],self.points[p]))
        self.noFill = noFill
        self.color = color

    def render(self,win):
        pygame.draw.polygon(win, self.color, self.points, ) if self.noFill else pygame.draw.polygon(win, self.color, self.points)


Map = [Poly([(90,120),(90,150),(120,120)]), Poly([(320,320),(370,210),(210,420)]),Poly([(0,0),(winWidth-1,0), (winWidth-1, winHeight-1), (0, winHeight-1)])]
