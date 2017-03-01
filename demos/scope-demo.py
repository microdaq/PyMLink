# Scope demo
# visit site www.microdaq.org
# author Witczenko
# email witczenko@gmail.com

from py_mlink import PyMLink
try:
    import pyqtgraph as pg
except ImportError:
    print 'To run this demo you have to install pyqtgraph and (PyQt4/5 or PySide).'

DATA_COUNT = 500
SAMPLE_RATE_HZ = 10000
DURATION_SEC = 60
CHANNEL = 1

# Create MLink object, connect to MicroDAQ device
pml = PyMLink.MLink('10.10.1.1')

# Init analog input scan
pml.ai_scan_init(CHANNEL, SAMPLE_RATE_HZ, DURATION_SEC, PyMLink.AIRange.AI_5V)

# Create plot with pyqtgraph
win = pg.GraphicsWindow(title='Scope demo')
win.resize(800, 600)
p = win.addPlot()

x = [i for i in range(0, DATA_COUNT)]
y = [0 for i in range(0, DATA_COUNT)]
plot = p.plot(x, y, pen="r")

print 'Acquiring data...'
for i in range((DURATION_SEC*SAMPLE_RATE_HZ)/DATA_COUNT):
    data = pml.ai_scan(DATA_COUNT, True)
    plot.setData(x, data[0])
    pg.QtGui.QApplication.processEvents()

win.close()
print 'done.'


