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
    return mdaq.get_str_hw_info() 

@pytest.fixture
def hwid_tuple(mdaq):
    return mdaq.get_hw_info() 


@pytest.fixture
def mdaq(ip, request, mock):
    """Resturns MLink class instance with established connection.
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
def skipif_adc(request, hwid_tuple):
    marker = request.node.get_closest_marker('skipif_adc')

    _, adc, _, _, _ = hwid_tuple    
    if marker and adc in marker.args[0]:
        pytest.skip(
            f'Test is not designed for given MicroDAQ ADC: {adc}')


def pytest_configure(config):
    config.addinivalue_line(
        "markers", 
        "skipif_hwid(hwid): Marker for skipping test for specified MicroDAQs hardware ID"
    )

    config.addinivalue_line(
        "markers", 
        "skipif_adc(adc_list): Marker for skipping test for specified MicroDAQs ADCs"
    )
