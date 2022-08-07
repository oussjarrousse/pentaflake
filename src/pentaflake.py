import math
import random

from .pentagon import PentaflakePentagon

# References:
# https://mathworld.wolfram.com/Pentaflake.html
# https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths

# A small tolerance for comparing floats for equality

class Pentaflake:
    """A class representing the Pentaflake fractal generation."""

    def __init__(self, origin=complex(0,0), circumradius=100, config={}):
        """
        Initialise the PenroseP1 instance with a scale determining the size
        of the final image and the number of generations, ngen, to inflate
        the initial triangles. Further configuration is provided through the
        key, value pairs of the optional config dictionary.

        """

        self.config = {
            "width": "100%",
            "height": "100%",
            "scale": 100,
            "stroke-colour": "#999",
            "draw-tiles": True,
            "base-stroke-width": 0.05,
            "margin": 1.05,
            "tile-opacity": 0.6,
            "random-tile-colours": False,
            "rotate": 0,
            "flip-y": False,
            "flip-x": False,
        }
        self.config.update(config)
        self.config["width"] = str(self.config["width"])
        self.config["height"] = str(self.config["height"])

        p = PentaflakePentagon(origin, circumradius)
        self.p = p
        self.elements = [self.p]


    def inflate(self):
        """ "Inflate" each triangle in the tiling ensemble."""
        new_elements = []
        for element in self.elements:
            new_elements.extend(element.inflate())
        self.elements = new_elements


    def make_svg(self):
        """Make and return the SVG for the tiling as a str."""

        # https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths

        # xmin = ymin = -self.scale * self.config["margin"]
        # width = height = 2 * self.scale * self.config["margin"]
        # viewbox = "{} {} {} {}".format(xmin, ymin, width, height)

        # width = height = 10
        viewbox = "0 0 {} {}".format(self.config["width"], self.config["width"])
        # print(viewbox)

        svg = [
            '<?xml version="1.0" encoding="utf-8"?>',
            '<svg width="{}" height="{}" viewBox="{}"'
            # ' preserveAspectRatio="xMidYMid meet" version="1.1"'
            ' baseProfile="full" xmlns="http://www.w3.org/2000/svg">'.format(
                self.config["width"], self.config["height"], viewbox
            ),
        ]
        if self.ngen > 0:
            stroke_width = str(
                self.config["scale"] * self.config["base-stroke-width"] / self.ngen
            )
        else:
            stroke_width = str(
                self.config["scale"] * self.config["base-stroke-width"]
            )

        svg.append(
            '<g style="stroke:{}; stroke-width: {};'
            ' stroke-linejoin: round;">'.format(
                self.config["stroke-colour"], stroke_width
            )
        )
        # draw_rhombuses = self.config["draw-rhombuses"]
        for e in self.elements:
            if self.config["draw-tiles"]:
                svg.append(
                    '<path fill="{}" fill-opacity="{}" d="{}"/>'.format(
                        self.get_tile_colour(e),
                        self.config["tile-opacity"],
                        e.path(),
                    )
                )
            else:
               svg.append(
                    '<path fill="none" d="{}"/>'.format(
                        self.get_tile_colour(e),
                        self.config["tile-opacity"],
                        e.path(),
                    )
                )

        svg.append("</g>\n</svg>")
        return "\n".join(svg)


    def get_tile_colour(self, e):
        """Return a HTML-style colour string for the tile."""
        return "#" + hex(random.randint(0, 0xFFF))[2:]


    def make_tiling(self, ngen=1):
        """Make the Penrose tiling by inflating ngen times."""
        self.elements = [self.p]
        for gen in range(ngen):
            self.inflate()

        self.ngen = ngen

        # Rotate the figure anti-clockwise by theta radians.
        # theta = self.config["rotate"]
        # if theta:
        #     self.rotate(theta)

        # # Flip the image about the y-axis (note this occurs _after_ any
        # # rotation.
        # if self.config["flip-y"]:
        #     self.flip_y()

        # # Flip the image about the x-axis (note this occurs _after_ any
        # # rotation and after any flip about the y-axis.
        # if self.config["flip-x"]:
        #     self.flip_x()

    def write_svg(self, ngen=1, filename="pentaflake.svg"):
        """Make and write the SVG for the tiling to filename."""
        self.make_tiling(ngen)
        svg = self.make_svg()
        with open(filename, "w") as fo:
            fo.write(svg)

