# Analog output demo
# visit site www.microdaq.org
# Embedded-solutions, November 2017

from py_mlink import PyMLink

# Create MLink object, connect to MicroDAQ device
mdaq = PyMLink.MLink('10.10.1.1')

# Choose channels to write eg. 1..4
ch = [1, 2, 3, 4]
# Set values
ch_voltage = [0.5, 1, 1.5, 2]

# Set analog outputs, output range from 0V to 5V
mdaq.ao_write(ch, [0, 5], ch_voltage)


