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
Turn on and turn off LED 1. 

    import time
    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')
    mdaq.led_write(led_id=1, state=True)
    time.sleep(1.0)
    mdaq.led_write(led_id=1, state=False)

<br>

##### Analog input 
Read analog input channels 1 and 2.

    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')
    data = mdaq.ai_read(channels=[1, 2], ai_range=[-10, 10])

    for i, volt in enumerate(data):
        print('Channel[%d]: %f V' % (i, volt))

<br>

##### Analog output
Set 1.0V and 2.0V to analog output channels 1 and 2 respectively.
Used range 0-5 volts. 

    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')
    mdaq.ao_write(
        channels=[1, 2],
        ao_range=microdaq.AORange.AO_5V_UNI,
        data=[1.0, 2.0])
        
<br>

##### PWM
Generate PWM signal on two channels A and B (PWM module 1).\
![alt text](examples/resources/pwm.png "Signal waveform.")

    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')
    mdaq.pwm_init(module=1, period=1000)
    mdaq.pwm_write(module=1, duty_a=25, duty_b=50)
    
<br>

##### Encoder
Read encoder position.

    import time
    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')
    mdaq.enc_init(encoder=1, init_value=0)

    for i in range(30):
        time.sleep(0.1)
        enc = mdaq.enc_read(encoder=1)
        print('position: %d\tdir: %d' % (enc[0], enc[1]))

    
<br>


##### DSP with Scilab XCOS model 
Load and run application generated in Scilab XCOS. 

Application overview:\
![alt text](examples/resources/signal-model-view.jpg "A 'signal-model.zcos' scheme.")

    import os
    import microdaq

    mdaq = microdaq.Device(ip='10.10.1.1')

    model = os.path.join("resources", "signal-model.out")
    mdaq.dsp_init(dsp_application=model, rate=100, duration=-1)
    mdaq.dsp_start()

    print("DSP is running: %s" % mdaq.dsp_is_done())
    mdaq.dsp_stop()
    print("DSP is running: %s" % mdaq.dsp_is_done())
    
<br>

## Tests
This sections is meant to be for package's developers/contributors. Tests for API
layer which does not required connected MicroDAQ device could be triggered by 
`pytest tests/test_api.py`.

Additional requirements needed:\
`pip install -r requirements/tests.txt`
    
## License

The BSD license. For more information read **LICENSE.md** file.  
