# PyMLink 

This package allows users to use data acquisition under MicroDAQ hardware with Python2.6/2.7 and Python 3. 
It provides an interface between the MLink driver and Python. 
The package works with Windows x86/x64, Linux x86/x64, MacOS x64 and EABI ARM machines.

## Installation

To install this package:<br />
1. Open install directory.<br /> 
2. Run `pip install .` (if Linux/MacOS, admin privileges required)

## Tests 

The `pytest` package is required in order to run tests.<br />
1. `pip install pytest`
2. `cd tests`
3. `pytest --ip <microdaq_ip>`



## License

The BSD license. 
