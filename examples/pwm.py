# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2017-2020, www.microdaq.org

import microdaq

mdaq = microdaq.Device(ip="10.10.1.1")
mdaq.pwm_init(module=1, period=1000)
mdaq.pwm_write(module=1, duty_a=10, duty_b=50)
