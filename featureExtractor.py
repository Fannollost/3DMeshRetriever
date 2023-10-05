import pymeshlab as pml
from mathHelper import areaTriangle
from shapeDescriptors import globalShapeDescriptorTypes as globalDescriptors
import numpy as np
import meshplex
from math import pi
from scipy.spatial import ConvexHull

class FeatureExtractor:
    def __init__(self, meshpath):
        print(meshpath)
        self.meshPath = meshpath
        self.pymesh = pml.MeshSet()   
        self.pymesh.load_new_mesh(meshpath)
        self.mesh = self.pymesh.current_mesh()

    def getFeatures(self):
        features = { globalDescriptors.SURFACE_AREA.value : self.getSurfaceArea(), globalDescriptors.VOLUME.value: self.getVolume(),
                     globalDescriptors.RECTANGULARITY.value : self.getVolume() / self.getOBBVolume(), globalDescriptors.COMPACTNESS.value : self.getCompactness(),
                     globalDescriptors.DIAMETER.value: self.getDiameter()}

        #SURFACE_AREA = "Surface Area"
        #VOLUME = "Volume"
        #COMPACTNESS = "Compactness"
        #RECTANGULARITY = "Rectangularity"
        #DIAMETER = "Diameter"
        CONVEXITY = "Convexity"
        ECCENTRICITY = "Eccentricity"
        A3 = "A3"
        D1 = "D1"
        D2 = "D2"
        D3 = "D3"
        D4 = "D4"

        return features

    def getCompactness(self):
        surfArea = self.getSurfaceArea()
        volume = self.getVolume()
        compactness = (surfArea ** 3 / (36 * pi * volume ** 2))
        return compactness
    
    def getSurfaceArea(self):
        vertices = self.mesh.vertex_matrix()
        faces = self.mesh.face_matrix()
        totArea = 0
        for f in faces:
            totArea += areaTriangle(vertices[f[0]],vertices[f[1]],vertices[f[2]])
        return totArea
    
    def getDiameter(self):
        vertices = self.mesh.vertex_matrix()
        distances = np.linalg.norm(vertices[:, np.newaxis] - vertices, axis=-1)
        return np.max(distances)
    
    def getOBBVolume(self):
        minSize = self.mesh.bounding_box().min()
        maxSize = self.mesh.bounding_box().max()
        return (maxSize[0] - minSize[0]) * (maxSize[1] - minSize[1]) * (maxSize[2] - minSize[2])  
    
    def getVolume(self):
        vertices = self.mesh.vertex_matrix()
        faces = self.mesh.face_matrix()

        hull = ConvexHull(vertices)
        volume = 0.0

        for f in faces:
            vert = [vertices[i] for i in f]
            tetraVolume = np.abs(np.dot(vert[0], np.cross(vert[1], vert[2]))) / 6.0
            volume += tetraVolume


        volume = np.abs(volume)
        return volume