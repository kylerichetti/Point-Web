#TODO:
#Set panel location
#Create buttons
#Tie the creation and removal of verticies to said buttons

from tkinter import *
from pointWebMesh import *
class pwControlPanel:
    def __init__(self, root, mesh):
        self.root = root
        self.mesh = mesh
        self.panel = Frame(self.root)
        self.addButton = Button(self.panel, text="Create Vertex", command=self.addVert)
        self.deleteButton = Button(self.panel, text="Delete Vertex", command=self.removeVert)

    def pack(self):
        self.addButton.pack(side=LEFT)
        self.deleteButton.pack(side=LEFT)
        self.panel.pack()

    def addVert(self):
        self.mesh.addVertex(Vertex(self.mesh.canvas, 400, 300, 15))
        self.mesh.render()

    def removeVert(self):
        delVertHandle = self.mesh.getSelectedVertHandle()
        if delVertHandle != None:
            self.mesh.removeVert(delVertHandle)

