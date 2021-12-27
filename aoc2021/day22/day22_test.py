from itertools import product

from aoc2021.day22.day22 import Action, gen_cubes, size, overlap_cube, one_d_case


def test_gen_cubes():
    expected = product((10, 11), (10, 11), (10, 11))
    assert tuple(expected) == tuple(gen_cubes(Action(True, (10, 11), (10, 11), (10, 11))))


def test_overlap_cube():
    first = Action(True, (1, 2), (1, 2), (1, 2))
    second = Action(True, (5, 6), (5, 6), (5, 5))
    assert overlap_cube(first, second) is None

    first = Action(True, (1, 2), (1, 2), (1, 2))
    second = Action(True, (2, 3), (2, 3), (2, 3))
    assert overlap_cube(first, second) == Action(True, (2, 2), (2, 2), (2, 2))


def test_one_d_case():
    assert (2, 2) == one_d_case((1, 2), (2, 3))
    assert (2, 3) == one_d_case((1, 3), (2, 4))
    assert (2, 3) == one_d_case((2, 4), (1, 3))


def test_size():
    assert 27 == size(Action(True, (10, 12), (10, 12), (10, 12)))