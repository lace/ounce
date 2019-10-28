import math

import pytest

from . import core as ounce


def test_all_units():
    for x in ["in", "cm", "deg", "years"]:
        assert x in ounce.all_units
    for method in ["all_units", "factor", "convert"]:
        assert method not in ounce.all_units


def test_all_units_classes():
    assert set(ounce.all_units_classes) == set(
        ["length", "weight", "angle", "time", "time_rate"]
    )


def test_units_class():
    assert ounce.units_class("cm") == "length"
    assert ounce.units_class("stone") == "weight"
    assert ounce.units_class("rad") == "angle"
    assert ounce.units_class("sec") == "time"
    assert ounce.units_class("") is None
    assert ounce.units_class(None) is None


def test_units_in_class():
    assert "m" in ounce.units_in_class("length")


def test_lengths():
    assert "m" in ounce.lengths


def test_weights():
    assert "lb" in ounce.weights


def test_angles():
    assert "degrees" in ounce.angles


def test_times():
    assert "sec" in ounce.times


def test_time_rates():
    assert "hours_per_week" in ounce.time_rates


def test_default_units():
    assert ounce.default_units() == {
        "length": "cm",
        "weight": "kg",
        "angle": "deg",
        "time": "yr",
        "time_rate": "hours_per_week",
    }


def test_raw():
    assert ounce.raw("m") == 1.0
    assert ounce.raw("mm") == 0.001


def test_factor():
    with pytest.raises(
        ValueError,
        match=r"Can\'t convert between apples and oranges \(stone and fathoms\)",
    ):
        ounce.factor("stone", "fathoms")

    nones = [(None, ""), ("", None), (None, None), ("", "")]
    for value in nones:
        assert ounce.factor(*value) == 1.0

    assert ounce.factor("in", "cm") == 2.54
    assert ounce.factor("year", "min") == pytest.approx(525600, 1e-3)
    assert ounce.factor("sec", "hr", units_class="time") == 1.0 / 3600

    with pytest.raises(ValueError, match=r"Units class must be length, but got time"):
        ounce.factor("sec", "hr", units_class="length")


def test_convert():
    assert ounce.convert(25, "cm", "mm")[0] == 250
    assert ounce.convert(180, "deg", "rad")[0] == math.pi
    assert ounce.convert(-10, "ft", "in")[0] == pytest.approx(-120)

    assert ounce.convert(25, "cm", "mm")[1] == "mm"
    assert ounce.convert(180, "deg", "rad")[1] == "rad"
    assert ounce.convert(-10, "ft", "in")[1] == "in"
    assert ounce.convert(None, "ft", "in") == (None, None)


def test_conversion_factors():
    assert ounce.convert(25, "cm", "m")[0] == 0.25
    assert ounce.convert(25, "cm", "cm")[0] == 25
    assert ounce.convert(25, "cm", "mm")[0] == 250
    assert ounce.convert(25, "cm", "in")[0] == pytest.approx(9.8425197)  # From Google
    assert ounce.convert(25, "cm", "ft")[0] == pytest.approx(0.82021)  # From Google.
    assert ounce.convert(25, "cm", "fathoms")[0] == pytest.approx(
        0.136701662
    )  # From Google.
    assert ounce.convert(25, "cm", "cubits")[0] == pytest.approx(
        0.546806649
    )  # From Google.
    assert ounce.convert(10, "kg", "kg")[0] == 10
    assert ounce.convert(1, "kg", "g")[0] == 1000
    assert ounce.convert(10, "kg", "lbs")[0] == 22.0462  # From Google.
    assert ounce.convert(10, "kg", "stone")[0] == 1.57473  # From Google.
    assert ounce.convert(90, "deg", "rad")[0] == math.pi / 2.0
    assert ounce.convert(90, "deg", "deg")[0] == 90
    assert ounce.convert(30, "min", "sec")[0] == 30 * 60
    assert ounce.convert(30, "min", "minutes")[0] == 30
    assert ounce.convert(30, "min", "hours")[0] == 0.5
    assert ounce.convert(2, "days", "min")[0] == 2 * 24 * 60
    assert ounce.convert(1, "years", "min")[0] == 525948.48


def test_convert_list():
    assert ounce.convert_list([10, 20, 30], "cm", "mm") == [100, 200, 300]


def test_convert_to_system_default():
    assert ounce.convert_to_system_default(10, "mm") == (1, "cm")

    result = (
        ounce.convert_to_system_default(10, "mm", "united_states"),
        (0.393701, "in"),
    )
    assert result[0][0] == pytest.approx(result[1][0], 1e-6)
    assert result[0][1] == result[1][1]

    result = (
        ounce.convert_to_system_default(10, "stone", "united_states"),
        (140, "lb"),
    )
    assert result[0][0] == pytest.approx(result[1][0], 1e-4)
    assert result[0][1] == result[1][1]

    assert ounce.convert_to_system_default(10, "") == (10, "")


def test_prettify():
    assert ounce.prettify(182.13992, "cm") == (182.0, "cm", 71.75, "in")
    assert ounce.prettify(1821.3992, "mm") == (182.0, "cm", 71.75, "in")
    assert ounce.prettify(-182.13992, "cm") == (-182.0, "cm", -71.75, "in")
    assert ounce.prettify(182.13992, "cm", precision=2) == (182.14, "cm", 71.71, "in")
    assert ounce.prettify(182.13992, "cm", precision=4) == (
        182.1399,
        "cm",
        71.7086,
        "in",
    )
