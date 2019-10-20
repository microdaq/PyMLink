# MLink Python tests 
# www.microdaq.org
# Embedded-solutions 2019

import pytest

from py_mlink import PyMLink as pml
import py_mlink_mock as pml_mock 


def pytest_addoption(parser):
    """Defines additional options for test execution
    
    usage example:
    pytest tests.py --ip=192.168.1.2 --tolerance=0.1 --mock
    """

    parser.addoption(
        "--ip",
        action="store",
        default="192.168.1.1",
        help="Set MicroDAQs IP (default: 192.168.1.1)",
    )

    parser.addoption(
        "--tolerance",
        action="store",
        default=0.0,
        help="Set float tolerance value for some tests (default: 0.0)",
    )

    parser.addoption(
        "--mock",
        action="store_true",
        help="Use mocked MLink class instance for running tests without MicroDAQ device",
    )


@pytest.fixture
def ip(request):
    return request.config.getoption("--ip") 


@pytest.fixture
def mock(request):
    return request.config.getoption("--mock") 


@pytest.fixture
def tolerance(request):
    return float(request.config.getoption("--tolerance"))


@pytest.fixture
def hwid(mdaq):
    """Returns MicroDAQ hardware configuration in a string format.
    example:
    'MicroDAQ E2000-ADC09-DAC06-12'
    """

    return mdaq.get_str_hw_info() 


@pytest.fixture
def hwid_tuple(mdaq):
    """Returns tuple with MicroDAQ hardware configuration.

    :return: (serie, adc, dac, cpu, mem)
    """

    return mdaq.get_hw_info() 


@pytest.fixture
def adc_id(hwid_tuple):
    """Returns ID of Analog to Digital Converter 
    from MicroDAQ configuration.
    """

    return hwid_tuple[1]


@pytest.fixture
def dac_id(hwid_tuple):
    """Returns ID of Digital to Analog Converter 
    from MicroDAQ configuration.
    """

    return hwid_tuple[2]


@pytest.fixture
def dio_count(adc_id, dac_id):
    """Returns count of available digital I/O."""
    count = 32 if adc_id == 1 and dac_id == 1 else 16
    return count


@pytest.fixture
def mdaq(ip, request, mock):
    """Returns MLink class instance with established connection.
    """

    if mock:
        mdaq = pml_mock.MLink(ip)
        yield mdaq
    else:
        mdaq = pml.MLink(ip)
        yield mdaq
        mdaq.disconnect()


@pytest.fixture
def mdaq_cls():
    """Returns MLink class or mocked MLink class.
    Returned object depends on --mock paramter. 
    """

    if mock:
        return pml_mock
    else:
        return pml


@pytest.fixture(autouse=True)
def skipif_hwid(request, hwid):
    marker = request.node.get_closest_marker('skipif_hwid')
    if marker and marker.args[0] == hwid:
        pytest.skip(
            f'Test is not designed for given MicroDAQ configuration: {hwid}')


@pytest.fixture(autouse=True)
def skipif_adc(request, adc_id):
    marker = request.node.get_closest_marker('skipif_adc')
    if marker and adc_id in marker.args[0]:
        pytest.skip(
            f'Test is not designed for given MicroDAQ ADC {adc_id}')


def pytest_configure(config):
    config.addinivalue_line(
        "markers", 
        "skipif_hwid(hwid): Marker for skipping test for specified MicroDAQs hardware ID"
    )

    config.addinivalue_line(
        "markers", 
        "skipif_adc(adc_list): Marker for skipping test for specified MicroDAQs ADCs"
    )
