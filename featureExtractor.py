import pymeshlab as pml
from mathHelper import areaTriangle, angleBetween, vector, length, dist, volumeTetrahydron
from shapeDescriptors import globalShapeDescriptorTypes as globalDescriptors
from shapeDescriptors import propertyDescriptorTypes as propertyDescriptors
from shapeDescriptors import histogramLimits
import numpy as np
import meshplex
from math import pi
import random
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
        samples = 10000
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

        A3 = self.getA3()
        D1 = self.getD1()
        D2 = self.getD2()
        return features

    def getA3(self, samples):
        vertices = self.pymesh.vertex_matrix()
        allSamples = []
        for i in range(samples):
            idx = random.randomint(0,len(vertices) - 1)
            vertex0 = vertices[idx]
            for j in range(samples):
                jdx = random.randomint(0,len(vertices) - 1)
                vertex1 = vertices[jdx]
                if idx == jdx: 
                    continue
                for k in range(samples):
                    kdx = random.randomint(0,len(vertices) - 1)
                    vertex2 = vertices[kdx]
                    if kdx == jdx or kdx == jdx: continue
                    allSamples.append(angleBetween(vector(vertex0,vertex1), vector(vertex0,vertex2)))

        yAxis, binEdges = np.histogram(allSamples, range =  histogramLimits[propertyDescriptors.A3.value], bins = 8)
        return self.normalise(yAxis, binEdges)
    
    def getD1(self, samples):
        vertices = self.pymesh.vertex_matrix()
        allSamples = []
        for i in range(samples):
            idx = random.randomint(0, len(vertices) - 1)
            vertex = vertices[idx]
            allSamples.append(length(vertex))
        yAxis, binEdges = np.histogram(allSamples, range = histogramLimits[propertyDescriptors.D1.value], bins=8)
        return self.normalise(yAxis,binEdges)
    
    def getD2(self,samples):
        vertices = self.pymesh.vertex_matrix()
        allSamples = []
        for i in range(samples):
            idx = random.randomint(0,len(vertices) - 1)
            vertex0 = vertices[idx]
            for j in range(samples):
                jdx = random.randomint(0,len(vertices) - 1)
                vertex1 = vertices[jdx]
                if jdx == idx: continue
                allSamples.append(dist(vertex0, vertex1))
        yAxis, binEdges = np.histogram(allSamples, range = histogramLimits[propertyDescriptors.D2.value], bins=8)
        return self.normalise(yAxis,binEdges)

    def getD3(self,samples): 
        vertices = self.pymesh.vertex_matrix()
        allSamples = []
        for i in range(samples):
            idx = random.randomint(0,len(vertices) - 1)
            vertex0 = vertices[idx]
            for j in range(samples):
                jdx = random.randomint(0,len(vertices) - 1)
                vertex1 = vertices[jdx]
                if jdx == idx : continue
                for k in range(samples):
                    kdx = random.randomint(0,len(vertices) - 1)
                    vertex2 = vertices[kdx]
                    if kdx == jdx or kdx == idx: continue
                    area = areaTriangle(vertex0,vertex1,vertex2)
                    allSamples.append(area)
        yAxis, binEdges = np.histogram(allSamples, range =  histogramLimits[propertyDescriptors.D3.value], bins = 8)
        return self.normalise(yAxis, binEdges)
    
    def getD4(self, samples):
        vertices = self.pymesh.vertex_matrix()
        allSamples = []
        for i in range(samples):
            idx = random.randomint(0,len(vertices) - 1)
            vertex0 = vertices[idx]
            for j in range(samples):
                jdx = random.randomint(0,len(vertices) - 1)
                vertex1 = vertices[jdx]
                if jdx == idx : continue
                for k in range(samples):
                    kdx = random.randomint(0,len(vertices) - 1)
                    vertex2 = vertices[kdx]
                    if kdx == jdx or kdx == idx: continue
                    for l in range(samples):
                        ldx = random.randomint(0,len(vertices) - 1)
                        vertex3 = vertices[ldx]
                        if ldx == kdx or ldx == jdx or ldx == idx: continue
                        volume = volumeTetrahydron(vector(vertex0,vertex1), vector(vertex0,vertex2), vector(vertex0,vertex3))


    def normalise(self, yAxis, binEdges):
        x = (binEdges[1:] + binEdges[:-1]) / 2
        normalise = []
        for v in yAxis: 
            normalise.append(v / sum(yAxis))
        return [x, normalise]

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