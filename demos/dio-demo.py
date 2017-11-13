# Digital I/O demo
# visit site www.microdaq.org
# Embedded-solutions, November 2017

from py_mlink import PyMLink

# Create MLink object, connect to MicroDAQ device
mdaq = PyMLink.MLink('10.10.1.2')

# Configure Digital I/O, disable all functions: encoder, pwm, uart
for i in range(1, 7):
    mdaq.dio_func(i, False)

# Choose channels to be digital input
DI = [1, 2, 3, 4, 5, 6, 7, 8]

# Choose channels to be digital output
DO = [9, 10, 11, 12, 13, 14, 15, 16]
DO_state = [True for state in range(8)]

# Read DI states
di_state = mdaq.dio_read(DI)
# Set DO states
mdaq.dio_write(DO, DO_state)

# Print data
for i, di in enumerate(di_state):
    print 'DI[%d]: %d' % (i, di)

