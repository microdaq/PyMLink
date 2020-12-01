# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import microdaq

mdaq = microdaq.Device("10.10.1.1")
channels = [1, 2]

mdaq.ao_scan_init([1, 2], [[3, 3], [4, 4]], [0, 5], True, 100, 5)
mdaq.ao_scan()

print("AO scan is done: %s" % mdaq.ao_scan_is_done())
for i in range(10):
    mdaq.ao_scan_data([1, 2], [[1, 1], [2, 2]], True)

print("AO scan wait until done")
mdaq.ao_scan_wait_until_done(-1)
mdaq.ao_scan_stop()
print("AO scan is done: %s" % mdaq.ao_scan_is_done())
