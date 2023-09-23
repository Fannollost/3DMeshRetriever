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

directories = ["Airplane", "Ant", "Armadillo", "Bearing", "Bird", "Bust", "Chair", "Cup", 
               "Fish", "FourLeg", "Glasses", "Hand", "Human", "Mech", "Octopus", "Plier", 
               "Octobus", "Plier", "Table", "Teddy", "Vase"] 
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
        self.classType = os.path.relpath(file.parent, file.parent.parent)
        self.bary_data = self.pymesh.get_geometric_measures()
        self.vertices, self.faces = self.verticesAndFaces()
        self.barycenter = self.getBarycenter(self.vertices, self.faces)

        self.fileName = self.meshPath.split('/')[2]
        quads = False
        triangles = False
        for face in self.faces:
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
        self.boundingbox = boundingbox
        self.maxSize = max(boundingbox)
        analyzedData = { data.CLASS.value : self.classType, data.AMOUNT_FACES.value : len(self.faces), data.AMOUNT_VERTICES.value : len(self.vertices),
                         data.BARY_CENTER.value : self.bary_data['barycenter'], data.SIZE.value : np.array(boundingbox), data.MAX_SIZE.value : max(boundingbox) }
        return analyzedData

    def getBarycenter(self, vertices, faces):
        barycenter = [0,0,0]
        total_weight = 0.0
        for face in faces:
            centroid = np.mean(face, axis=0)
            area = tripy.area(np.array(zip(face)))
            weighted = centroid * area
            barycenter += weighted
            total_weight += area
        
        return barycenter / total_weight
        for vertex in vertices:
            barycenter[0] +=vertex[0]
            barycenter[1] +=vertex[1]
            barycenter[2] +=vertex[2]
            # TODO
        barycenter[0] /= len(vertices)
        barycenter[1] /= len(vertices)
        barycenter[2] /= len(vertices)
        return barycenter

    def getBoundingBox(self, vertices):
        x_coordinates, y_coordinates, z_coordinates = zip(*vertices)
        return [(min(x_coordinates), min(y_coordinates), min(z_coordinates)), (max(x_coordinates), max(y_coordinates), max(z_coordinates))]

    def normaliseMesh(self):
        self.getAnalyzedData()
        self.removeUnwantedMeshData()
        translated = self.centerBarycenters()
        normalised = self.normaliseVertices(translated)
        self.SaveMesh(normalised, self.faces, 'normalisedDB/' + self.classType + '/' + str(self.fileName))
        normalisedData = { data.CLASS.value : self.classType, data.AMOUNT_FACES.value : len(self.faces), data.AMOUNT_VERTICES.value : len(translated),
                         data.BARY_CENTER.value : self.getBarycenter(normalised, self.faces), data.SIZE.value : np.array(self.getBoundingBox(normalised)) } #, data.MAX_SIZE.value : max(normalised) }
        return normalisedData

    def normaliseVertices(self, vertices):
        """min = np.min(vertices, axis=0)
        max = np.max(vertices, axis=0)

        dimension = max - min
        scaling = 1 / np.max(dimension)

        print(scaling)
        vertices = [vertex * scaling for vertex in vertices]
        return vertices
        """
        x_min = min(point[0] for point in vertices)
        y_min = min(point[1] for point in vertices)
        z_min = min(point[2] for point in vertices)

        normalized_x = ((point[0] - x_min) / self.maxSize - 0.5 for point in vertices)
        normalized_y = ((point[1] - y_min) / self.maxSize - 0.5 for point in vertices) 
        normalized_z = ((point[2] - z_min) / self.maxSize - 0.5 for point in vertices) 

        self.normalized = list(zip(normalized_x,normalized_y,normalized_z))
        return self.normalized

    def centerBarycenters(self):
        translated = [ vertex - self.bary_data['barycenter'] for vertex in self.vertices]
        return translated

    def removeUnwantedMeshData(self):
        self.pymesh.apply_filter('meshing_remove_duplicate_vertices')
        self.pymesh.apply_filter('meshing_remove_duplicate_faces')
        self.pymesh.apply_filter('meshing_remove_unreferenced_vertices')

    def SaveMesh(sellf, vertices, faces, file_path):
        with open(file_path, 'w') as obj_file:
            for vertex in vertices:
                obj_file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        
            for face in faces:
                # In OBJ format, face indices are 1-based, so we need to add 1 to each index.
                face_str = "f " + " ".join(str(idx + 1) for idx in face) + "\n"
                obj_file.write(face_str)
    
    def remeshUP(path):
        minTriangles = targetTriangles * 0.8

        mesh_lowpoly = pml.MeshSet()
        mesh_lowpoly.load_new_mesh(path)

        iteration = 0

        while(mesh_lowpoly.current_mesh().face_number() < minTriangles or iteration > 10):
            iteration += 1
            mesh_lowpoly.meshing_isotropic_explicit_remeshing(targetlen=pml.AbsoluteValue(target_edge_length), iterations=1)
            print(mesh_lowpoly.current_mesh().face_number())

    def remeshDOWN(path):
        minTriangles = targetTriangles * 1.2

        mesh_lowpoly = pml.MeshSet()
        mesh_lowpoly.load_new_mesh(path)

        iteration = 0

        while(mesh_lowpoly.current_mesh().face_number() > minTriangles or iteration > 10):
            mesh_lowpoly.meshing_isotropic_explicit_remeshing(targetlen=pml.AbsoluteValue(target_edge_length), iterations=1)
            print(mesh_lowpoly.current_mesh().face_number())
        
    def saveMesh(mesh, path):
        mesh.save_current_mesh(path)
