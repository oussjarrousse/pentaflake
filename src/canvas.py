from .polygon import Polygon

DISTRIBUTE_EVENLY_HORIZONTALLY = 2


class Canvas:
    def __init__(self):
        self.polygons = list()

    def add_polygon(self, polygon: Polygon):
        self.polygons.append(polygon)

    def arrange(self, config):
        style = config["arrange"]
        if style & DISTRIBUTE_EVENLY_HORIZONTALLY:
            self.arrange_distribute_evenly_horizontally(float(config["width"]))

        return self

    def arrange_distribute_evenly_horizontally(self, width: float):
        # Calculate the center position of each polygon
        # width available for each polygon
        width_available = float(width) / len(self.polygons)

        # get big enough bounding box
        _, _, big_enough_bounding_box = self.polygons[0].bounding_box
        for polygon in self.polygons[1:]:
            _, _, bounding_box_relative_to_origin = polygon.bounding_box
            if bounding_box_relative_to_origin.imag > big_enough_bounding_box.imag:
                big_enough_bounding_box.imag = bounding_box_relative_to_origin.imag
            if bounding_box_relative_to_origin.real > big_enough_bounding_box.real:
                big_enough_bounding_box.real = bounding_box_relative_to_origin

        # do we need to scale
        if big_enough_bounding_box.real > width_available:
            print("scaling down polygons to fit the right width")
            scale_factor = width_available / big_enough_bounding_box.real
            print("scale factor = {}".format(scale_factor))
            for polygon in self.polygons:
                polygon.scale(complex(scale_factor, scale_factor))

        allign_height = big_enough_bounding_box.imag / 2
        # Go over polygons and translate them to center
        i = 0
        for polygon in self.polygons:
            i = i + 1
            center = polygon.center
            polygon.translate(complex(i * width_available / 2, allign_height) - center)

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
            "arrange": DISTRIBUTE_EVENLY_HORIZONTALLY,
        }
        self.config.update(config)
        self.config["width"] = str(self.config["width"])
        self.config["height"] = str(self.config["height"])

        viewbox = "0 0 {} {}".format(self.config["width"], self.config["width"])

        svg = list()
        svg.append('<?xml version="1.0" encoding="utf-8"?>')
        svg.append(
            '<svg width="{}" height="{}" viewBox="{}"'
            # ' preserveAspectRatio="xMidYMid meet" version="1.1"'
            ' baseProfile="full" xmlns="http://www.w3.org/2000/svg">'.format(
                self.config["width"], self.config["height"], viewbox
            )
        )
        stroke_width = str(self.config["base-stroke-width"])
        svg.append(
            '<g style="stroke:{}; stroke-width: {};'
            ' stroke-linejoin: round;">'.format(
                self.config["stroke-color"], stroke_width
            )
        )

        if self.config["arrange"]:
            self.arrange(self.config)

        # go over polygons and draw them
        for polygon in self.polygons:
            for element in polygon.elements:
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
