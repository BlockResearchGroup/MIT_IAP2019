import rhinoscriptsyntax as rs

from compas.datastructures import Mesh
from compas.geometry import scale_vector
from compas.geometry import add_vectors
from compas.geometry import flatness
from compas.utilities import i_to_rgb
from compas_rhino.utilities import get_line_coordinates


def draw_interface(vertices, faces, maxdev):
    # don't refresh viewport
    rs.EnableRedraw(False)
    # compute level of flatness
    flat_vals = flatness(vertices, faces, maxdev)

    srfs = []
    for i, face in enumerate(faces):
        # vertex coordinates for face
        pts = [vertices[key] for key in face]
        # create Rhino surface
        srfs.append(rs.AddSrfPt(pts))
        # color surface based on flatness
        rgb = i_to_rgb(flat_vals[i])
        rs.ObjectColor(srfs[-1], rgb)

    rs.AddObjectsToGroup(srfs, rs.AddGroup())
    # refresh viewport
    rs.EnableRedraw(True)


if __name__ == '__main__':

    thickness = 0.2

    edge_crvs = rs.GetObjects("Select edges", 4)
    lines = get_line_coordinates(edge_crvs)

    mesh = Mesh.from_lines(lines, delete_boundary_face=True)

    # compute offset points top (a)
    vertices_list = []
    key_index_a = {}
    for i, key in enumerate(mesh.vertices()):
        pt = mesh.vertex_coordinates(key)
        normal = mesh.vertex_normal(key)
        vertices_list.append(
            add_vectors(pt, scale_vector(normal, thickness * .5)))
        # create key_index map top (a)
        key_index_a[key] = i

    # compute offset points bottom (b)
    n = mesh.number_of_vertices()
    key_index_b = {}
    for i, key in enumerate(mesh.vertices()):
        pt = mesh.vertex_coordinates(key)
        normal = mesh.vertex_normal(key)
        vertices_list.append(
            add_vectors(pt, scale_vector(normal, thickness * -.5)))
        # create key_index map bottom (b)
        key_index_b[key] = i + n

    # create faces for interfaces (voussoirs/blocks)
    faces_list = []
    for u, v in mesh.edges():
        faces_list.append(
            [key_index_a[u], key_index_a[v], key_index_b[v], key_index_b[u]])

    # draw and group interfaces
    maxdev = 0.015
    draw_interface(vertices_list, faces_list, maxdev)
