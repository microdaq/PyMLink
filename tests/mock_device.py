# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

"""Mocked class for microdaq.Device"""

import ctypes
import microdaq


class Device(microdaq.Device):
    """Mocked implementation of the microdaq.Device class. It suppresses only
    MLinkError exceptions in order to validate Python wrapper only.

    The assumption is, whenever MLinkError exception appear that means we passed
    through API without any major problems and we properly called function from
    MLink sharded library.

    It doesn't require connected MicroDAQ device.
    """

    def __init__(self, ip, maintain_connection=False):
        _ = ip
        self._connectionless = maintain_connection
        self._linkfd = ctypes.c_int32()
        self._ip = "0.0.0.0"
        self._connectionless = False
        self._ao_scan_ch = 0
        self._mdaq_hwid = 0
        self._ai_scan_channels = None
        self._mdaq_hwid = (0, 0, 0, 0, 0)

    def _raise_exception(self, res):
        pass
