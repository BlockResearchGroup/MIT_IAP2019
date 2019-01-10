import rhinoscriptsyntax as rs

from compas.datastructures import Mesh
from compas.geometry import scale_vector
from compas.geometry import add_vectors
from compas.geometry import planarize_faces
from compas.geometry import bounding_box
from compas_rhino.utilities import get_line_coordinates
from compas_rhino.artists.meshartist import MeshArtist


def callback(k, callback_args=None):
    if k % 5 == 0:
        rs.Prompt('Iteration: {0} '.format(k))


if __name__ == '__main__':

    # define min/max shell thickness
    thickness_max = 0.4
    thickness_min = 0.1
    new_z_delta = thickness_max - thickness_min

    # select tessellation
    edge_crvs = rs.GetObjects("Select edges", 4)
    lines = get_line_coordinates(edge_crvs)

    mesh = Mesh.from_lines(lines, delete_boundary_face=True)

    # find z-max and z-min of the tessellation geomerty
    bb = bounding_box(mesh.get_vertices_attributes(('x', 'y', 'z')))
    print(bb)
    z_max = bb[0][2]
    z_min = bb[4][2]
    z_delta = z_max - z_min

    vertices_list = []
    # compute offset points top (a)
    key_index_a = {}
    for i, key in enumerate(mesh.vertices()):
        pt = mesh.vertex_coordinates(key)
        normal = mesh.vertex_normal(key)
        thickness = (((pt[2] - z_min) * new_z_delta) / z_delta) + thickness_min
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
        thickness = (((pt[2] - z_min) * new_z_delta) / z_delta) + thickness_min
        vertices_list.append(
            add_vectors(pt, scale_vector(normal, thickness * -.5)))
        # create key_index map bottom (b)
        key_index_b[key] = i + n

    # create faces for interfaces (voussoirs/blocks)
    faces_list = []
    for u, v in mesh.edges():
        faces_list.append(
            [key_index_a[u], key_index_a[v], key_index_b[v], key_index_b[u]])

    # planarize interfaces
    if 1:
        planarize_faces(vertices_list, faces_list, kmax=150, callback=callback)
        layer = 'voussoirs_planar'
    else:
        layer = 'voussoirs_ruled'

    # create mesh per voussoir/block
    voussoirs_meshes = {}
    for fkey in mesh.faces():

        # initiate mesh object
        voussoir_mesh = Mesh()
        # loop over edges of face (fkey)
        for u, v in mesh.face_halfedges(fkey):
            # add top vertices of face
            x, y, z = vertices_list[key_index_a[u]]
            voussoir_mesh.add_vertex(key_index_a[u], x=x, y=y, z=z)

            # add bottom vertices of face
            x, y, z = vertices_list[key_index_b[u]]
            voussoir_mesh.add_vertex(key_index_b[u], x=x, y=y, z=z)

            # add interfaces
            face = [
                key_index_a[v], key_index_a[u], key_index_b[u], key_index_b[v]
            ]
            voussoir_mesh.add_face(face)

        # add top and bottom faces
        face_a = [key_index_a[key] for key in mesh.face_vertices(fkey)]
        face_b = [key_index_b[key] for key in mesh.face_vertices(fkey)]
        face_b.reverse()
        voussoir_mesh.add_face(face_a)
        voussoir_mesh.add_face(face_b)

        voussoirs_meshes[fkey] = voussoir_mesh

    # draw all voussoir meshes
    for fkey, voussoir_mesh in voussoirs_meshes.items():
        artist = MeshArtist(voussoir_mesh, layer=layer)
        artist.draw_faces(join_faces=True)

    artist.redraw()
