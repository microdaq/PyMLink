# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import ctypes
import microdaq


class Device(microdaq.Device):
    def __init__(self, ip):
        self._linkfd = ctypes.c_int32()
        self._ip = "0.0.0.0"
        self._connectionless = False
        self._ao_scan_ch = 0
        self._mdaq_hwid = 0
        self._ai_scan_channels = None
        self._mdaq_hwid = (0, 0, 0, 0, 0)

    def _raise_exception(self, res):
        ...
