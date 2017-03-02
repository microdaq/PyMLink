# Scope FFT  - demo
# visit site www.microdaq.org
# author Witczenko
# email witczenko@gmail.com

from py_mlink import PyMLink
import numpy.fft as npfft
import numpy as np

try:
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtCore
except ImportError:
    print 'To run this demo you have to install pyqtgraph and (PyQt4/5 or PySide).'

# to suppress "Qpicture: invalid format version 0" warning
QtCore.qInstallMsgHandler(lambda *args: None)

# Params
DATA_COUNT = 500
SAMPLE_RATE_HZ = 10000
DURATION_SEC = 60*5
CHANNEL = 1

# Create plot with pyqtgraph
win = pg.GraphicsWindow(title='Scope FFT - demo')
win.resize(800, 600)

p_data = win.addPlot(row=1, col=1, title='ANALOG INPUT (CHANNEL 1)')
p_data.addItem(pg.GridItem())
p_data.setLabel(axis='left', units='V')

p_fft = win.addPlot(row=2, col=1, title='FFT (CHANNEL 1)')
p_fft.addItem(pg.GridItem())
p_fft.setLabel(axis='bottom', units='Hz')

xf = np.arange(DATA_COUNT/2)*(SAMPLE_RATE_HZ / DATA_COUNT)
xd = np.arange(DATA_COUNT)
p_fft_handle = p_fft.plot(xf, np.zeros(DATA_COUNT/2), pen="r")
p_data_handle = p_data.plot(xd, np.zeros(DATA_COUNT), pen="g")


# Create MLink object, connect to MicroDAQ device
pml = PyMLink.MLink('10.10.1.1', connectionless=False)
# Init analog input scan
pml.ai_scan_init(CHANNEL, SAMPLE_RATE_HZ, DURATION_SEC, PyMLink.AIRange.AI_5V)

print 'Acquiring data...'
for i in range((DURATION_SEC*SAMPLE_RATE_HZ)/DATA_COUNT):
    # Get AI data
    data = pml.ai_scan(DATA_COUNT, True)

    # Calc FFT and draw plots
    y = np.array(abs(npfft.fft(data[0])/DATA_COUNT))
    y = y[0:(DATA_COUNT/2)]*2.0
    p_fft_handle.setData(xf, y)
    p_data_handle.setData(xd, data[0])

    pg.QtGui.QApplication.processEvents()

win.close()
print 'done.'


