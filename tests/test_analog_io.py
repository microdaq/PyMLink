# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import pytest


def compare_value_with_tolerance(values_to_compare, expected_values, tolerance):
    """Compares to sets of values with given tolerance.

    :param values_to_compare: list of input values 
    :param expected_values: list of reference values to compare with
    values_to_compare
    :param tolerance: maximum difference beetween values_to_compare and
    expected_values
    :return: True when all values fit with given tolerance,
    otherwise returns False
    """
    assert len(values_to_compare) == len(expected_values)

    diffs = map(lambda val, expected: abs(val-expected), values_to_compare, expected_values)
    above_tolerance = list(filter(lambda val: val > tolerance, diffs))

    return not bool(above_tolerance) 


def test_read_ai_1_to_8_channels(mdaq, tolerance):
    expected_values = [0.0]*8
    channels = [1, 2, 3, 4, 5, 6, 7, 8]

    data = mdaq.ai_read(channels, [-10, 10])

    assert compare_value_with_tolerance(data, expected_values, tolerance)


@pytest.mark.skipif_adc([1, 2, 4, 6, 7, 10])
def test_read_ai_1_to_16_channels(mdaq, tolerance):
    expected_values = [0.0]*16
    channels = [ch_id for ch_id in range(1, 17)]

    data = mdaq.ai_read(channels, [-10, 10])

    assert compare_value_with_tolerance(data, expected_values, tolerance)


@pytest.mark.skipif_hwid('MicroDAQ E2000-ADC09-DAC06-12')
def test_not_for_given_configuration_for_whatever_reason():
    assert True