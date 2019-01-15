from compas.geometry import Line
from compas.plotters import Plotter

# create a line
line = Line([0, 0, 0], [1, 1, 1])
# compute a line midpoint
mid_pt = line.midpoint
print(mid_pt)

# create a plotter with figsize=(10, 6)
plotter = Plotter(figsize=(10, 6))

# create lines to draw
lines = [{'start': line.start, 'end': line.end, 'width': 1.0}]
# create start points to draw
points = [{
    'pos': line.start,
    'radius': 0.05,
    'facecolor': '#ffffff',
    'text': 'start_point: {}'.format(line.start)
}]

# create mid point to draw
points.append({'pos': mid_pt, 'radius': 0.05, 'facecolor': '#ff0000'})

# draw lines and points
plotter.draw_lines(lines)
plotter.draw_points(points)

# plot
plotter.show()
