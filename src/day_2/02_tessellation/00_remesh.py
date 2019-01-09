import rhinoscriptsyntax as rs

from compas.datastructures import Mesh

from compas.topology import trimesh_remesh
from compas.topology import delaunay_from_points
from compas.topology import mesh_dual

from compas.utilities import geometric_key

from compas_rhino.artists.meshartist import MeshArtist
from compas_rhino.conduits import MeshConduit


def sort_pts(sets_pts):
    # sorts point sets for coons patch

    # sort point sets in a "continous chain"
    end_pt = sets_pts[0][-1]
    new_sets_pts = [sets_pts[0]]
    sets_pts.pop(0)

    while True:
        flag = True
        for i, set_pts in enumerate(sets_pts):
            if geometric_key(set_pts[0]) == geometric_key(end_pt):
                end_pt = set_pts[-1]
                new_sets_pts.append(set_pts)
                sets_pts.pop(i)
                flag = False
            elif geometric_key(set_pts[-1]) == geometric_key(end_pt):
                end_pt = set_pts[0]
                set_pts.reverse()
                new_sets_pts.append(set_pts)
                sets_pts.pop(i)
                flag = False

        if flag: break

    return new_sets_pts


# callback function executed inside the smoothing loop
def callback(mesh, k, args):
    if k % 10 == 0:
        rs.Prompt(str(k))

    srf = args[0]

    # constrain all non-fixed to a surface
    for key, attr in mesh.vertices(data=True):
        if key in fixed:
            continue

        x, y, z = rs.BrepClosestPoint(srf, mesh.vertex_coordinates(key))[0]
        attr['x'] = x
        attr['y'] = y
        attr['z'] = z

    conduit.redraw()


if __name__ == '__main__':

    # set the remeshing parameters
    trg_l = 0.65
    kmax = 300

    crvs = rs.GetObjects("Select boundary curves", 4)
    srf = rs.GetObject("Select nurbs srf", 8)

    sets_pts = [
        rs.DivideCurve(crv, round(rs.CurveLength(crv) / trg_l, 0))
        for crv in crvs
    ]

    sets_pts = sort_pts(sets_pts)

    # cull duplicate points
    points = []
    for pts in sets_pts:
        points += pts[1:]

    # construct delaunay mesh
    faces = delaunay_from_points(points, boundary=points)
    mesh = Mesh.from_vertices_and_faces(points, faces)

    # set fixed vertices
    fixed = set(mesh.vertices_on_boundary())

    #    artist = MeshArtist(mesh, layer='delaunay')
    #    artist.draw_faces(join_faces=True)

    conduit = MeshConduit(mesh, refreshrate=2)

    # run remeshing algorithm
    with conduit.enabled():
        trimesh_remesh(
            mesh,
            target=trg_l,
            kmax=kmax,
            tol=0.1,
            divergence=0.01,
            allow_boundary_split=True,
            allow_boundary_swap=True,
            allow_boundary_collapse=False,
            smooth=True,
            fixed=fixed,
            callback=callback,
            callback_args=[srf])

    artist = MeshArtist(mesh, layer='remeshed')
    artist.draw()
