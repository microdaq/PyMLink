# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import microdaq

mdaq = microdaq.Device("10.10.1.1")
print("Firmware version: %s" % mdaq.get_fw_version())
print("MLink version:    %s" % mdaq.get_lib_version())
print("Device version:   %s" % mdaq.get_str_hw_info())
