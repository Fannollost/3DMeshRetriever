import os.path
from pathlib import Path
import sys
import glob 
import pywavefront 
import pandas as pd
import pymeshlab as pml
from meshDataTypes import dataTypes as data
import numpy as np
import mathHelper
from helper import getEveryElementFromEveryList


target_edge_length = 0.02
targetVertices = 10000

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
        eigen_values, eigen_vectors = self.getPCA()
        boundingbox = [self.mesh.bounding_box().dim_x(), self.mesh.bounding_box().dim_y(), self.mesh.bounding_box().dim_z()]
        analyzedData = { data.CLASS.value : classType, data.AMOUNT_FACES.value : self.mesh.face_number(), data.AMOUNT_VERTICES.value : self.mesh.vertex_number(),
                         data.BARY_CENTER.value : bary_data['barycenter'], data.SIZE.value : np.array(boundingbox), data.MAX_SIZE.value : max(boundingbox),
                         data.DISTANCE_ORIGIN.value : mathHelper.length(bary_data['barycenter']), data.EIGEN_VALUE.value : eigen_values, data.EIGEN_VECTORS.value : eigen_vectors }
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

    def normaliseVertices(self):
        d = self.getAnalyzedData()
        self.pymesh.compute_matrix_from_translation(traslmethod='XYZ translation', axisx = -1 * d[data.BARY_CENTER.value][0],
                                                     axisy = -1 * d[data.BARY_CENTER.value][1],
                                                     axisz = -1 * d[data.BARY_CENTER.value][2])
        self.alignAxises()
        d = self.getAnalyzedData()
        self.pymesh.compute_matrix_from_scaling_or_normalization(axisx=1 / d[data.MAX_SIZE.value], customcenter=d[data.BARY_CENTER.value], uniformflag=True)

    def alignAxises(self):
        meshData = self.getAnalyzedData()
        eigenVectors = meshData[data.EIGEN_VECTORS.value]
        for vector in eigenVectors:
            vector[0] = vector[0]/mathHelper.length(vector)
            vector[1] = vector[1]/mathHelper.length(vector)
            vector[2] = vector[2]/mathHelper.length(vector)

        facesMatrix = self.mesh.face_matrix()
        vertexMatrix = self.mesh.vertex_matrix()
        edgesMatrix = self.mesh.edge_matrix()
       # print(vertexMatrix)
        for vIdx in range(len(vertexMatrix)):
            vertexMatrix[vIdx] = [np.dot(eigenVectors[0], vertexMatrix[vIdx]), np.dot(eigenVectors[1], vertexMatrix[vIdx]), np.dot(eigenVectors[2], vertexMatrix[vIdx])]

        rotatedMesh = pml.Mesh(vertex_matrix = vertexMatrix, face_matrix = facesMatrix, edge_matrix = edgesMatrix)
        self.pymesh.clear()
        self.pymesh.add_mesh(rotatedMesh)
        self.mesh = self.pymesh.current_mesh()

    def centerBarycenters(self):
        translated = [ vertex - self.bary_data['barycenter'] for vertex in self.mesh.ver]
        return translated

    def removeUnwantedMeshData(self):
        self.pymesh.apply_filter('meshing_remove_duplicate_vertices')
        self.pymesh.apply_filter('meshing_remove_duplicate_faces')
        self.pymesh.apply_filter('meshing_remove_unreferenced_vertices')
        self.mesh = self.pymesh.current_mesh()

    def SaveMesh(self, file_path):
        #Create parent dir if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        print(self.pymesh.current_mesh().vertex_matrix())
        #Save the file in obj format
        if file_path==None:
            self.pymesh.save_current_mesh(file_path)
        else:
            self.pymesh.save_current_mesh(file_path)
    
    def remesh(self):
        targetVertices = 10000
        while(self.mesh.vertex_number() < targetVertices - 100):
            if(self.mesh.vertex_number() < targetVertices - 100):
                try:
                    self.pymesh.apply_filter('meshing_surface_subdivision_loop', threshold=pml.Percentage(0), iterations=1)
                except:
                    self.pymesh.apply_filter('meshing_repair_non_manifold_edges', method='Remove Faces')
                    self.pymesh.apply_filter('meshing_repair_non_manifold_vertices')
            elif(self.mesh.vertex_numbers() > targetVertices - 100):
                self.ms.apply_filter('meshing_decimation_quadric_edge_collapse', targetperc= targetVertices / self.mesh.vertex_number())

        if(self.mesh.vertex_number() - 100 > targetVertices):
           self.pymesh.apply_filter('meshing_decimation_quadric_edge_collapse', targetperc= targetVertices / self.mesh.vertex_number())

        print(self.pymesh.current_mesh().vertex_number())

    def getPCA(self):
        vertexMat = self.mesh.vertex_matrix()
        V = np.zeros((3, len(vertexMat)))
        V[0] = getEveryElementFromEveryList(0,vertexMat)
        V[1] = getEveryElementFromEveryList(1,vertexMat)
        V[2] = getEveryElementFromEveryList(2,vertexMat)

        V_cov = np.cov(V)
        eigenvalues, eigenvectors = np.linalg.eig(V_cov)
        res=[getEveryElementFromEveryList(0,eigenvectors),getEveryElementFromEveryList(1,eigenvectors), getEveryElementFromEveryList(2,eigenvectors)]

        for i in range (3):
            for j in range(i+1,3):
                if(eigenvalues[j]>eigenvalues[i]):
                   temp=res[i].copy()
                   res[i] = res[j]
                   res[j] = temp
                   temp=eigenvalues[i]
                   eigenvalues[i] = eigenvalues[j]
                   eigenvalues[j] = temp

        return eigenvalues, [res[0],res[1],mathHelper.crossProduct(res[0],res[1])]