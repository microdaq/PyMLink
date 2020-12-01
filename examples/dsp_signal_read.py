# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import os

import microdaq

mdaq = microdaq.Device("10.10.1.1")
mdaq.dsp_init(os.path.join("resources", "signal-model.out"), 10, -1)
mdaq.dsp_start()

print(mdaq.dsp_signal_read(1, 1, 10))
print(mdaq.dsp_signal_read(2, 1, 10))
print(mdaq.dsp_signal_read(3, 1, 10))

mdaq.dsp_stop()
