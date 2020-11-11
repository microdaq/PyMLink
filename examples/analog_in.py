# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2017-2020, www.microdaq.org

import microdaq

# connect to MicroDAQ device
mdaq = microdaq.Device("10.10.1.1")

# read data from channels 1..4, input range from -10V to 10V, single ended
data = mdaq.ai_read([1, 2, 3, 4], [-10, 10], False)

# print data
for i, volt in enumerate(data):
    print("Channel[%d]: %f V" % (i, volt))
