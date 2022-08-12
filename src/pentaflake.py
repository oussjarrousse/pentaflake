import math
import random

from .pentagon import PentaflakePentagon
from .helpers import get_random_HTML_color

# References:
# https://mathworld.wolfram.com/Pentaflake.html
# https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths

class Pentaflake:
    """A class representing the Pentaflake fractal generation."""

    def __init__(self, origin=complex(0,0), circumradius=100):
        """
        Initialise the Pentaflake instance with an origin, and a circumradius 
        for the initial Pentagon. That circumradius will determin the size of 
        the final image.
        """
        p = PentaflakePentagon(origin, circumradius)
        self.p = p
        self.ngen = 0        
        self.elements = [self.p]


    def inflate(self, 
        remove_inflated_tiles_indices=None,
    ):
        """ "Inflate" each triangle in the tiling ensemble."""
        new_elements = []
        if remove_inflated_tiles_indices == None:        
            for element in self.elements:
                new_elements.extend(element.inflate())               
        else:
            for element in self.elements:
                inflated_element = element.inflate()
                for index in sorted(remove_inflated_tiles_indices, reverse=True):
                    inflated_element.pop(index)
                new_elements.extend(inflated_element)
        self.elements = new_elements
        self.ngen += 1
        return self

    def rotate(self, theta):
        # rotate all elements theta radians 
        # around the center of the original pentagon
        origin = self.p.center
        for e in self.elements:
            e.rotate(theta, origin)
        return self


    def make_tiling(self, 
        ngen=1, 
        rotate_theta=0,        
        flip_x=False, 
        flip_y=False,
        remove_inflated_tiles_indices=None
    ):
        """
        Make the Penrose tiling by inflating ngen times.
        Depending on the configurations
        """
        if rotate_theta:
            self.rotate(rotate_theta)

        if flip_x:
            self.flip_x()

        if flip_y:
            self.flip_y()

        self.elements = [self.p]
        for gen in range(ngen):
            self.inflate(remove_inflated_tiles_indices)
        return self

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
            "random-tile-colors": False, 
        }
        self.config.update(config)
        self.config["width"] = str(self.config["width"])
        self.config["height"] = str(self.config["height"])

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
                self.config["base-stroke-width"] / self.ngen
            )
        else:
            stroke_width = str(
                self.config["base-stroke-width"]
            )

        svg.append(
            '<g style="stroke:{}; stroke-width: {};'
            ' stroke-linejoin: round;">'.format(
                self.config["stroke-color"], stroke_width
            )
        )

        for e in self.elements:
            if self.config["draw-tiles"]:
                if self.config["random-tile-colors"]:
                    tile_color = get_random_HTML_color()
                else:
                    tile_color = self.config["tile_color"]
                svg.append(
                    '<path fill="{}" fill-opacity="{}" d="{}"/>'.format(
                        tile_color,
                        self.config["tile-opacity"],
                        e.path(),
                    )
                )
            else:
               svg.append(
                    '<path fill="none" d="{}"/>'.format(
                        e.path(),
                    )
                )

        svg.append("</g>\n</svg>")
        return "\n".join(svg)

    def write_svg(self, ngen=1, filename="pentaflake.svg"):
        """Make and write the SVG for the tiling to filename."""
        self.make_tiling(ngen)
        svg = self.make_svg()
        with open(filename, "w") as fo:
            fo.write(svg)
        

