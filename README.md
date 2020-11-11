# microdaq

This package allows users to use data acquisition under MicroDAQ hardware 
with Python2.7 and Python 3. It provides an interface between the MLink driver 
and Python. The package works with Windows x86/x64, Linux x86/x64, MacOS x64 
and EABI ARM machines.

## installation

`pip install microdaq`

## examples
In order to run any example, simply run a script, e.g.:\
`python exmaples/ai-demo.py`

##### LED control example

    import time
    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')   # connect to MDAQ
    mdaq.led_write(led_id=1, state=True)     # Turn on LED 1
    time.sleep(1.0)                          # Wait a second
    mdaq.led_write(led_id=1, state=False)    # Turn off LED 1

##### Analog input 

    import time
    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')                     # connect to MDAQ
    data = mdaq.ai_read(channels=[1, 2], ai_range=[-10, 10])   # read from AIs
    
    for i, volt in enumerate(data):
        print('Channel[%d]: %f V' % (i, volt))

##### Analog output

    import time
    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')                     # connect to MDAQ
    mdaq.ao_write(
        channels=[1, 2], 
        ao_range=micordaq.AORange.AO_5V_UNI, 
        data=[1.0, 2.0])  
    
    for i, volt in enumerate(data):
        print('Channel[%d]: %f V' % (i, volt))
        
##### PWM

    import time
    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')                     # connect to MDAQ
    mdaq.pwm_init(1, 1000)
    mdaq.pwm_write(pwm_module, 10, 50)
    
##### DSP with Scilab XCOS model 
    
## license

The BSD license. For more information read _LICENSE_ file.  
