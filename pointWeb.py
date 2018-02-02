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

from pointWebMesh import *

canvasWidth = 800
canvasHeight = 600
root = Tk()

stdRadius = 15

w = Canvas(root, width=canvasWidth, height=canvasHeight)
w.pack()

w.create_rectangle(0,0,canvasWidth,canvasHeight,fill='black',outline='black')

m = Mesh(w)
m.addVertex(Vertex(w, 600, 300, stdRadius))
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
