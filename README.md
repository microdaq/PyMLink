# Microdaq

This package allows users to use data acquisition under MicroDAQ hardware 
with Python2.7 and Python 3. It provides an interface between the MLink driver 
and Python application. The package works with Windows x86/x64, Linux x86/x64, MacOS x64 
and EABI ARM machines.

## Installation

`pip install microdaq`

If already installed, upgrading could be done by\
`pip install microdaq --upgrade `

## Examples

Sample programs are located in `examples` directory. In order to run them,
connect MicroDAQ device to your computer and run chosen script without any 
additional steps. For example: `python exmaples/ai-demo.py`

Scripts from **'examples/complex'** require additional packages to work.\
They could be installed via `pip install -r requirements/examples.txt` command.

<br>

##### LED control example


    import time
    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')   # connect to MDAQ
    mdaq.led_write(led_id=1, state=True)     # Turn on LED 1
    time.sleep(1.0)                          # Wait a second
    mdaq.led_write(led_id=1, state=False)    # Turn off LED 1

<br>

##### Analog input 

    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')                     # connect to MDAQ
    data = mdaq.ai_read(channels=[1, 2], ai_range=[-10, 10])   # read from AIs
    
    for i, volt in enumerate(data):
        print('Channel[%d]: %f V' % (i, volt))

<br>

##### Analog output

    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')                     # connect to MDAQ
    mdaq.ao_write(                                             # read channel 1, 2
        channels=[1, 2], 
        ao_range=micordaq.AORange.AO_5V_UNI, 
        data=[1.0, 2.0])  
    
    for i, volt in enumerate(data):
        print('Channel[%d]: %f V' % (i, volt))
        
<br>

##### PWM

    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')                     # connect to MDAQ
    mdaq.pwm_init(pwm_module=1, period=1000)                   # setup PWM01
    mdaq.pwm_write(pwm_module=1, duty_a=10, duty_b=50)         # start PWM01 
    
<br>

##### DSP with Scilab XCOS model 
    
## license

The BSD license. For more information read **LICENSE.md** file.  
