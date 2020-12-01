# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import time

import microdaq

mdaq = microdaq.Device("10.10.1.1")
for i in range(50):
    time.sleep(0.1)
    print("KEY1/KEY2: %d/%d" % (mdaq.func_key_read(1), mdaq.func_key_read(2)))
