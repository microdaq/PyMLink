# LED demo
# visit site www.microdaq.org
# Embedded-solutions, November 2017-2019

import time

from py_mlink import PyMLink

# Create MLink object, connect to MicroDAQ device
mdaq = PyMLink.MLink('10.10.1.1')

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


