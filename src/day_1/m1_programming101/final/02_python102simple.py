# class intro: making a point and line class


class Point(object):
    """Class Point

    Attributes:
        x (float): x coord.
        y (float): y coord.
        z (float): z coord.
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Point({0}, {1}, {2})'.format(self.x, self.y, self.z)

    def __iter__(self):
        return iter([self.x, self.y, self.z])


class Line(object):
    """Class Line

    Attributes:
        p1 (point): first point.
        p2 (point): second point.
    """

    def __init__(self, p1, p2):
        self.start = p1
        self.end = p2

    def midpoint(self):
        """Point: The midpoint between start and end."""
        return Point(0.5 * (self.start.x + self.end.x),
                     0.5 * (self.start.y + self.end.y),
                     0.5 * (self.start.z + self.end.z))

    def __repr__(self):
        return 'Line({0}, {1})'.format(self.start, self.end)


if __name__ == '__main__':

    # create a line
    l1 = Line([0, 0, 0], [1, 1, 1])
    print(l1)

    # the type of start point
    print("Type of l1 is: ", type(l1.start))
    # show the start point
    print("l1 start point is: ", l1.start)
    # calculate midpoint
    print("midpoint of l1 is: ", l1.midpoint)

    p1 = Point(1, 2, 3)
    p2 = Point(2, 3, 4)
    l2 = Line(p1, p2)
    print("Line 2 is: ", l2)
