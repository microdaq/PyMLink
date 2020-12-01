# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org


import os
import time

import microdaq

mdaq = microdaq.Device("10.10.1.1")
mdaq.dsp_init(os.path.join("resources", "signal-model.out"), 10, 2)
mdaq.dsp_mem_write(1, [1, 2, 3, 4])
mdaq.dsp_start()

for i in range(0, 20):
    print(mdaq.dsp_signal_read(4, 4, 1))
    mdaq.dsp_mem_write(1, [2 + i, 3 + i, 4 + i, 5 + i])
    time.sleep(0.1)

mdaq.dsp_stop()
