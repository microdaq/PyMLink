# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org


import pytest

import microdaq
import tests.mock_device


def pytest_addoption(parser):
    """Define additional options for test execution.

    usage example:
    pytest tests.py --ip=192.168.1.2 --tolerance=0.1 --mock
    """

    parser.addoption(
        "--ip",
        action="store",
        default="192.168.1.1",
        help="Set MicroDAQs IP (default: 192.168.1.1)",
    )


@pytest.fixture
def ip(request):
    return request.config.getoption("--ip")


@pytest.fixture
def mdaq(ip, mock, mock_mdaq):
    """Return MLink class instance with established connection.
    """

    return microdaq.Device(ip)


@pytest.fixture
def mdaq_cls():
    """Return MLink class or mocked MLink class.

    NOTE: Returned object depends on --mock parameter.
    """

    return tests.mock_device.Device


@pytest.fixture
def mock_mdaq(ip):
    """Return mocked Device."""

    return tests.mock_device.Device(ip)


@pytest.fixture
def mock_mdaq_cls(ip):
    """Return mocked Device class."""

    return tests.mock_device.Device
