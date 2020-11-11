# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import time
import microdaq

mdaq = microdaq.Device("10.10.1.1")
mdaq.enc_init(1, 0)

for i in range(30):
    time.sleep(0.1)
    enc = mdaq.enc_read(1)
    print("position: %d\tdir: %d" % (enc[0], enc[1]))
