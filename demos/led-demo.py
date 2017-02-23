# LED demo
# visit site www.microdaq.org
# author Witczenko
# email witczenko@gmail.com

from py_mlink import PyMLink
import time

try:
    # Create MLink object, connect to MicroDAQ device
    pml = PyMLink.MLink('10.10.1.1')

    # turn on LED 1
    pml.led_write(1, True)
    # turn on LED 2
    pml.led_write(2, True)

    # wait a second
    time.sleep(1.0)

    # turn off LED 1
    pml.led_write(1, False)
    # turn off LED 2
    pml.led_write(2, False)

except PyMLink.MLinkError, errval:
    print "Error:", errval

