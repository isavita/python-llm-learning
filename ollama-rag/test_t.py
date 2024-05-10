import t
import pytest


def test_square():
    assert t.square(6) == 36


def test_square_float():
    assert t.square(5.0) == pytest.approx(25.00001)


@pytest.mark.parametrize(("input_n", "expected"), ((5, 25), (4.0, 16.0)))
def test_square_table(input_n, expected):
    assert t.square(input_n) == expected


class TestSquare:
    def test_square(self):
        assert t.square(7) == 49
