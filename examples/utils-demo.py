# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2017-2020, www.microdaq.org

import microdaq

# Print documentation e.g:
print(microdaq.Device.__doc__)
print(microdaq.Device.ai_scan_init.__doc__)

# Connect to MicroDAQ device without worrying about
# connection timeout (maintain_connection=True)
# this option has slightly less performance
mdaq = microdaq.Device('10.10.1.1', maintain_connection=True)

# Print model name of connected MicroDAQ device
mdaq.get_hw_info()

# Catch MLink errors
try:
    mdaq.ai_read(99, [-10, 10], False)
except microdaq.MLinkError as errval:
    print("Error:", errval)

    # Close connection
    mdaq.disconnect()
