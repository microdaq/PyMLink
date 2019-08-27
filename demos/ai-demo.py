# Analog input demo
# visit site www.microdaq.org
# Embedded-solutions, November 2017-2019

from py_mlink import PyMLink

# Create MLink object, connect to MicroDAQ device
mdaq = PyMLink.MLink('10.10.1.1')

# Read data from channels 1..4, input range from -10V to 10V, single ended
data = mdaq.ai_read([1, 2, 3, 4], [-10, 10], False)

# Print data
for i, volt in enumerate(data):
    print('Channel[%d]: %f V' % (i, volt))



