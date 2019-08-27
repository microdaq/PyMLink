# Analog output demo
# visit site www.microdaq.org
# Embedded Solutions 2019

import matplotlib.pyplot as plt
from time import sleep

from py_mlink import PyMLink
import pprint

# Create MLink object, connect to MicroDAQ device
mdaq = PyMLink.MLink('10.10.1.1')

mdaq.ai_scan_init([1], [-10, 10], False, 1000, 1)
mdaq.ai_scan_trigger_ext_start(PyMLink.Triggers.AO_SCAN_START)
data = mdaq.ai_scan(0, 2)
sleep(0.5)
# Generation
initial_data = [0, 1, 2, 3, 4]
mdaq.ao_scan_init([1], initial_data,[-10, 10], False, 100, 1)
mdaq.ao_scan()

data = mdaq.ai_scan(1000, 2)

plt.plot(data)
plt.show()
mdaq.disconnect()
