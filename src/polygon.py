import math

from .helpers import get_random_HTML_color


class Polygon:
    def __init__(self, vertices):
        self.vertices = vertices

    @property
    def n(self):
        return len(self.vertices)

    def translate(self, c: complex):
        new_vertices = list()
        for vertex in self.vertices:
            new_vertices.append(vertex + c)
        self.vertices = new_vertices
        return self

    def rotate(self, theta, origin):
        """Rotate the figure anti-clockwise by theta radians."""
        rot = math.cos(theta) + 1j * math.sin(theta)
        new_vertices = list()
        for vertex in self.vertices:
            new_vertices.append((vertex - origin) * rot + origin)
        self.vertices = new_vertices
        return self

    def scale(self, scale: complex):
        new_vertices = list()
        for vertex in self.vertices:
            new_vertices.append(
                complex(
                    vertex.real / scale_factor.real, vertex.imag / scale_factor.imag
                )
            )
        self.vertices = new_vertices
        return self

    @property
    def bounding_box(self):
        """
        returns two points top left and bottom right

        """
        bounding_box_upper_left = self.vertices[0]
        bounding_box_bottom_right = self.vertices[0]
        for vertice in self.vertices[1:]:
            if vertice.real > bounding_box_bottom_right.real:
                bounding_box_bottom_right.real = vertice.real
            if vertice.real < bounding_box_upper_left.real:
                bounding_box_upper_left.real = vertice.real
            if vertice.imag > bounding_box_upper_left.imag:
                bounding_box_upper_left.imag = vertice.imag
            if vertice.imag < bounding_box_bottom_right.imag:
                bounding_box_bottom_right.imag = vertice.imag

        return bounding_box_upper_left, bounding_box_bottom_right, width, height


class RegularPolygon(Polygon):
    def __init__(self, origin, circumradius, n):
        rotational_symmetry_radians = 2 * math.pi / n
        self.vertices = list()
        for i in range(n):
            self.vertices.append(
                origin
                + circumradius
                * complex(
                    math.cos(i * rotational_symmetry_radians),
                    math.sin(i * rotational_symmetry_radians),
                )
            )
        self.circumradius = circumradius
        self.origin = origin

    @property
    def center(self):
        """
        Return the position of the center of the rhombus formed from two
        triangles joined by their bases.
        """
        return sum(self.vertices) / self.n

    @property
    def circumradius(self):
        """
        Getter function for the circumradius property of the pentagon
        """
        return self._circumradius

    @circumradius.setter
    def circumradius(self, circumradius):
        """
        Getter function for the circumradius property of the pentagon
        """

        self._circumradius = circumradius

    @property
    def inradius(self):
        # https://en.wikipedia.org/wiki/Pentagon#Regular_pentagons
        return self.circumradius * math.cos(math.pi / self.n)
        # return self.side_length / (2 * math.tan(math.pi/n))

    @property
    def side_length(self):
        """ """
        return 2 * self.circumradius * math.sin(math.pi / self.n)

    @property
    def height(self):
        # https://en.wikipedia.org/wiki/Pentagon#Regular_pentagons
        return self.circumradius + self.inradius

    def path(self):
        """
        Return the SVG "d" path element specifier for the rhombus formed
        by this triangle and its mirror image joined along their bases. If
        rhombus=False, the path for the triangle itself is returned instead.

        """
        edges = tuple()
        xy = lambda v: (v.real, v.imag)
        origin = self.origin
        path = "m{},{} ".format(*xy(self.vertices[0]))

        for i in range(self.n - 1):
            dl = self.vertices[(i + 1)] - self.vertices[i]
            path += "l{},{} ".format(*xy(dl))
        path += "z"

        return path

    def make_svg(self, config={}):
        """Make and return the SVG for the tiling as a str."""
        self.config = {
            "width": "600",
            "height": "600",
            "stroke-color": "#000",
            "draw-tiles": True,
            "tile_color": "#000",
            "base-stroke-width": 5,
            "margin": 1.05,
            "tile-opacity": 1,
            "random-tile-colors": True,
        }
        self.config.update(config)
        self.config["width"] = str(self.config["width"])
        self.config["height"] = str(self.config["height"])

        viewbox = "0 0 {} {}".format(self.config["width"], self.config["width"])

        svg = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<svg width="{}" height="{}" viewBox="{}"'
            # ' preserveAspectRatio="xMidYMid meet" version="1.1"'
            ' baseProfile="full" xmlns="http://www.w3.org/2000/svg">'.format(
                self.config["width"], self.config["height"], viewbox
            ),
        ]
        stroke_width = str(self.config["base-stroke-width"])

        svg.append(
            '<g style="stroke:{}; stroke-width: {};'
            ' stroke-linejoin: round;">'.format(
                self.config["stroke-color"], stroke_width
            )
        )

        if self.config["draw-tiles"]:
            if self.config["random-tile-colors"]:
                tile_color = get_random_HTML_color()
            else:
                tile_color = self.config["tile_color"]
            svg.append(
                '<path fill="{}" fill-opacity="{}" d="{}"/>'.format(
                    tile_color,
                    self.config["tile-opacity"],
                    self.path(),
                )
            )
        else:
            svg.append(
                '<path fill="none" d="{}"/>'.format(
                    self.path(),
                )
            )

        svg.append("</g>\n</svg>")
        return "\n".join(svg)
