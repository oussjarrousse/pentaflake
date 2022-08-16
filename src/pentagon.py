import cmath
import math

from .helpers import phi
from .polygon import Polygon
from .polygon import RegularPolygon

# References:
# https://en.wikipedia.org/wiki/Pentagon#Regular_pentagons
# https://archive.lib.msu.edu/crcmath/math/math/p/p195.htm
# https://mathworld.wolfram.com/Pentaflake.html


rotational_symmetry_radians = 2 * math.pi / 5
rotational_symmetry_radians_2 = math.pi / 5
rotational_symmetry_radians_2 = math.pi
# phi = (1 + math.sqrt(5)) / 2


class Pentagon(Polygon):
    """
    A class representing a pentagon.

    """

    def __init__(self, vertices):
        """
        Initialize the triangle with the ordered vertices. A and C are the
        vertices at the equal base angles; B is at the vertex angle.

        """

        super().__init__(vertices)


class RegularPentagon(RegularPolygon):
    """
    A class representing an Equilateral Pentagon.

    """

    def __init__(self, origin, circumradius):
        """
        Initialize the RegularPentagon and generate the vertices based on Origin and circumradius.
        """

        # self.vertices = list()
        # for i in range(5):
        #     self.vertices.append(
        #         origin
        #         + circumradius
        #         * complex(
        #             math.cos(i * rotational_symmetry_radians),
        #             math.sin(i * rotational_symmetry_radians),
        #         )
        #     )
        # self.circumradius = circumradius
        super().__init__(origin=origin, circumradius=circumradius, n=5)

    def path(self):
        """
        Return the SVG "d" path element specifier for the rhombus formed
        by this triangle and its mirror image joined along their bases. If
        rhombus=False, the path for the triangle itself is returned instead.

        """
        edges = tuple()
        xy = lambda v: (v.real, v.imag)
        origin = self.center
        path = "m{},{} ".format(*xy(self.vertices[0]))

        for i in range(self.n - 1):
            dl = self.vertices[(i + 1)] - self.vertices[i]
            path += "l{},{} ".format(*xy(dl))
        path += "z"

        return path

    def conjugate(self):
        """
        Return the vertices of the reflection of this pentagon about the
        x-axis. Since the vertices are stored as complex numbers, we simply
        need the complex conjugate values of their values.

        """
        return self.__class__([vertex.conjugate() for vertex in self.vertices])


class PentaflakePentagon(RegularPentagon):

    mark = False

    def inflate(self):
        s = self.side_length / (1 + phi)
        R = s * math.sqrt((5 + math.sqrt(5)) / 10)
        d = R * phi
        v = self.vertices[0] - self.center

        c1 = self.center
        p1 = PentaflakePentagon(c1, R)

        if self.mark == False:
            p1.rotate(rotational_symmetry_radians_2, c1)
            p1.mark = True
        else:
            p1.mark = False

        c2 = c1 + cmath.rect(d, cmath.phase(v))
        p2 = PentaflakePentagon(c2, R)
        if self.mark == True:
            p2.rotate(rotational_symmetry_radians_2, c2)
            p2.mark = True

        c3 = c1 + cmath.rect(d, cmath.phase(v) + rotational_symmetry_radians)
        p3 = PentaflakePentagon(c3, R)
        if self.mark == True:
            p3.rotate(rotational_symmetry_radians_2, c3)
            p3.mark = True

        c4 = c1 + cmath.rect(d, cmath.phase(v) + 2 * rotational_symmetry_radians)
        p4 = PentaflakePentagon(c4, R)
        if self.mark == True:
            p4.rotate(rotational_symmetry_radians_2, c4)
            p4.mark = True

        c5 = c1 + cmath.rect(d, cmath.phase(v) + 3 * rotational_symmetry_radians)
        p5 = PentaflakePentagon(c5, R)
        if self.mark == True:
            p5.rotate(rotational_symmetry_radians_2, c5)
            p5.mark = True

        c6 = c1 + cmath.rect(d, cmath.phase(v) + 4 * rotational_symmetry_radians)
        p6 = PentaflakePentagon(c6, R)
        if self.mark == True:
            p6.rotate(rotational_symmetry_radians_2, c6)
            p6.mark = True

        return [p1, p2, p3, p4, p5, p6]
