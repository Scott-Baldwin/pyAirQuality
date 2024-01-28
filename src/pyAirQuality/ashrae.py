def separation_dilution():
    """
    Adapted from ASHRAE Research Project Report 1635-RP:
    Simplified Procedure For Calculating Exhaust/Intake
    Separation Distances
    """
    distance = 25  # ft
    flow_rate = 10000  # cfm
    exit_velocity = 3000  # fpm
    d = ((11.1 * distance) / (exit_velocity**0.5) + (exit_velocity / 400)) ** 2
    return d


def handbook_dilution():
    """
    Adapted from the 2019 ASHRAE Handbook - HVAC Applications:
    Chapter 46: Building Air Intake and Exhaust Design
    """
    return None
