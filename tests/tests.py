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
from pyAirQuality import ashrae_handbook, separation_method


class TestASHRAE(unittest.TestCase):
    def test_separation(self):
        self.assertAlmostEqual(157.9, separation_method.get_dilution(), 1)

    def test_handbook(self):
        self.assertAlmostEqual(
            6.6,
            ashrae_handbook.get_dilution(
                U_h=1,
                sigma_y=1,
                sigma_z=1,
                V_e=1,
                d_e=1,
                zeta=1,
            ),
            1,
        )


# %%
if __name__ == "__main__":
    unittest.main()
