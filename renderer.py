from meshLoading import Mesh
import numpy as np
import polyscope as ps
import open3d as o3d

class Renderer():
    # Use polyscope to draw the model and allow switching between smooth-shaded. May also draw wireframe (but not when mesh is transparent)
    def renderMesh(self, mesh):
        ps.init()
        vertices, faces = mesh.verticesAndFaces()
        vertices = np.array(vertices)
        faces = np.array(faces)
        ps_mesh = ps.register_surface_mesh("mesh", vertices, faces)
        ps.show()
    # Use Open3D to show wireframe of model
    def renderWireFrame(self, file):
        # Load the mesh with open3d
        mesh = o3d.io.read_triangle_mesh(file)
        mesh.compute_vertex_normals()

         # We first need to obtain a lineset of the wireframe if we don't want to render the mesh itself
        wireframe = o3d.geometry.LineSet.create_from_triangle_mesh(mesh) 
        o3d.visualization.draw_geometries([wireframe], width=1280, height=720)
