# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

import microdaq

mdaq = microdaq.Device("10.10.1.1")
channels = [x for x in range(1, 9)]

print(mdaq.ai_scan_init.__doc__)
# channels, range, isDifferential, rate, duration
mdaq.ai_scan_init([1, 2, 3], [-10, 10], [False, True, True], 1000, 1)

print(mdaq.ai_scan.__doc__)
data = mdaq.ai_scan(1000, True)
