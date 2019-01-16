# This simple example is to show travel quad mesh in row

import rhinoscriptsyntax as rs

from compas.datastructures import Mesh
from compas_rhino import get_line_coordinates

from compas_rhino.artists.meshartist import MeshArtist
from compas_rhino.helpers import mesh_select_edge


def get_parallel_edges(mesh, uv):

    edges = [uv]

    u, v = uv
    # process from edge uv in both directions
    for a, b in [(u, v), (v, u)]:

        # search until a boundary or the starting edge is reached
        while True:
            # face on one side of the edge
            fkey = mesh.halfedge[a][b]

            # check for boundary
            if fkey is None:
                break

            # get all vertices of the face
            vertices = mesh.face_vertices(fkey)

            # for a quad mesh we know exactly the opposite face edge
            i = vertices.index(a)
            a = vertices[i - 1]
            b = vertices[i - 2]

            # check if the starting edge is reached
            if (a, b) in edges or (b, a) in edges:
                break

            edges.append((a, b))

    return [(u, v) for u, v in edges]


if __name__ == '__main__':

    crvs = rs.GetObjects("Select mesh edges", 4)
    lines = get_line_coordinates(crvs)

    mesh = Mesh.from_lines(lines, delete_boundary_face=True)

    artist = MeshArtist(mesh, layer='new_lines')
    artist.draw_edges()
    artist.redraw()

    # select edge
    rs.HideObjects(crvs)
    edge = mesh_select_edge(mesh, "select a mesh edge")
    rs.ShowObjects(crvs)

    # select edge
    artist.clear_edges()

    # find "every second" edge (joint lines)
    new_lines = []

    para_edges = get_parallel_edges(mesh, edge)
    for u, v in para_edges[2::2]:
        new_lines.append((u, v))

    # draw new lines
    artist.draw_edges(keys=new_lines, color=(255, 0, 0))
    artist.redraw()
