# Analog outputs demo
# visit site www.microdaq.org
# author Witczenko
# email witczenko@gmail.com

from py_mlink import PyMLink

try:
    # Create MLink object, connect to MicroDAQ device
    pml = PyMLink.MLink('10.10.1.1')

    # Choose channels to write eg. 1..4
    channels = [ch for ch in range(1, 5)]
    # Set values
    channels_voltage = [0.5, 1, 1.5, 2]

    # Set analog outputs
    pml.ao_write(channels, channels_voltage)

except PyMLink.MLinkError, errval:
    print "Error:", errval

