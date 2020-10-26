# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import pytest


def test_invalid_connection(mdaq_cls):
    with pytest.raises(mdaq_cls.MLinkError):
        mdaq = mdaq_cls.MLink("999.999.999.999")
        mdaq.disconnect()


def test_valid_connection(mdaq_cls, ip):
    mdaq = mdaq_cls.MLink(ip)
    mdaq.disconnect()
