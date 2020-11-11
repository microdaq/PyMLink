# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2017-2020, www.microdaq.org

import time

import microdaq

# connect to MicroDAQ device
mdaq = microdaq.Device('10.10.1.1')

# turn on LED 1
mdaq.led_write(1, True)
# turn on LED 2
mdaq.led_write(2, True)

# wait a second
time.sleep(1.0)

# turn off LED 1
mdaq.led_write(1, False)
# turn off LED 2
mdaq.led_write(2, False)
