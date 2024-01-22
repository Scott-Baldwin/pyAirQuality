# %%
import sys, unittest

sys.path.append("src")


# %%
from pyAirQuality import example


class TestExample(unittest.TestCase):
    def test_test(self):
        self.assertEqual("!", example.test())

    def test_error(self):
        self.assertRaises(ValueError, example.error)


# %%
from pyAirQuality import ashrae


class TestASHRAE(unittest.TestCase):
    def test_separation(self):
        self.assertIsNone(ashrae.separation_distance())

    def test_handbook(self):
        self.assertIsNone(ashrae.handbook_dilution())


# %%
if __name__ == "__main__":
    unittest.main()
