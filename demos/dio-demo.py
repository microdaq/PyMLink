# Digital I/O demo
# visit site www.microdaq.org
# author Witczenko
# email witczenko@gmail.com

from py_mlink import PyMLink

try:
    # Create MLink object, connect to MicroDAQ device
    pml = PyMLink.MLink('10.10.1.1')

    # Configure Digital I/O
    # Disable all functions: encoder, pwm, uart
    for i in range(1, 7):
        pml.dio_func(i, False)

    # Set first 8 I/O to input mode
    pml.dio_dir(1, False)
    # Set next 8 I/O to output mode
    pml.dio_dir(2, True)

    # Choose channels to read eg. 1..8
    channels_in = [ch for ch in range(1, 9)]
    # Choose channels to write eg. 9..16
    channels_out = [ch for ch in range(9, 17)]
    channels_out_data = [True for state in range(8)]

    # Read data
    data_in = pml.dio_read(channels_in)
    # Set data
    pml.dio_write(channels_out, channels_out_data)

    # Print data
    i = 0
    for ch in channels_in:
        print 'DI[%d]: %d' % (ch, data_in[i])
        i += 1

except PyMLink.MLinkError, errval:
    print "Error:", errval
