# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import microdaq

mdaq = microdaq.Device("10.10.1.1")
for i in range(1, 7):
    mdaq.dio_func(i, False)

for i in range(1, 9):
    print("DI %d: %d" % (i, mdaq.dio_read(i)))

for i in range(9, 17):
    mdaq.dio_write(i, True)
