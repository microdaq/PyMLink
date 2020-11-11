# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2017-2020, www.microdaq.org

import microdaq

# connect to MicroDAQ device
mdaq = microdaq.Device('10.10.1.1')

# configure Digital I/O, disable all functions: encoder, PWM, UART
for i in range(1, 7):
    mdaq.dio_func(i, False)

# set DIO bank 1 (DIO 1..8) to input mode
mdaq.dio_dir(1, False)

# set DIO bank 2 (DIO 9..16) to output mode
mdaq.dio_dir(2, True)

# choose channels to read
DI = [1, 2, 3, 4, 5, 6, 7, 8]

# choose channels to write
DO = [9, 10, 11, 12, 13, 14, 15, 16]
DO_state = [True for state in range(8)]

# read DI states
di_state = mdaq.dio_read(DI)
# set DO states
mdaq.dio_write(DO, DO_state)

# print data
for i, di in enumerate(di_state):
    print('DI[%d]: %d' % (i, di))
