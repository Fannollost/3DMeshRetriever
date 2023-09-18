from meshLoading import Mesh
import numpy as np
import polyscope as ps

class Renderer():
    def renderMesh(self, mesh):
        ps.init()
        vertices, faces = mesh.verticesAndFaces()
        vertices = np.array(vertices)
        faces = np.array(faces)
        ps_mesh = ps.register_surface_mesh("mesh", vertices, faces)
        ps.show()
