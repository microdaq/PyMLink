# MLink Python tests 
# www.microdaq.org
# Embedded-solutions 2019

import pytest


def test_invalid_connection(mdaq_cls):
    with pytest.raises(mdaq_cls.MLinkError):
        mdaq = mdaq_cls.MLink("999.999.999.999")
        mdaq.disconnect()


def test_valid_connection(mdaq_cls, ip):
    mdaq = mdaq_cls.MLink(ip)
    mdaq.disconnect()
