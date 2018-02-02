#TODO:
#Animate connections to move in real time: Done
    #Erase and rerender just the connections?: Done
    #Might need a way just redraw connections related to the vertext being moved: Done
#Allow the creation and removal of verticies
#Fix the Mesh funcionts for checking, adding, and removing verticies
    #Section begins on line 299, further notes are there
#Fix connections to always stop on the correct side of the circle: Done
#Find a better way to associate verticies and their handle numbers



import math
from tkinter import *
canvasWidth = 800
canvasHeight = 600
root = Tk()

stdRadius = 15

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
        
class Mesh:
    def __init__(self, canvas):
        self.canvas = canvas
        self.verticies = []
        self._dragData = {"x" : 0, "y" : 0, "item": None}
        self._connectionData = {"item1": None, "item2": None}

    def addVertex(self, vert):
        #Might have to do some scope related shinanigans here, I'm not sure
        self.verticies.append(vert)

    def addConnection(self, v1, v2):
        #Need to add checks so that a vertex can't be connected to itself
        self.verticies[v1].addConnection(self.verticies[v2])

    def removeConnection(self, v1, v2):
        self.verticies[v1].remove(self.verticies[v2])

    def checkConnection(self, v1, v2):
        return self.verticies[v1].isConnected(self.verticies[v2])

    def render(self):
        self.canvas.delete("vert")
        self.canvas.delete("Connection")
        for vert in self.verticies:
            vert.render()
        self.canvas.tag_bind("vert", "<ButtonPress-1>", self.onLeftMousePress)
        self.canvas.tag_bind("vert", "<ButtonRelease-1>", self.onLeftMouseRelease)
        self.canvas.tag_bind("vert", "<B1-Motion>", self.onMotion)
        self.canvas.tag_bind("vert", "<ButtonPress-3>", self.onRightMousePress)

    def rerenderConnections(self):
        self.canvas.delete("Connection")
        for vert in self.verticies:
            vert.drawConnections()

    def onLeftMousePress(self, event):
        self._dragData["item"] = self.canvas.find_closest(event.x, event.y)[0]
        #The vert will snap so that its center is directly under the mouse
        #It looks a little rough, but is functional for now
        #I'll have to figure out how to smooth the whole thing later
        vert = self.findVertWithHandleNum(self._dragData["item"])
        self._dragData["x"] = vert.getX()
        self._dragData["y"] = vert.getY()

    def onLeftMouseRelease(self, event):
        #Find vertex object in mesh array
        vert = self.findVertWithHandleNum(self._dragData["item"])
        
        #Update vertex
        #Not sure on scope here again. Gets into pass by reference and how that
        #plays with arrays. Also not sure on best practices
        #vert.updateCoords( (self._dragData["x"], self._dragData["y"]) )
    
        #Re-render
        self.render()
        
        #Reset drag data
        self._dragData["item"] = None
        self._dragData["x"] = 0
        self._dragData["y"] = 0

    def onMotion(self, event):
        #Compute distance
        deltaX = event.x - self._dragData["x"]
        deltaY = event.y - self._dragData["y"]
        #Move the object
        self.canvas.move(self._dragData["item"], deltaX, deltaY)
        #Record the new position
        self._dragData["x"] = event.x
        self._dragData["y"] = event.y
        #Update the vertex data so the connections will move with it
        vert = self.findVertWithHandleNum(self._dragData["item"])
        vert.updateCoords( (self._dragData["x"], self._dragData["y"]) )
        #Rerender connections
        self.rerenderConnections()

    def onRightMousePress(self, event):
        #Check if an item has not already been selected
        if self._connectionData["item1"] == None:
            #Store the first item
            self._connectionData["item1"] = self.canvas.find_closest(event.x, event.y)[0]
            #Visual indication?
            #print(self._connectionData["item1"])
        else:
            #Store second item
            self._connectionData["item2"] = self.canvas.find_closest(event.x, event.y)[0]
            #Checks
            #Check if the same vertex was clicked twice
            if self._connectionData["item1"] == self._connectionData["item2"]:
                #Clear connection data
                self._connectionData["item1"] = None
                self._connectionData["item2"] = None
                return
            #Get the location of the verticies in the mesh's array
            vert1 = self.findVertWithHandleNum(self._connectionData["item1"])
            vert2 = self.findVertWithHandleNum(self._connectionData["item2"])
            
            #Check if a connection already exists
            #This is the proper way to do it, need to
            #refactor so that it works
            #if self.checkConnection(vert1, vert2):
                #If so, remove the connection
                #self.removeConnection(vert1, vert2)
            #else:
                #Else, add connection
                #self.addConnection(vert1, vert2)
                #vert1.addConnection(vert2)

            #Check if a connection already exists
            if vert1.isConnected(vert2):
                #If so, remove the connection
                vert1.removeConnection(vert2)
                vert2.removeConnection(vert1)
            else:
                #Else, add connection
                vert1.addConnection(vert2)

            #Reset connection data
            self._connectionData["item1"] = None
            self._connectionData["item2"] = None
            self.render()
        
    def findVertWithHandleNum(self, handleNum):
        for vert in self.verticies:
            if vert.getHandleNum() == handleNum:
                #Not sure if I want to return the vert itself or
                #a way to identify it in the mesh's array
                return vert

w = Canvas(root, width=canvasWidth, height=canvasHeight)
w.pack()

w.create_rectangle(0,0,canvasWidth,canvasHeight,fill='black',outline='black')

m = Mesh(w)
m.addVertex(Vertex(w, 400, 300, stdRadius))
m.addVertex(Vertex(w, 500, 200, stdRadius))
m.addVertex(Vertex(w, 500, 400, stdRadius))
m.addVertex(Vertex(w, 300, 200, stdRadius))
m.addVertex(Vertex(w, 300, 400, stdRadius))

#m.addConnection(0,2)
m.addConnection(0,1)
m.addConnection(0,2)
m.addConnection(1,2)
m.addConnection(2,3)
m.addConnection(3,4)
m.render()

root.mainloop()
