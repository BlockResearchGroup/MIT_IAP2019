# This simple example to show shortest path on network

import rhinoscriptsyntax as rs

from compas.datastructures import Network
from compas_rhino import get_line_coordinates

from compas_rhino.artists.networkartist import NetworkArtist
from compas_rhino.helpers import network_select_vertices
from compas.topology import dijkstra_path
from compas.utilities import pairwise

if __name__ == '__main__':

    crvs = rs.GetObjects("Select network edges", 4)
    lines = get_line_coordinates(crvs)

    network = Network.from_lines(lines)

    artist = NetworkArtist(network, layer='new_lines')
    artist.draw_vertices(color=(255, 0, 0))
    artist.redraw()

    # select vertices
    vertices = network_select_vertices(network, "select a network vertices")

    print(vertices)

    adjacency = {
        key: network.vertex_neighbors(key)
        for key in network.vertices()
    }

    weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}
    weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

    path = dijkstra_path(adjacency, weight, vertices[0], vertices[1])

    print(path)

    edges = []
    for u, v in pairwise(path):
        if v not in network.edge[u]:
            u, v = v, u
        edges.append((u, v))

    artist.draw_edges(keys=edges, color=(255, 0, 0))
    artist.clear_vertices()
    artist.redraw()
