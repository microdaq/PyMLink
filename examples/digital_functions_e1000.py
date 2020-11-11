# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org


import microdaq

mdaq = microdaq.Device("10.10.1.1")
mdaq.dio_dir(1, 0)  # set bank 1 to input mode
mdaq.dio_dir(2, 0)  # set bank 2 to input mode
mdaq.dio_dir(3, 0)  # set bank 3 to input mode
mdaq.dio_dir(4, 0)  # set bank 4 to input mode

for i in range(1, 7):
    mdaq.dio_func(i, False)

for i in range(1, 33):
    print("DI %d: %d" % (i, mdaq.dio_read(i)))

mdaq.dio_dir(1, 1)  # set bank 1 to output mode
mdaq.dio_dir(2, 1)  # set bank 2 to output mode
mdaq.dio_dir(3, 1)  # set bank 3 to output mode
mdaq.dio_dir(4, 1)  # set bank 4 to output mode

print(mdaq.dio_write.__doc__)
for i in range(1, 33):
    mdaq.dio_write(i, True)
