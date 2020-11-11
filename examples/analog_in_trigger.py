# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import os

import microdaq

mdaq = microdaq.Device("10.10.1.1")
mdaq.ai_scan_init([1, 2], [-10, 10], False, 1000, 1)
mdaq.ai_scan_trigger_dio(6, 1)
mdaq.ai_scan_trigger_dio_pattern("xxxxx1xx")
mdaq.ai_scan_trigger_clear()
mdaq.ai_scan_trigger_ext_start(microdaq.Triggers.DSP_START)

try:
    data = mdaq.ai_scan(10, 2)
    print(data)
except microdaq.MLinkError as error:
    print("Error: %s" % error)

mdaq.dsp_init(os.path.join("model", "signal-model.out"), 100, -1)
mdaq.dsp_start()

data = mdaq.ai_scan(10, 2)
print(data)
