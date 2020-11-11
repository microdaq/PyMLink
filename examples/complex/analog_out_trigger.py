# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2019-2020, www.microdaq.org

import matplotlib.pyplot as plt
from time import sleep

import microdaq

# Connect to MicroDAQ device
mdaq = microdaq.Device('10.10.1.1')

mdaq.ai_scan_init([1], [-10, 10], False, 1000, 1)
mdaq.ai_scan_trigger_ext_start(microdaq.Triggers.AO_SCAN_START)
data = mdaq.ai_scan(0, 2)

sleep(0.5)

# Generation
initial_data = [0, 1, 2, 3, 4]
mdaq.ao_scan_init([1], initial_data, [-10, 10], False, 100, 1)
mdaq.ao_scan()

data = mdaq.ai_scan(1000, 2)

plt.plot(data)
plt.show()

mdaq.disconnect()
