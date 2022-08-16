import pytest

from src.polygon import Polygon


@pytest.mark.UNIT
def test_polygon_init():
    vertices = []
    p = Polygon(vertices)
    assert p.vertices is not None
    assert len(p.vertices) == 0

    vertices = [complex(0, 0), complex(0, 1)]

    p = Polygon(vertices)
    assert p.vertices is not None
    assert len(p.vertices) == 2
    for i, _ in enumerate(vertices):
        assert p.vertices[i] == vertices[i]


@pytest.mark.UNIT
def test_polygon_translate():
    vertices = [
        complex(0, 0),
        complex(0, 1),
        complex(1, 1),
        complex(1, 0),
    ]

    p = Polygon(vertices)
    c = complex(10, 20)
    p.translate(c)
    for i, vertice in enumerate(vertices):
        assert p.vertices[i] == vertice + c
