# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import microdaq

mdaq = microdaq.Device("10.10.1.1")
print(
    "Firmware version (major.minor.fix.build): %d.%d.%d.%d"
    % mdaq.get_fw_version()
)

print(
    "MLink version (major.minor.fix.build): %d.%d.%d.%d"
    % mdaq.get_lib_version()
)

print(
    "Hardware version\n"
    "Series: %d\n"
    "ADC: %d\n"
    "DAC: %d\n"
    "CPU: %d\n"
    "MEM: %d\n" % mdaq.get_hw_info()
)
print("Hardware version (str): %s" % mdaq.get_str_hw_info())
