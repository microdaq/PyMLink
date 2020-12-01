# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import microdaq

mdaq = microdaq.Device("10.10.1.1")

# disable UART function for DIO9 to allow dio_write() operation
mdaq.dio_func(6, False)

# set digital output state to 1
mdaq.dio_write(9, True)

# enable DIO9 alternative function (UART)
mdaq.dio_func(6, True)
