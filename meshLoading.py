import os.path
from pathlib import Path
import sys
import glob 
import pywavefront 
import pandas as pd
import pymeshlab as pml
from meshDataTypes import dataTypes as data
import numpy as np
import tripy


target_edge_length = 0.02
targetTriangles = 10000

class Mesh:
    
    def __init__(self, meshPath):
        pml.print_pymeshlab_version()
        self.meshPath = meshPath
        self.pymesh = pml.MeshSet()   
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
        self.fileName = self.meshPath.split('/')[2]
        
        quads = False
        triangles = False
        for face in self.mesh.polygonal_face_list():
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
        analyzedData = { data.CLASS.value : classType, data.AMOUNT_FACES.value : self.mesh.face_number(), data.AMOUNT_VERTICES.value : self.mesh.vertex_number(),
                         data.BARY_CENTER.value : bary_data['barycenter'], data.SIZE.value : np.array(boundingbox), data.MAX_SIZE.value : max(boundingbox) }
        return analyzedData

    def getBoundingBox(self):
        return [self.mesh.bounding_box().dim_x(), self.mesh.bounding_box().dim_y(), self.mesh.bounding_box().dim_z()]

    def normaliseMesh(self):
        self.getAnalyzedData()
        self.removeUnwantedMeshData()
        self.remesh()
        self.normaliseVertices()
        d = self.getAnalyzedData()
        self.SaveMesh('normalisedDB/' + d[data.CLASS.value] + '/' + str(self.fileName))
        return d

    def remesh(self):
        maxVertices = 100000
        minVertices = 10000

        if(self.mesh.vertex_number() > maxVertices):
            self.remeshDOWN()
            print("DOWN!")
        if(self.mesh.vertex_number() < minVertices):
            self.remeshUP()
            print("UP!")

    def normaliseVertices(self):
        d = self.getAnalyzedData()
        self.pymesh.compute_matrix_from_translation(traslmethod='XYZ translation', axisx = -1 * d[data.BARY_CENTER.value][0],
                                                     axisy = -1 * d[data.BARY_CENTER.value][1],
                                                     axisz = -1 * d[data.BARY_CENTER.value][2])
        d = self.getAnalyzedData()
        self.pymesh.compute_matrix_from_scaling_or_normalization(axisx=1 / d[data.MAX_SIZE.value], customcenter=d[data.BARY_CENTER.value], uniformflag=True)

    def centerBarycenters(self):
        translated = [ vertex - self.bary_data['barycenter'] for vertex in self.mesh.ver]
        return translated

    def removeUnwantedMeshData(self):
        self.pymesh.apply_filter('meshing_remove_duplicate_vertices')
        self.pymesh.apply_filter('meshing_remove_duplicate_faces')
        self.pymesh.apply_filter('meshing_remove_unreferenced_vertices')
        self.pymesh.current_mesh()

    def SaveMesh(self, file_path):
        #Create parent dir if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        #Save the file in off format
        if file_path==None:
            self.pymesh.save_current_mesh(file_path)
        else:
            self.pymesh.save_current_mesh(file_path)
    
    def remeshUP(self):
        minTriangles = targetTriangles * 0.8
        iteration = 0

        while(self.mesh.face_number() < minTriangles or iteration > 10):
            iteration += 1
            self.pymesh.remeshing_isotropic_explicit_remeshing(targetlen=pml.AbsoluteValue(target_edge_length), iterations=1)
            print(self.pymesh.current_mesh().face_number())

    def remeshDOWN(self):
        minTriangles = targetTriangles * 1.2
        iteration = 0

        while(self.mesh.face_number() > minTriangles or iteration > 10):
            self.pymesh.remeshing_isotropic_explicit_remeshing(targetlen=pml.AbsoluteValue(target_edge_length), iterations=1)
            print(self.pymesh.current_mesh().face_number())
