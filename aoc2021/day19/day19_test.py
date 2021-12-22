from aoc2021.day19.day19 import rotate_on_axis, rotate, translate


def test_rotate_on_axis():
    data = (1, 2, 3)
    assert data == rotate_on_axis(data, "x", 0)
    assert (1, -3, 2) == rotate_on_axis(data, "x", 1)
    assert (1, -2, -3) == rotate_on_axis(data, "x", 2)
    assert (1, 3, -2) == rotate_on_axis(data, "x", 3)
    assert data == rotate_on_axis(data, "y", 0)
    assert (-3, 2, 1) == rotate_on_axis(data, "y", 1)
    assert (-1, 2, -3) == rotate_on_axis(data, "y", 2)
    assert (3, 2, -1) == rotate_on_axis(data, "y", 3)
    assert data == rotate_on_axis(data, "z", 0)
    assert (2, -1, 3) == rotate_on_axis(data, "z", 1)
    assert (-1, -2, 3) == rotate_on_axis(data, "z", 2)
    assert (-2, 1, 3) == rotate_on_axis(data, "z", 3)


def test_rotate_new():
    data = (1, 2, 3)
    assert data == rotate(data, 0)
    assert (-1, 2, -3) == rotate(data, 2)
    assert (1, -2, -3) == rotate(data, 8)
    assert (-3, 1, -2) == rotate(data, 15)
    assert (-2, 3, -1) == rotate(data, 23)


def test_translate():
    a = (404, -588, -901)
    b = (-336, 658, 858)
    result = translate(b, (68, -1246, -43), 2)
    assert a == result
