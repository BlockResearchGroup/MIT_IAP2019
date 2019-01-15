import compas

from compas.datastructures import Mesh
from compas.geometry import smooth_centroid

from compas_rhino.artists import MeshArtist
from compas_rhino.conduits import LinesConduit

# create mesh from an obj file
mesh = Mesh.from_obj(compas.get('faces.obj'))

# fix the corner
fixed = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

# create lines
lines = []
for u, v in mesh.edges():
    lines.append([mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)])

conduit = LinesConduit(lines, refreshrate=1)


# a callback function that update line position
def callback(k, args):

    # update points
    for key, attr in mesh.vertices(True):
        attr['x'] = vertices[key][0]
        attr['y'] = vertices[key][1]
        attr['z'] = vertices[key][2]

    segments = []
    for u, v in mesh.edges():
        a = vertices[u]
        b = vertices[v]
        segments.append([a, b])

    # update lines
    conduit.lines = segments

    conduit.redraw(k)


# create topology for smoothing
vertices = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
adjacency = [mesh.vertex_neighbors(key) for key in mesh.vertices()]

with conduit.enabled():
    # smoothing function
    smooth_centroid(
        vertices, adjacency, fixed=fixed, kmax=100, callback=callback)

# create mesh artist in for compas rhino
artist = MeshArtist(mesh, layer='mesh-out')
# draw faces
artist.draw_faces(join_faces=True)
