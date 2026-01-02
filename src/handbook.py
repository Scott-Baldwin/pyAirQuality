import math

# Adapted from the 2019 ASHRAE Handbook - HVAC Applications:
# Chapter 46: Building Air Intake and Exhaust Design
# Section 3: EXHAUST-TO-INTAKE DILUTION OR CONCENTRATION CALCULATIONS


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
    return (i_z**2 * x**2 + sigma_o**2) ** (1 / 2)


def get_turbulence(z, z_o):
    # eqn. 21
    n = 0.24 + math.log10(z_o) + 0.016 * (math.log10(z_o) ** 2)
    i_x = n * math.log(30 / z_o) / math.log(z / z_o)
    i_y = 0.75 * i_x
    i_z = 0.5 * i_x
    return (i_y, i_z)


# TODO: add plume-rise calcs to get zeta


# %% test
def main():
    z = 10
    z_o = 0.5

    x = 30
    d_e = 1

    U_h = 10
    V_e = 2.5
    zeta = 2

    i_y, i_z = get_turbulence(z, z_o)

    sigma_o = 0.35 * d_e
    sigma_y = get_sigma_y(x, i_y, sigma_o)
    sigma_z = get_sigma_y(x, i_z, sigma_o)

    print(get_dilution(U_h, sigma_y, sigma_z, V_e, d_e, zeta))


# %%
if __name__ == "__main__":
    main()
