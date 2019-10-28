import math

__all__ = [
    "all_units",
    "all_units_classes",
    "units_class",
    "units_in_class",
    "lengths",
    "weights",
    "angles",
    "times",
    "time_rates",
    "default_units",
    "raw",
    "factor",
    "convert",
    "convert_list",
    "convert_to_default",
    "convert_to_system_default",
    "prettify",
]


_ureg = {}

# lengths: conversion to m
_ureg["m"] = _ureg["meter"] = _ureg["meters"] = ("length", 1.0)
_ureg["mm"] = _ureg["millimeter"] = _ureg["millimeters"] = (
    "length",
    _ureg["m"][1] / 1000,
)
_ureg["cm"] = _ureg["centimeter"] = _ureg["centimeters"] = (
    "length",
    _ureg["m"][1] / 100,
)
_ureg["in"] = _ureg["inch"] = _ureg["inches"] = ("length", 0.0254)
_ureg["ft"] = _ureg["foot"] = _ureg["feet"] = ("length", 0.3048)
_ureg["fathoms"] = ("length", 1.8288)
_ureg["cubits"] = ("length", 0.4572)

# weights: conversion to kg
_ureg["kg"] = _ureg["kilograms"] = ("weight", 1.0)
_ureg["g"] = _ureg["grams"] = ("weight", _ureg["kg"][1] / 1000)
_ureg["lbs"] = _ureg["pounds"] = _ureg["lb"] = ("weight", _ureg["kg"][1] / 2.20462)
_ureg["stone"] = ("weight", _ureg["kg"][1] / 0.157473)

# angles: conversion to degrees
_ureg["deg"] = _ureg["degrees"] = ("angle", 1.0)
_ureg["rad"] = _ureg["radians"] = ("angle", _ureg["deg"][1] * 180 / math.pi)

# time: conversion to seconds
_ureg["sec"] = _ureg["second"] = _ureg["seconds"] = ("time", 1.0)
_ureg["min"] = _ureg["minute"] = _ureg["minutes"] = ("time", _ureg["sec"][1] * 60)
_ureg["hr"] = _ureg["hour"] = _ureg["hours"] = ("time", 60 * _ureg["min"][1])
_ureg["day"] = _ureg["days"] = ("time", _ureg["hour"][1] * 24)
_ureg["yr"] = _ureg["year"] = _ureg["years"] = ("time", _ureg["day"][1] * 365.242)

_ureg["hours_per_week"] = ("time_rate", 1.0)

_default_units = {
    "metric": {
        "length": "cm",
        "weight": "kg",
        "angle": "deg",
        "time": "yr",
        "time_rate": "hours_per_week",
    },
    "united_states": {
        "length": "in",
        "weight": "lb",
        "angle": "deg",
        "time": "yr",
        "time_rate": "hours_per_week",
    },
}


def units_class(units):
    """
    Returns 'length', 'weight', 'angle', 'time', or 'time_rate'.

        >>> units_class('cm')
        'length'

    """
    if units is None or units == "":
        return None
    return _ureg[units][0]


def units_in_class(uclass):
    """
    Return a list of all units in uclass, where uclass is e.g.
    length', 'weight', 'angle, 'time', 'time_rate'.
    """
    return [key for key, (uclass_0, _) in _ureg.items() if uclass_0 == uclass]


def default_units(unit_system="metric", exceptions={}):
    """
    Get the default unit for a given unit system. unit_class is
    'length', 'weight', 'angle', or 'time'. unit_system is
    either 'metric' or 'united_states'.

    """
    result = dict()
    result.update(_default_units[unit_system])
    result.update(exceptions)
    return result


def raw(units):
    """
    Returns a raw units conversion factor. Try not to use this.
    Use factor() or convert() instead.
    """
    return _ureg[units][1]


def factor(from_units, to_units, units_class=None):
    """
    Return a conversion factor:

        >>> value_in_cm = 25
        >>> value_in_cm * factor('cm', 'mm')
        250

    class: If specified, the class of the units must match the class provided.

    """
    if (from_units is None or not len(from_units)) and (
        to_units is None or not len(to_units)
    ):  # pylint: disable=len-as-condition
        return 1.0
    if from_units == to_units:
        return 1.0
    if _ureg[from_units][0] != _ureg[to_units][0]:
        raise ValueError(
            "Can't convert between apples and oranges (%s and %s)"
            % (from_units, to_units)
        )
    if units_class and _ureg[from_units][0] != units_class:
        raise ValueError(
            "Units class must be %s, but got %s" % (units_class, _ureg[from_units][0])
        )
    return _ureg[from_units][1] / _ureg[to_units][1]


def convert(value, from_units, to_units, units_class=None):
    """
    Convert a number from one unit to another.

    class: If specified, the class of the units must match the class provided.

    Returns a tuple with the converted value and the units.

        >>> value_cm = 25
        >>> value, units = convert(value_cm, 'cm', 'mm')
        >>> value
        250
        >>> units
        'mm'

    """
    # Get factor first so we return errors for apples and oranges,
    # even when value is None
    this_factor = factor(from_units, to_units, units_class=units_class)
    if value is None:
        return None, None
    return value * this_factor, to_units


def convert_list(a_list, from_units, to_units):
    """
    Convenience helper to convert a list of numbers from one unit to another.

    Unlike convert(), does not return a tuple.

        >>> convert_list([10, 20, 30], 'cm', 'mm')
        [100, 200, 300]

    """
    scale_factor = factor(from_units, to_units)
    return [scale_factor * x for x in a_list]


def convert_to_default(value, from_units, defaults):
    """
    Convert a number from the given unit to a default for
    the given unit system.

    Returns a tuple with the converted value and the units.

        >>> value_cm = 100
        >>> convert_to_default(value_cm, 'cm', {'length': 'in', 'weight': 'lb', 'angle': 'deg', 'time': 'yr'})
        (39.3701, 'in')

    """
    this_units_class = units_class(from_units)
    if this_units_class:
        to_units = defaults[this_units_class]
        return convert(value, from_units, to_units)
    else:
        return value, from_units


def convert_to_system_default(value, from_units, to_unit_system="metric"):
    """
    Convert a number from the given unit to a default for
    the given unit system.

    Returns a tuple with the converted value and the units.

        >>> value_cm = 100
        >>> convert_to_system_default(value_cm, 'cm', 'united_states')
        (39.3701, 'in')

    """
    return convert_to_default(value, from_units, default_units(to_unit_system))


def prettify(value, units, precision=None):
    """
    Take a value, and units, and return rounded values in the
    default metric and United States units.

    The default precision values vary per unit. Specifying an
    integer for `precision` will override those defaults.

        >>> prettify(182.13992, 'cm'),
        (182.0, 'cm', 71.75, 'in')
        >>> prettify(182.13992, 'cm', precision=1)
        (182.1, 'cm', 71.7, 'in')
        >>> prettify(182.13992, 'cm', precision=2)
        (182.14, 'cm', 71.71, 'in')

    """

    def round_to(value, nearest):
        """
        Round a number to the nearest specified increment.

        e.g.:

            >>> round_to(3.8721, 0.05)
            3.85
            >>> round_to(3.8721, 0.1)
            3.9
            >>> round_to(3.8725, 0.25)
            3.75
            >>> round_to(3.8725, 2.0)
            4

        Use reciprocal due to floating point weirdness:

            >>> value, nearest = 3.9, 0.1
            >>> round(value / nearest) * nearest
            3.9000000000000004
            >>> round(value / nearest) / (1.0 / nearest)
            3.9

        """
        reciprocal = 1.0 / nearest
        return round(value / nearest) / reciprocal

    def round_value(value, units):
        if precision is None:
            nearest = {"cm": 0.5, "in": 0.25, "kg": 0.5, "lb": 1.0, "yr": 1.0}.get(
                units, 0.1
            )
        else:
            # Work around weird floating point rounding issues
            nearest = 1.0 / 10 ** precision
        return round_to(value, nearest), units

    return round_value(*convert_to_system_default(value, units)) + round_value(
        *convert_to_system_default(value, units, "united_states")
    )


all_units = _ureg.keys()
all_units_classes = list(set([item[0] for item in _ureg.values()]))
lengths = units_in_class("length")
weights = units_in_class("weight")
angles = units_in_class("angle")
times = units_in_class("time")
time_rates = units_in_class("time_rate")
