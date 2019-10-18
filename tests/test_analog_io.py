# MLink Python tests 
# www.microdaq.org
# Embedded-solutions 2019

import math
import pytest

from py_mlink import PyMLink 


def compare_value_with_tolerance(values_to_compare, expected_values, tolerance):
    """Compares to sets of values with given tolerance 

    :param values_to_compare: list of input values 
    :param expected_values: list of reference values to compare with values_to_compare
    :param tolerance: maximum difference beetween values_to_compare and expected_values
    :return: True when all values fit with given tolerance, otherwise returns False
    """
    assert len(values_to_compare) == len(expected_values)

    diffs = map(lambda val, expected: abs(val-expected), values_to_compare, expected_values)
    above_tolerance = list(filter(lambda val: val > tolerance, diffs))

    return not bool(above_tolerance) 


@pytest.mark.skip_hwid('MicroDAQ E2000-ADC09-DAC06-12')
def test_read_ai_1_to_8_channels(mdaq, tolerance, hwid):
    expected_values = [1.0]*8
    channels = [1, 2, 3, 4, 5, 6, 7, 8]

    data = mdaq.ai_read(channels, [-10, 10])

    assert compare_value_with_tolerance(data, expected_values, tolerance)


def test_read_ai_1_to_16_channels(mdaq, tolerance):
    expected_values = [1.0]*16
    channels = [ch_id for ch_id in range(1, 17)]

    data = mdaq.ai_read(channels, [-10, 10])

    assert compare_value_with_tolerance(data, expected_values, tolerance)