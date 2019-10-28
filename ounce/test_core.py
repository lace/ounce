import unittest
from . import core as ounce


class TestUnits(unittest.TestCase):
    def test_all_units(self):
        for x in ["in", "cm", "deg", "years"]:
            self.assertIn(x, ounce.all_units)
        for method in ["all_units", "factor", "convert"]:
            self.assertNotIn(method, ounce.all_units)

    def test_all_units_classes(self):
        self.assertEqual(
            set(ounce.all_units_classes),
            set(["length", "weight", "angle", "time", "time_rate"]),
        )

    def test_units_class(self):
        self.assertEqual(ounce.units_class("cm"), "length")
        self.assertEqual(ounce.units_class("stone"), "weight")
        self.assertEqual(ounce.units_class("rad"), "angle")
        self.assertEqual(ounce.units_class("sec"), "time")
        self.assertEqual(ounce.units_class(""), None)
        self.assertEqual(ounce.units_class(None), None)

    def test_units_in_class(self):
        self.assertIn("m", ounce.units_in_class("length"))

    def test_lengths(self):
        self.assertIn("m", ounce.lengths)

    def test_weights(self):
        self.assertIn("lb", ounce.weights)

    def test_angles(self):
        self.assertIn("degrees", ounce.angles)

    def test_times(self):
        self.assertIn("sec", ounce.times)

    def test_time_rates(self):
        self.assertIn("hours_per_week", ounce.time_rates)

    def test_default_units(self):
        self.assertEqual(
            ounce.default_units(),
            {
                "length": "cm",
                "weight": "kg",
                "angle": "deg",
                "time": "yr",
                "time_rate": "hours_per_week",
            },
        )

    def test_raw(self):
        self.assertEqual(ounce.raw("m"), 1.0)
        self.assertEqual(ounce.raw("mm"), 0.001)

    def test_factor(self):
        with self.assertRaisesRegexp(
            ValueError,
            r"Can\'t convert between apples and oranges \(stone and fathoms\)",
        ):
            ounce.factor("stone", "fathoms")

        nones = [(None, ""), ("", None), (None, None), ("", "")]
        for value in nones:
            self.assertEqual(ounce.factor(*value), 1.0)

        self.assertEqual(ounce.factor("in", "cm"), 2.54)
        self.assertAlmostEqual(ounce.factor("year", "min"), 525600, -3)
        self.assertEqual(ounce.factor("sec", "hr", units_class="time"), 1.0 / 3600)

        with self.assertRaisesRegexp(
            ValueError, r"Units class must be length, but got time"
        ):
            self.assertEqual(
                ounce.factor("sec", "hr", units_class="length"), 1.0 / 3600
            )

    def test_convert(self):
        import numpy as np

        self.assertEqual(ounce.convert(25, "cm", "mm")[0], 250)
        self.assertEqual(ounce.convert(180, "deg", "rad")[0], np.pi)
        self.assertAlmostEqual(ounce.convert(-10, "ft", "in")[0], -120)

        self.assertEqual(ounce.convert(25, "cm", "mm")[1], "mm")
        self.assertEqual(ounce.convert(180, "deg", "rad")[1], "rad")
        self.assertAlmostEqual(ounce.convert(-10, "ft", "in")[1], "in")

    def test_conversion_factors(self):
        import numpy as np

        self.assertAlmostEqual(ounce.convert(25, "cm", "m")[0], 0.25)
        self.assertAlmostEqual(ounce.convert(25, "cm", "cm")[0], 25)
        self.assertAlmostEqual(ounce.convert(25, "cm", "mm")[0], 250)
        self.assertAlmostEqual(
            ounce.convert(25, "cm", "in")[0], 9.8425197
        )  # from google
        self.assertAlmostEqual(ounce.convert(25, "cm", "ft")[0], 0.82021)  # from google
        self.assertAlmostEqual(
            ounce.convert(25, "cm", "fathoms")[0], 0.136701662
        )  # from google
        self.assertAlmostEqual(
            ounce.convert(25, "cm", "cubits")[0], 0.546806649
        )  # from google
        self.assertAlmostEqual(ounce.convert(10, "kg", "kg")[0], 10)
        self.assertAlmostEqual(ounce.convert(1, "kg", "g")[0], 1000)
        self.assertAlmostEqual(
            ounce.convert(10, "kg", "lbs")[0], 22.0462
        )  # from google
        self.assertAlmostEqual(
            ounce.convert(10, "kg", "stone")[0], 1.57473
        )  # from google
        self.assertAlmostEqual(ounce.convert(90, "deg", "rad")[0], np.pi / 2)
        self.assertAlmostEqual(ounce.convert(90, "deg", "deg")[0], 90)
        self.assertAlmostEqual(ounce.convert(30, "min", "sec")[0], 30 * 60)
        self.assertAlmostEqual(ounce.convert(30, "min", "minutes")[0], 30)
        self.assertAlmostEqual(ounce.convert(30, "min", "hours")[0], 0.5)
        self.assertAlmostEqual(ounce.convert(2, "days", "min")[0], 2 * 24 * 60)
        self.assertAlmostEqual(ounce.convert(1, "years", "min")[0], 525948.48)

    def test_convert_list(self):
        self.assertEqual(ounce.convert_list([10, 20, 30], "cm", "mm"), [100, 200, 300])

    def test_convert_to_system_default(self):
        self.assertEqual(ounce.convert_to_system_default(10, "mm"), (1, "cm"))

        result = (
            ounce.convert_to_system_default(10, "mm", "united_states"),
            (0.393701, "in"),
        )
        self.assertAlmostEqual(result[0][0], result[1][0], 6)
        self.assertEqual(result[0][1], result[1][1])

        result = (
            ounce.convert_to_system_default(10, "stone", "united_states"),
            (140, "lb"),
        )
        self.assertAlmostEqual(result[0][0], result[1][0], 0)
        self.assertEqual(result[0][1], result[1][1])

        self.assertEqual(ounce.convert_to_system_default(10, ""), (10, ""))

    def test_prettify(self):
        self.assertEqual(ounce.prettify(182.13992, "cm"), (182.0, "cm", 71.75, "in"))
        self.assertEqual(ounce.prettify(1821.3992, "mm"), (182.0, "cm", 71.75, "in"))
        self.assertEqual(ounce.prettify(-182.13992, "cm"), (-182.0, "cm", -71.75, "in"))
        self.assertEqual(
            ounce.prettify(182.13992, "cm", precision=2), (182.14, "cm", 71.71, "in")
        )
        self.assertEqual(
            ounce.prettify(182.13992, "cm", precision=4),
            (182.1399, "cm", 71.7086, "in"),
        )
