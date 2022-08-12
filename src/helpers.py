import random

phi = (1 + math.sqrt(5)) / 2

def get_random_HTML_color():
    """Return a HTML-style color string for the tile."""
    return "#" + hex(random.randint(0, 0xFFF))[2:]