import math
class Vertex:
    def __init__(self, canvas, x, y, radius):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.handleNum = 0
        self.connectedVerticies = []

    def updateCoords(self, coords):
        (x,y) = coords
        self.x = x
        self.y = y

        
    def render(self):
        self.drawConnections()
        self.canvas.create_oval(self.x - self.radius,
                                self.y - self.radius,
                                self.x + self.radius,
                                self.y + self.radius,
                                tag = ("vert"),
                                fill = "White")
        #Need additional checks to make sure the oval is grabbed,
        #not a line. (Which can happen if two verts are overlapping)
        self.handleNum = self.canvas.find_enclosed(self.x - self.radius*2,
                                                   self.y - self.radius*2,
                                                   self.x + self.radius*2,
                                                   self.y + self.radius*2)[0]
        

    def drawConnections(self):
        for vert in self.connectedVerticies:
            #Need to catch div by 0
            theta = 0
            try:
                theta = math.atan( (vert.getY() - self.y) / (vert.getX() - self.x) )
            except:
                theta = 0

            if self.x == vert.getX():
                if self.y > vert.getY():
                    #vert is directly above self
                    theta = 3*math.pi/2
                elif self.y < vert.getY():
                    #vert is directly below self
                    theta = math.pi/2
            elif self.y == vert.getY():
                if self.x > vert.getX():
                    #vert is directly left of self
                    theta = math.pi
                    #vert is directly right of self gives a theta of 0
                    
                    
            #Self is the center
            if self.x > vert.getX() and self.y > vert.getY():
                #Vert is in the upper left quadrent
                x1 = (self.radius * math.cos(theta - math.pi)) + self.x
                y1 = (self.radius * math.sin(theta - math.pi)) + self.y
                x2 = (vert.getRadius() * math.cos(theta)) + vert.getX()
                y2 = (vert.getRadius() * math.sin(theta)) + vert.getY()
            elif self.x > vert.getX() and self.y < vert.getY():
                #Vert is in the lower left quadrent
                x1 = (self.radius * math.cos(theta - math.pi)) + self.x
                y1 = (self.radius * math.sin(theta - math.pi)) + self.y
                x2 = (vert.getRadius() * math.cos(theta)) + vert.getX()
                y2 = (vert.getRadius() * math.sin(theta)) + vert.getY()
            elif self.x < vert.getX() and self.y > vert.getY():
                #Vert is in the upper right quadrent
                x1 = (self.radius * math.cos(theta)) + self.x
                y1 = (self.radius * math.sin(theta)) + self.y
                x2 = (vert.getRadius() * math.cos(theta - math.pi)) + vert.getX()
                y2 = (vert.getRadius() * math.sin(theta - math.pi)) + vert.getY()
            elif self.x < vert.getX() and self.y < vert.getY():
                #Vert is in the lower right quadrent
                x1 = (self.radius * math.cos(theta)) + self.x
                y1 = (self.radius * math.sin(theta)) + self.y
                x2 = (vert.getRadius() * math.cos(theta - math.pi)) + vert.getX()
                y2 = (vert.getRadius() * math.sin(theta - math.pi)) + vert.getY()
            else:
                x1 = (self.radius * math.cos(theta)) + self.x
                y1 = (self.radius * math.sin(theta)) + self.y
                x2 = (vert.getRadius() * math.cos(theta - math.pi)) + vert.getX()
                y2 = (vert.getRadius() * math.sin(theta - math.pi)) + vert.getY()
            
            self.canvas.create_line(x1, y1, x2, y2,
                                    fill="Green", width=3, tag="Connection")

    def addConnection(self, vert):
        self.connectedVerticies.append(vert)

    def removeConnection(self, vert):
        if vert in self.connectedVerticies:
            self.connectedVerticies.remove(vert)

    def isConnected(self, vert):
        if vert in self.connectedVerticies:
            return True
        else:
            return False
    
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getRadius(self):
        return self.radius
    def getHandleNum(self):
        return self.handleNum
