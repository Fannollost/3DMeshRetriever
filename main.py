import os.path
import polyscope as ps
import numpy as np
#import pymeshlab as pymesh
import meshLoading 

path = "db/"
meshType = "Fish/"
meshId = "222.off"

def main():
    ps.init()
    vertices, faces = meshLoading.read_off(path + meshType + meshId)
    vertices = np.array(vertices)
    faces = np.array(faces)
    ps_mesh = ps.register_surface_mesh("mesh", vertices, faces)
    ps.show()

main()
