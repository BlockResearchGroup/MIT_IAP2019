import compas_rhino

from compas.datastructures import Mesh
from compas_rhino.helpers import mesh_from_guid
from compas_rhino.artists.meshartist import MeshArtist
from compas.topology import mesh_dual


def my_mesh_dual(mesh, cls=None):
    """Construct the dual of a mesh."""
    if not cls:
        cls = type(mesh)

    dual = cls()

    fkey_centroid = {fkey: mesh.face_centroid(fkey) for fkey in mesh.faces()}
    outer = mesh.vertices_on_boundary()
    inner = list(set(mesh.vertices()) - set(outer))
    # print(set(mesh.vertices()))
    # print('vertice', set(mesh.vertices()))
    # print('outer', outer)
    # print('inner', inner)
    vertices = {}
    faces = {}

    # inner faces
    for key in inner:
        fkeys = mesh.vertex_faces(key, ordered=True)
        for fkey in fkeys:
            if fkey not in vertices:
                vertices[fkey] = fkey_centroid[fkey]
        faces[key] = fkeys

    # boundary condition
    for key in outer:
        fkeys = mesh.vertex_faces(key, ordered=True)
        if len(fkeys) > 1:
            for fkey in fkeys:
                if fkey not in vertices:
                    vertices[fkey] = fkey_centroid[fkey]

            vkeys = reversed(mesh.vertex_neighbors(key, ordered=True))
            for i, v in enumerate(vkeys):
                if mesh.is_edge_on_boundary(key, v) and (
                        len(fkey_centroid) * (i + 1) + fkey) not in vertices:
                    vertices[len(fkey_centroid) * (i + 1) +
                             fkey] = mesh.edge_midpoint(key, v)
                    fkeys.append(len(fkey_centroid) * (i + 1) + fkey)

            faces[key] = fkeys

    for key, (x, y, z) in vertices.items():
        dual.add_vertex(key, x=x, y=y, z=z)

    for fkey, vertices in faces.items():
        dual.add_face(vertices, fkey=fkey)

    return dual


if __name__ == '__main__':

    guid = compas_rhino.select_mesh()
    mesh = mesh_from_guid(Mesh, guid)

    # call the function from the compas dual_mesh
    # dual_mesh = mesh_dual(mesh)
    compas_rhino.clear_layer('my_dual')

    # make my own dula mesh with edge condition
    dual_mesh = my_mesh_dual(mesh)
    # print(dual_mesh)

    artist = MeshArtist(dual_mesh, layer='my_dual')
    artist.draw_edges(color=[255, 0, 0])

    # artist.draw_faces(join_faces=True)

    artist.redraw()
