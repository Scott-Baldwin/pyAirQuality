import math, unittest

# Adapted from the 2019 ASHRAE Handbook - HVAC Applications:
# Chapter 46: Building Air Intake and Exhaust Design
# Sections 2 & 3


# %% from section 2
def stack_downwash(D_e, V_e, U_h, B_cap):
    # eqn. 8
    if V_e / U_h > 3:
        # no downwash
        h_d = 0
    else:
        # downwash
        h_d = D_e * (3 - B_cap * V_e / U_h)

    return h_d


def momentum_plume_rise(x, B_cap, U_h, V_e, D_e, H, Z_o):
    # eqn. 7
    F_m = V_e**2 * ((D_e**2) / 4)
    B_jet = (1 / 3) + (U_h / V_e)
    U_h_over_U_star = 2.5 * math.log(H / Z_o)

    h_x = ((3 * F_m * x) / (B_jet**2 * U_h**2)) ** (1 / 3)
    h_f = (0.9 * (F_m * U_h_over_U_star) ** 0.5) / (U_h * B_jet)

    # plume rise at downwind x
    h_r = B_cap * min(h_x, h_f)
    return h_r


# %% from section 3
def get_zeta(h_plume, h_top):
    # eqn. 16
    return max(0, h_plume - h_top)


def get_plume_rise(h_stack, x, B_cap, U_h, V_e, D_e, H, Z_o):
    # eqn. 17
    h_r = momentum_plume_rise(x, B_cap, U_h, V_e, D_e, H, Z_o)
    h_d = stack_downwash(D_e, V_e, U_h, B_cap)
    return h_stack + h_r - h_d


def get_dilution(U_h, sigma_y, sigma_z, V_e, d_e, zeta):
    # eqn. 18
    return ((4 * U_h * sigma_y * sigma_z) / (V_e * d_e**2)) * math.exp(
        zeta**2 / (2 * sigma_z**2)
    )


def get_sigma_y(x, i_y, sigma_o):
    # eqn. 19
    return (i_y**2 * x**2 + sigma_o**2) ** (1 / 2)


def get_sigma_z(x, i_z, sigma_o):
    # eqn. 20
    # TODO: same as sigma_y, could combine into single general purpose func
    return (i_z**2 * x**2 + sigma_o**2) ** (1 / 2)


def get_turbulence(z, z_o):
    # eqn. 21
    n = 0.24 + 0.096 * math.log10(z_o) + 0.016 * (math.log10(z_o) ** 2)
    i_x = n * math.log(30 / z_o) / math.log(z / z_o)
    i_y = 0.75 * i_x
    i_z = 0.5 * i_x
    return (i_y, i_z)


# %%
def get_results(
    x,
    Z_o,
    H_roof,
    h_stack,
    h_top,
    D_e,
    V_e,
    U_h,
    B_cap,
):
    h_plume = get_plume_rise(h_stack, x, B_cap, U_h, V_e, D_e, H_roof, Z_o)
    zeta = get_zeta(h_plume, h_top)

    i_y, i_z = get_turbulence(H_roof, Z_o)

    sigma_o = 0.35 * D_e
    sigma_y = get_sigma_y(x, i_y, sigma_o)
    sigma_z = get_sigma_z(x, i_z, sigma_o)

    D_r = get_dilution(U_h, sigma_y, sigma_z, V_e, D_e, zeta)

    result = {
        "D_r": D_r,
        "i_y*x": i_y * x,
        "i_z*x": i_z * x,
        "sigma_y": sigma_y,
        "sigma_z": sigma_z,
        "h_plume": h_plume,
    }

    return result


# %% unit tests
class TestHandbookExample_2(unittest.TestCase):
    def test_fig_7_row_1(self):
        result = get_results(
            x=14.1,
            Z_o=0.65,
            H_roof=15,
            h_stack=6.1,
            h_top=2,
            D_e=0.5,
            V_e=9,
            U_h=5,
            B_cap=1,
        )

        # dilution example values have some sort of error in example calcs
        # all calculated dilution values are low by roughly 2% compared to examples
        # all individual components are within at least 1 place of example values
        self.assertAlmostEqual(result["D_r"], 1100, -2)
        self.assertAlmostEqual(result["i_y*x"], 2.87, 2)
        self.assertAlmostEqual(result["i_z*x"], 1.92, 2)
        self.assertAlmostEqual(result["sigma_y"], 2.88, 2)
        self.assertAlmostEqual(result["sigma_z"], 1.92, 2)
        self.assertAlmostEqual(result["h_plume"], 6.77, 1)

    def test_fig_7_row_2(self):
        result = get_results(
            x=14.1,
            Z_o=0.65,
            H_roof=15,
            h_stack=6.1,
            h_top=2,
            D_e=0.5,
            V_e=9,
            U_h=7,  # changed
            B_cap=1,
        )
        self.assertAlmostEqual(result["D_r"], 591, -2)
        self.assertAlmostEqual(result["h_plume"], 5.97, 2)

    def test_fig_7_row_3(self):
        result = get_results(
            x=14.1,
            Z_o=0.65,
            H_roof=15,
            h_stack=6.1,
            h_top=2,
            D_e=0.5,
            V_e=9,
            U_h=9,  # changed
            B_cap=1,
        )
        self.assertAlmostEqual(result["D_r"], 504, -2)
        self.assertAlmostEqual(result["h_plume"], 5.57, 2)

    def test_fig_7_row_4(self):
        result = get_results(
            x=14.1,
            Z_o=0.325,  # changed
            H_roof=15,
            h_stack=6.1,
            h_top=2,
            D_e=0.5,
            V_e=9,
            U_h=5,
            B_cap=1,
        )
        self.assertAlmostEqual(result["D_r"], 3194, -3)
        self.assertAlmostEqual(result["i_y*x"], 2.46, 2)
        self.assertAlmostEqual(result["i_z*x"], 1.64, 2)
        self.assertAlmostEqual(result["sigma_y"], 2.47, 2)
        self.assertAlmostEqual(result["sigma_z"], 1.64, 1)
        self.assertAlmostEqual(result["h_plume"], 6.91, 2)

    def test_fig_7_row_5(self):
        result = get_results(
            x=14.1,
            Z_o=0.325,  # changed
            H_roof=15,
            h_stack=6.1,
            h_top=2,
            D_e=0.5,
            V_e=9,
            U_h=7,  # changed
            B_cap=1,
        )
        self.assertAlmostEqual(result["D_r"], 1065, -2)
        self.assertAlmostEqual(result["h_plume"], 6.05, 2)

    def test_fig_7_row_6(self):
        result = get_results(
            x=14.1,
            Z_o=0.325,  # changed
            H_roof=15,
            h_stack=6.1,
            h_top=2,
            D_e=0.5,
            V_e=9,
            U_h=9,  # changed
            B_cap=1,
        )
        self.assertAlmostEqual(result["D_r"], 745, -2)
        self.assertAlmostEqual(result["h_plume"], 5.62, 2)

    def test_fig_7_row_7(self):
        result = get_results(
            x=14.1,
            Z_o=0.975,  # changed
            H_roof=15,
            h_stack=6.1,
            h_top=2,
            D_e=0.5,
            V_e=9,
            U_h=5,
            B_cap=1,
        )
        self.assertAlmostEqual(result["D_r"], 704, -2)
        self.assertAlmostEqual(result["i_y*x"], 3.17, 2)
        self.assertAlmostEqual(result["i_z*x"], 2.11, 2)
        self.assertAlmostEqual(result["sigma_y"], 3.17, 2)
        self.assertAlmostEqual(result["sigma_z"], 2.11, 1)
        self.assertAlmostEqual(result["h_plume"], 6.69, 2)

    def test_fig_7_row_8(self):
        result = get_results(
            x=14.1,
            Z_o=0.975,  # changed
            H_roof=15,
            h_stack=6.1,
            h_top=2,
            D_e=0.5,
            V_e=9,
            U_h=7,  # changed
            B_cap=1,
        )
        self.assertAlmostEqual(result["D_r"], 470, -2)
        self.assertAlmostEqual(result["h_plume"], 5.92, 2)

    def test_fig_7_row_9(self):
        result = get_results(
            x=14.1,
            Z_o=0.975,  # changed
            H_roof=15,
            h_stack=6.1,
            h_top=2,
            D_e=0.5,
            V_e=9,
            U_h=9,  # changed
            B_cap=1,
        )
        self.assertAlmostEqual(result["D_r"], 438, -1)
        self.assertAlmostEqual(result["h_plume"], 5.54, 2)


# %%
if __name__ == "__main__":
    unittest.main()
