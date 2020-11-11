# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2017-2020, www.microdaq.org

import microdaq

# connect to MicroDAQ device
mdaq = microdaq.Device("10.10.1.1")

# choose channels to write eg. 1..4
ch = [1, 2, 3, 4]
# set values
ch_voltage = [0.5, 1, 1.5, 2]

# set analog outputs, output range from 0V to 5V
mdaq.ao_write(ch, [0, 5], ch_voltage)
