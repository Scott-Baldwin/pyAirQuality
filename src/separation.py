import unittest


# %% WIP NEEDS WORK
def get_dilution():
    """
    Adapted from ASHRAE Research Project Report 1635-RP:
    Simplified Procedure For Calculating Exhaust/Intake
    Separation Distances
    """
    # THIS IS ALL BS
    distance = 25  # ft
    flow_rate = 10000  # cfm
    exit_velocity = 3000  # fpm
    d = ((11.1 * distance) / (exit_velocity**0.5) + (exit_velocity / 400)) ** 2
    return d


# %% unit tests
class TestSeparation(unittest.TestCase):
    def test_1(self):
        self.assertAlmostEqual(157.9, get_dilution(), 1)

    # TODO: add more/better tests


# %%
if __name__ == "__main__":
    unittest.main()
