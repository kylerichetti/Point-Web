from pointWebVertex import *
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
        #self.canvas.delete("vert")
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
        #Re-render
        self.rerenderConnections()
        
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
            #Select the item that was clicked on
            item = self.canvas.find_closest(event.x,event.y)[0]            
            #Store the first item with its new color
            self._connectionData["item1"] = self.toggleVertColor(item)
        else:
            #Revert color of item 1
            self._connectionData["item1"] = self.toggleVertColor(self._connectionData["item1"])
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
                #Currently returning the vert itself
                return vert
            
    def toggleVertColor(self, handleNum):
        #Find the vert in the mesh's array
            item = self.findVertWithHandleNum(handleNum)
            #Toggle its color
            item.toggleColor()
            #Render so that the color change is visible
            item.render()
            #Return the new handleNum
            return item.getHandleNum()
