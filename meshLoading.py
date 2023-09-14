import os
import sys
import glob 
import pywavefront 
import pandas as pd

directories = ["Airplane", "Ant", "Armadillo", "Bearing", "Bird", "Bust", "Chair", "Cup", 
               "Fish", "FourLeg", "Glasses", "Hand", "Human", "Mech", "Octopus", "Plier", 
               "Octobus", "Plier", "Table", "Teddy", "Vase"] 

"""
Loads all the meshes
"""
def loadAllMeshes():
    for dir in directories:
        for name in glob.glob('/db/' + dir + ''):
            if(name.__contains__("labels")):
                continue
            verticesAndFaces(name)

"""
Extract all faces and vertices from obj file
"""
def verticesAndFaces(file):
    obj_data = pywavefront.Wavefront(file, collect_faces=True)
    vertices = obj_data.vertices
    faces = [face for mesh in obj_data.mesh_list for face in mesh.faces]
    return vertices, faces

