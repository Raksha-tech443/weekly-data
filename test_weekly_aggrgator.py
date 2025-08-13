import unittest
from weekly_aggregator import aggregate_weekly

class TestWeeklyAggregator(unittest.TestCase):
    def test_basic_sum(self):
        data = {
            "2025-08-11": 10,  # Monday
            "2025-08-12": 20,
            "2025-08-17": 30,  # Sunday
        }
        out = aggregate_weekly(data)
        # Monday of that week is 2025-08-11
        self.assertEqual(out, {"2025-08-11": 60})

    def test_multiple_weeks(self):
        data = {
            "2025-08-11": 10,  # Mon
            "2025-08-17": 30,  # Sun
            "2025-08-18": 5,   # Next Mon (new week)
        }
        out = aggregate_weekly(data)
        self.assertEqual(out, {"2025-08-11": 40, "2025-08-18": 5})

    def test_validation(self):
        with self.assertRaises(ValueError):
            aggregate_weekly({})  # empty

        with self.assertRaises(ValueError):
            aggregate_weekly({"2025/08/11": 1})  # bad date

        with self.assertRaises(ValueError):
            aggregate_weekly({"1969-12-31": 1})  # out of range

        with self.assertRaises(ValueError):
            aggregate_weekly({"2025-08-11": 1_000_001})  # out of range value

        # missing Sunday
        with self.assertRaises(ValueError):
            aggregate_weekly({"2025-08-11": 1})  # only Monday

if __name__ == "__main__":
    unittest.main()
