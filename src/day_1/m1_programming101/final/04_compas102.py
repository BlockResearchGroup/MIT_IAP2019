import compas

from compas.datastructures import Mesh
from compas.geometry import smooth_centroid

from compas.plotters import Plotter

# create mesh from an obj file
mesh = Mesh.from_obj(compas.get('faces.obj'))

# fix the corner
fixed = [key for key in mesh.vertices() if mesh.vertex_degree(key) == 2]

# create points
points = []
for key in mesh.vertices():
    points.append({
        'pos':
        mesh.vertex_coordinates(key),
        'radius':
        0.1,
        'facecolor':
        '#ff0000' if mesh.vertex_degree(key) == 2 else '#ffffff'
    })

# create lines
lines = []
for u, v in mesh.edges():
    lines.append({
        'start': mesh.vertex_coordinates(u),
        'end': mesh.vertex_coordinates(v),
        'width': 1.0
    })

# initial plotter
plotter = Plotter(figsize=(10, 6))

# draw points and lines
pcoll = plotter.draw_points(points)
lcoll = plotter.draw_lines(lines)


# a callback function that update line and point positions
def callback(k, args):
    # update points
    plotter.update_pointcollection(pcoll, vertices, 0.1)

    segments = []
    for u, v in mesh.edges():
        a = vertices[u]
        b = vertices[v]
        segments.append([a, b])

    # update lines
    plotter.update_linecollection(lcoll, segments)
    # update plotter
    plotter.update(pause=0.001)


# create topology for smoothing
vertices = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
adjacency = [mesh.vertex_neighbors(key) for key in mesh.vertices()]

# smoothing function
smooth_centroid(vertices, adjacency, fixed=fixed, kmax=100, callback=callback)

# plot
plotter.show()
