#TODO:
#Animate connections to move in real time: Done
    #Erase and rerender just the connections?: Done
    #Might need a way just redraw connections related to the vertext being moved: Done
#Fix connections to always stop on the correct side of the circle: Done
#Find a better way to associate verticies and their handle numbers: Done*
    #Seems to be fixed since all verticies are no longer rerendered on release
#Add visual indications when a vertex has been selected to add a new connection: Done

#Use canvas.coords to move connections instead of deleting and rerendering them
#Allow the creation and removal of verticies
    #Perhaps right clicking on a vertex selects it, and from there it can be deleted?
#Fix the Mesh funcionts for checking, adding, and removing verticies
    #Details are in the pointWebMesh class
#Decide how to handle drawing connections when verticies overlap


import math
from tkinter import *

#from pointWebMesh import *

#Also imports the mesh and verticies
from pointWebControlPanel import *

canvasWidth = 800
canvasHeight = 600
root = Tk()

stdRadius = 15

w = Canvas(root, width=canvasWidth, height=canvasHeight)
w.pack()

w.create_rectangle(0,0,canvasWidth,canvasHeight,fill='black',outline='black')

m = Mesh(w)

cp = pwControlPanel(root, m)
cp.pack()

m.addVertex(Vertex(w, 600, 300, stdRadius))
m.addVertex(Vertex(w, 500, 200, stdRadius))
m.addVertex(Vertex(w, 500, 400, stdRadius))
m.addVertex(Vertex(w, 300, 200, stdRadius))
m.addVertex(Vertex(w, 300, 400, stdRadius))

m.addConnection(0,1)
m.addConnection(0,2)
m.addConnection(1,2)
m.addConnection(2,3)
m.addConnection(3,4)
m.render()

root.mainloop()
