import pymeshlab as pml
from mathHelper import areaTriangle, angleBetween, vector, length, dist, volumeTetrahydron
from shapeDescriptors import globalShapeDescriptorTypes as globalDescriptors
from shapeDescriptors import propertyDescriptorTypes as propertyDescriptors
from shapeDescriptors import histogramLimits
import numpy as np
import meshplex
from math import pi
import random
from scipy.spatial import ConvexHull, distance
import scipy
from itertools import combinations
from helper import getEveryElementFromEveryList
import open3d

SapeProperties = True

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
                     globalDescriptors.CONVEXITY.value: self.getVolume() / self.getConvexHull(), globalDescriptors.ECCENTRICITY.value : self.getEccentric(),
                     globalDescriptors.DIAMETER.value : self.getDiameter()} 
        
        samples = 100000

        ## TODO 
        #SURFACE_AREA = "Surface Area"
        #VOLUME = "Volume"
        #COMPACTNESS = "Compactness"
        RECTANGULARITY = "Rectangularity"
        #DIAMETER = "Diameter"
        #CONVEXITY = "Convexity"
        #ECCENTRICITY = "Eccentricity"
        # A3 = "A3"
        # D1 = "D1"
        # D2 = "D2"
        # D3 = "D3"
        # D4 = "D4"

        if SapeProperties:
            A3 = self.getA3(int(samples ** (1/3))+ 1) 
            print("done with A3")
            D1 = self.getD1(samples)
            print("done with D1")
            D2 = self.getD2(int(samples ** (1/2))+ 1)
            print("done with D2")
            D3 = self.getD3(int(samples ** (1/3))+ 1)
            print("done with D3")
            D4 = self.getD4(int(samples ** (1/4))+ 1)
            print("done with D4")

            for i in range(len(A3[0])):
                features["A3_"+str(i)] = A3[1][i]
            for i in range(len(D1[0])):
                features["D1_"+str(i)] = D1[1][i]
            for i in range(len(D2[0])):
                features["D2_"+str(i)] = D2[1][i]
            for i in range(len(D3[0])):
                features["D3_"+str(i)] = D3[1][i]
            for i in range(len(D4[0])):
                features["D4_" + str(i)] = D4[1][i]
        return features

    def getA3(self, samples):
        vertices = self.mesh.vertex_matrix()
        allSamples = []
        for i in range(samples):
            idx = random.randint(0,len(vertices) - 1)
            vertex0 = vertices[idx]
            for j in range(samples):
                jdx = random.randint(0,len(vertices) - 1)
                vertex1 = vertices[jdx]
                if idx == jdx: 
                    continue
                for k in range(samples):
                    kdx = random.randint(0,len(vertices) - 1)
                    vertex2 = vertices[kdx]  
                    if kdx == jdx or kdx == jdx: continue
                    allSamples.append(angleBetween(vector(vertex0,vertex1), vector(vertex0,vertex2)))

        yAxis, binEdges = np.histogram(allSamples, range = (0, histogramLimits[propertyDescriptors.A3.value]), bins = 8)
        return self.normalise(yAxis, binEdges)
    
    def getD1(self, samples):
        vertices = self.mesh.vertex_matrix()
        allSamples = []
        for i in range(samples):
            idx = random.randint(0, len(vertices) - 1)
            vertex = vertices[idx]
            allSamples.append(length(vertex))
        yAxis, binEdges = np.histogram(allSamples, range = (0, histogramLimits[propertyDescriptors.D1.value]), bins=8)
        return self.normalise(yAxis,binEdges)
    
    def getD2(self,samples):
        vertices = self.mesh.vertex_matrix()
        allSamples = []
        for i in range(samples):
            idx = random.randint(0,len(vertices) - 1)
            vertex0 = vertices[idx]
            for j in range(samples):
                jdx = random.randint(0,len(vertices) - 1)
                vertex1 = vertices[jdx]
                if jdx == idx: continue
                allSamples.append(dist(vertex0, vertex1))
        yAxis, binEdges = np.histogram(allSamples, range = (0, histogramLimits[propertyDescriptors.D2.value]), bins=8)
        return self.normalise(yAxis,binEdges)

    def getD3(self,samples): 
        vertices = self.mesh.vertex_matrix()
        allSamples = []
        for i in range(samples):
            idx = random.randint(0,len(vertices) - 1)
            vertex0 = vertices[idx]
            for j in range(samples):
                jdx = random.randint(0,len(vertices) - 1)
                vertex1 = vertices[jdx]
                if jdx == idx : continue
                for k in range(samples):
                    kdx = random.randint(0,len(vertices) - 1)
                    vertex2 = vertices[kdx]
                    if kdx == jdx or kdx == idx: continue
                    area = areaTriangle(vertex0,vertex1,vertex2)
                    allSamples.append(area)
        yAxis, binEdges = np.histogram(allSamples, range =  (0, histogramLimits[propertyDescriptors.D3.value]), bins = 8)
        return self.normalise(yAxis, binEdges)
    
    def getD4(self, samples):
        vertices = self.mesh.vertex_matrix()
        allSamples = []
        for i in range(samples):
            idx = random.randint(0,len(vertices) - 1)
            vertex0 = vertices[idx]
            for j in range(samples):
                jdx = random.randint(0,len(vertices) - 1)
                vertex1 = vertices[jdx]
                if jdx == idx : continue
                for k in range(samples):
                    kdx = random.randint(0,len(vertices) - 1)
                    vertex2 = vertices[kdx]
                    if kdx == jdx or kdx == idx: continue
                    for l in range(samples):
                        ldx = random.randint(0,len(vertices) - 1)
                        vertex3 = vertices[ldx]
                        if ldx == kdx or ldx == jdx or ldx == idx: continue
                        volume = volumeTetrahydron(vector(vertex0,vertex1), vector(vertex0,vertex2), vector(vertex0,vertex3))
                        #print(volume)
                        allSamples.append(volume)
        yAxis, binEdges = np.histogram(allSamples, range=(0, histogramLimits[propertyDescriptors.D4.value]), bins = 8)
        return self.normalise(yAxis, binEdges)

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
        self.pymesh.generate_convex_hull()
        vertexMat = self.pymesh.current_mesh().vertex_matrix()
        diameter = 0
        for u in vertexMat:
            for v in vertexMat:
                dia = dist(u,v)
                if dia > diameter:
                    diameter = dia
        self.pymesh.set_current_mesh(0)
        return diameter
    

    def getOBBVolume(self):
        minSize = self.mesh.bounding_box().min()
        maxSize = self.mesh.bounding_box().max()
        return (maxSize[0] - minSize[0]) * (maxSize[1] - minSize[1]) * (maxSize[2] - minSize[2])  
    
    def getVolume(self):
        vertices = self.mesh.vertex_matrix()
        faces = self.mesh.face_matrix()

        volume = 0.0

        for f in faces:
            vert = [vertices[i] for i in f]
            tetraVolume = np.abs(np.dot(vert[0], np.cross(vert[1], vert[2]))) / 6.0
            volume += tetraVolume


        volume = np.abs(volume)
        return volume#
    
    def getConvexHull(self):
        vertices = self.mesh.vertex_matrix()
        hull = ConvexHull(vertices)
        return hull.volume
    
    def getEccentric(self):
        vertices = self.mesh.vertex_matrix()
        V = np.zeros((3, len(vertices)))
        V[0] = getEveryElementFromEveryList(0, vertices)
        V[1] = getEveryElementFromEveryList(1, vertices)
        V[2] = getEveryElementFromEveryList(2, vertices)

        cov = np.cov(V)
        eig, vec = np.linalg.eig(cov)
        return abs(np.max(eig)) / abs(np.min(eig))
    
    def getOBB(self):
        show_aabb = True
        show_obb = True
        mesh = open3d.io.read_triangle_mesh(self.meshPath)
        obb = mesh.get_oriented_bounding_box()

        # Get axis-aligned bounding box (AABB)
        aabb = mesh.get_axis_aligned_bounding_box()
        aabb_points = aabb.get_box_points()
        aabb_line_indices = [[0, 1], [1, 6], [6, 3], [3, 0], [0, 2], [2, 5], [5, 4], [4, 7], [7, 2], [6, 4], [1, 7], [3, 5]]
        aabb_lineset = open3d.geometry.LineSet(
            points=open3d.utility.Vector3dVector(aabb_points),
            lines=open3d.utility.Vector2iVector(aabb_line_indices),
        )
        red = [255, 0, 0]
        aabb_lineset.colors = open3d.utility.Vector3dVector(np.array([red] * 12))

        obb_points = obb.get_box_points()
        obb_line_indices = [[0, 1], [1, 6], [6, 3], [3, 0], [0, 2], [2, 5], [5, 4], [4, 7], [7, 2], [6, 4], [1, 7], [3, 5]]
        obb_lineset = open3d.geometry.LineSet(
            points=open3d.utility.Vector3dVector(obb_points),
            lines=open3d.utility.Vector2iVector(obb_line_indices),
        )
        blue = [0, 0, 255]
        obb_lineset.colors = open3d.utility.Vector3dVector(np.array([blue] * 12))

        # Visualize the geometry
        to_draw = [mesh]
        to_draw.append(aabb_lineset) if show_aabb else print("Not showing Axis-Aligned Bounding Box")
        to_draw.append(obb_lineset) if show_obb else print("Not showing Oriented Bounding Box")
        open3d.visualization.draw_geometries(
            to_draw,
            width=1280,
            height=720,
            mesh_show_wireframe=True
        )
        return obb.volume()