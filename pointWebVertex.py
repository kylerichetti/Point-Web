import math
class Vertex:
    def __init__(self, canvas, x, y, radius):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.handleNum = None
        self.connectedVerticies = []
        self.fillColor = "White"

    def updateCoords(self, coords):
        (x,y) = coords
        self.x = x
        self.y = y
        
    def render(self):
        self.drawConnections()
        #If vert is already drawn, delete it
        if self.handleNum:
            self.canvas.delete(self.handleNum)
        
        self.handleNum = self.canvas.create_oval(self.x - self.radius,
                                self.y - self.radius,
                                self.x + self.radius,
                                self.y + self.radius,
                                tag = ("vert"),
                                fill = self.fillColor)

    def drawConnections(self):
        for vert in self.connectedVerticies:
            #Catch div by 0
            theta = 0 #Might be able to remove this line? Haven't tested
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

    #Need to look for a string comparison function
    #Python probably has one built in that would work better
    def toggleColor(self):
        if self.fillColor == "White":
            self.fillColor = "Red"
        else:
            self.fillColor = "White"
