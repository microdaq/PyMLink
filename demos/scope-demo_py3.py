# Scope demo
# visit site www.microdaq.org
# Embedded-solutions, November 2017-2019

import pyqtgraph as pg

from py_mlink import PyMLink

DATA_COUNT = 5000
SAMPLE_RATE_HZ = 100000
DURATION_SEC = 60
CHANNEL = 1

# Create MLink object, connect to MicroDAQ device
mdaq = PyMLink.MLink('10.10.1.1')

# Init analog input scan
mdaq.ai_scan_init(
    CHANNEL, PyMLink.AIRange.AI_5V,
    False, SAMPLE_RATE_HZ, DURATION_SEC)

# Create plot with pyqtgraph
win = pg.GraphicsWindow(title='Scope demo')
win.resize(800, 600)
p = win.addPlot()

x = [i for i in range(0, DATA_COUNT)]
y = [0 for i in range(0, DATA_COUNT)]
plot = p.plot(x, y, pen="r")

print('Acquiring data...')
for i in range(int((DURATION_SEC*SAMPLE_RATE_HZ)/DATA_COUNT)):
    data = mdaq.ai_scan(DATA_COUNT, -1)
    plot.setData(x, data)
    pg.QtGui.QApplication.processEvents()

win.close()
print('done.')

