# microdaq

This package allows users to use data acquisition under MicroDAQ hardware 
with Python2.7 and Python 3. It provides an interface between the MLink driver 
and Python. The package works with Windows x86/x64, Linux x86/x64, MacOS x64 
and EABI ARM machines.

## installation

Run `pip install microdaq`

## examples
In order to run any example, simply run a script, e.g.:\
`python exmaples/ai-demo.py`

##### LED control example:

    import time
    
    import microdaq

    mdaq = micordaq.Device('10.10.1.1')  # connect to MDAQ
    mdaq.led_write(1, True)              # Turn on LED 1
    mdaq.led_write(2, True)              # Turn on LED 2
    time.sleep(1.0)                      # Wait a second
    mdaq.led_write(1, False)             # Turn off LED 1
    mdaq.led_write(2, False)             # Turn off LED 2

## license

The BSD license. For more information read _LICENSE_ file.  
