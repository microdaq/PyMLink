# Utils demo
# visit site www.microdaq.org
# Embedded-solutions, November 2017-2019

from py_mlink import PyMLink

# Print documentation e.g:
print(PyMLink.MLink.__doc__)
print(PyMLink.MLink.ai_scan_init.__doc__)

# Connect to MicroDAQ device without worrying about
# connection timeout (maintain_connection=True)
# this option has slightly less performance
mdaq = PyMLink.MLink('10.10.1.1', maintain_connection=True)

# Print model name of connected MicroDAQ device
mdaq.hw_info()

# Catch MLink errors
try:
    mdaq.ai_read(99, [-10, 10], False)
except PyMLink.MLinkError as errval:
    print("Error:", errval)

    # Close connection
    mdaq.disconnect()

