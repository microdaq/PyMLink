# Scope FFT demo
# visit site www.microdaq.org
# Embedded-solutions, November 2017-2019

import numpy as np
import pyqtgraph as pg

from py_mlink import PyMLink

# Params
DATA_COUNT = 10000
SAMPLE_RATE_HZ = 100000
DURATION_SEC = 60
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
p_fft_handle = p_fft.plot(xf, np.zeros(int(DATA_COUNT/2)), pen="r")
p_data_handle = p_data.plot(xd, np.zeros(DATA_COUNT), pen="g")


# Create MLink object, connect to MicroDAQ device
mdaq = PyMLink.MLink('10.10.1.1')

# Init analog input scan
mdaq.ai_scan_init(
    CHANNEL, PyMLink.AIRange.AI_5V,
    False, SAMPLE_RATE_HZ, DURATION_SEC)

print('Acquiring data...')
for i in range(int((DURATION_SEC*SAMPLE_RATE_HZ)/DATA_COUNT)):

    # Get AI data
    data = mdaq.ai_scan(DATA_COUNT, -1)

    # Calc FFT and draw plots
    data = data - np.mean(data)
    y = np.array(abs(np.fft.fft(data)/DATA_COUNT))
    y = y[0:int(DATA_COUNT/2)]*2.0
    p_fft_handle.setData(xf, y)
    p_data_handle.setData(xd, data)

    pg.QtGui.QApplication.processEvents()

win.close()
print('done.')


