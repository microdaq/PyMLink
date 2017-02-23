# Analog inputs demo
# visit site www.microdaq.org
# author Witczenko
# email witczenko@gmail.com

from py_mlink import PyMLink

try:
    # Create MLink object, connect to MicroDAQ device
    pml = PyMLink.MLink('10.10.1.1')

    # Choose channels to read eg. 1..8
    channels = [ch for ch in range(1, 9)]

    # Read data
    data = pml.ai_read(channels)

    # Print data
    i = 0
    for ch in channels:
        print 'Channel[%d]: %f V' % (ch, data[i])
        i += 1

except PyMLink.MLinkError, errval:
    print "Error:", errval

