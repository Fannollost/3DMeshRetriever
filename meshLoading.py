import os.path
from pathlib import Path
import sys
import glob 
import pywavefront 
import pandas as pd
import pymeshlab
from meshDataTypes import dataTypes as data


directories = ["Airplane", "Ant", "Armadillo", "Bearing", "Bird", "Bust", "Chair", "Cup", 
               "Fish", "FourLeg", "Glasses", "Hand", "Human", "Mech", "Octopus", "Plier", 
               "Octobus", "Plier", "Table", "Teddy", "Vase"] 

class Mesh:
    
    def __init__(self, meshPath):
        pymeshlab.print_pymeshlab_version()
        self.meshPath = meshPath
        self.pymesh = pymeshlab.MeshSet()   
        self.pymesh.load_new_mesh(meshPath)
        self.mesh = self.pymesh.current_mesh()

    """
    Extract all faces and vertices from obj file
    """
    def verticesAndFaces(self):
        obj_data = pywavefront.Wavefront(self.meshPath, collect_faces=True)
        vertices = obj_data.vertices
        faces = [face for mesh in obj_data.mesh_list for face in mesh.faces]
        return vertices, faces
    
    """
    Loads all the meshes
    """
    def loadAllMeshes(self):
        for dir in directories:
            for name in glob.glob('/db/' + dir + ''):
                if(name.__contains__("labels")):
                    continue
                self.verticesAndFaces(name)

    def getAnalyzedData(self):
        file = Path(self.meshPath)
        classType = os.path.relpath(file.parent, file.parent.parent)
        bary_data = self.pymesh.get_geometric_measures()
        vertices, faces = self.verticesAndFaces()
        quads = False
        triangles = False
        for face in faces:
            if len(face) == 4: 
                quads = True
            if len(face) == 3:
                triangles = True
        
        if quads and triangles:
            print("We have a mix of triangles and quads")
        if triangles and not(quads):
            print("We only have triangles")
        else:
            print("We have quads only")
            
        boundingbox = [self.mesh.bounding_box().dim_x(), self.mesh.bounding_box().dim_y(), self.mesh.bounding_box().dim_z()]
        analyzedData = { data.CLASS.value : classType, data.AMOUNT_FACES.value : len(faces), data.AMOUNT_VERTICES.value : len(vertices),
                         data.BARY_CENTER.value : bary_data['barycenter'], data.SIZE.value : boundingbox, data.MAX_SIZE.value : max(boundingbox) }
        return analyzedData


