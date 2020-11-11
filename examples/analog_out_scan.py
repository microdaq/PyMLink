# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import time

import microdaq

mdaq = microdaq.Device("10.10.1.1")
channels = [1, 2]

mdaq.ao_scan_init([1, 2], [[1, 2, 3], [1.5, 2.5, 3.5]], [0, 5], False, 100, -1)
mdaq.ao_scan()
time.sleep(1)

mdaq.ao_scan_data([1, 2], [[-1, -2, -3], [-4, -5, -6]], True)
time.sleep(1)

mdaq.ao_scan_stop()
