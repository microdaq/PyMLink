# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import microdaq

# connect to MicroDAQ device
IP = "10.10.1.1"
mdaq = microdaq.Device(IP)

print("diconenct()")
mdaq.disconnect()

print("reconenct()")
mdaq.reconnect()

for i in range(2):
    print("diconenct()")
    mdaq.disconnect()
    print("connect()")
    mdaq.connect(IP)
