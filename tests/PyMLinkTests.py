from py_mlink import PyMLink as pml
import sys
import time
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

IP = '10.10.1.1'

# print '****CONNECTION TEST****'
# try:
#     mdaq = pml.MLink(IP)
#
#     print mdaq.connect.__doc__
#     print 'diconenct()'
#     mdaq.disconnect()
#
#     print mdaq.reconnect.__doc__
#     print 'reconenct()'
#     mdaq.reconnect()
#
#     for i in range(2):
#         print 'diconenct()'
#         mdaq.disconnect()
#         print 'connect()'
#         mdaq.connect(IP)
#
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise
#
#
# raw_input("Press Enter to continue...")
# print '\n\n****LED TEST****'
# try:
#     mdaq = pml.MLink(IP)
#
#     for i in range(4):
#         time.sleep(0.5)
#         print 'LED 1 to 1 | LED 2 to 0'
#         mdaq.led_write(1, True)
#         mdaq.led_write(2, False)
#
#         time.sleep(0.5)
#         print 'LED 1 to 0 | LED 2 to 1'
#         mdaq.led_write(1, False)
#         mdaq.led_write(2, True)
#
#     mdaq.led_write(2, False)
#     mdaq.disconnect()
#
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise
#
#
# raw_input("Press Enter to continue...")
# print '\n\n****SET AO TEST****'
# try:
#     mdaq = pml.MLink(IP)
#     num_channels = 8
#
#     values = [x*0.1 for x in range(1, num_channels+1)]
#     channels = [x for x in range(1, num_channels+1)]
#
#     print len(values)
#     print 'Set analog output:'
#     print mdaq.ao_write.__doc__
#     mdaq.ao_write(channels, pml.AORange.AO_5V_UNI, values)
#     mdaq.disconnect()
#
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise
#
#
# raw_input("Press Enter to continue...")
# print '\n\n****GET VERSION TEST****'
# try:
#     print pml.MLink.__doc__
#     mdaq = pml.MLink(IP)
#     print 'MLINK ver:',  mdaq.get_version()
#     mdaq.disconnect()
#
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise
#
#
# raw_input("Press Enter to continue...")
# print '\n\n****DSP FUNCTIONS TEST****'
# try:
#     mdaq = pml.MLink(IP)
#
#     mdaq.dsp_load('pytong_led.out')
#     mdaq.dsp_start()
#     time.sleep(4.0)
#     mdaq.dsp_stop()
#     mdaq.disconnect()
#
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise
#
#
# raw_input("Press Enter to continue...")
# print '\n\n****DIO FUNCTIONS E1000 TEST****'
# try:
#     mdaq = pml.MLink(IP)
#
#     print mdaq.dio_dir.__doc__
#     mdaq.dio_dir(1, 0)  # set bank 1 to input mode
#     mdaq.dio_dir(2, 0)  # set bank 2 to input mode
#     mdaq.dio_dir(3, 0)  # set bank 3 to input mode
#     mdaq.dio_dir(4, 0)  # set bank 4 to input mode
#
#     print mdaq.dio_func.__doc__
#     for i in range(1, 7):
#         mdaq.dio_func(i, False)
#
#     print mdaq.dio_read.__doc__
#     for i in range(1, 33):
#         print 'DI %d: %d' % (i, mdaq.dio_read(i))
#
#     mdaq.dio_dir(1, 1)  # set bank 1 to output mode
#     mdaq.dio_dir(2, 1)  # set bank 2 to output mode
#     mdaq.dio_dir(3, 1)  # set bank 3 to output mode
#     mdaq.dio_dir(4, 1)  # set bank 4 to output mode
#
#     print mdaq.dio_write.__doc__
#     for i in range(1, 33):
#         mdaq.dio_write(i, True)
#
#     mdaq.disconnect()
#
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise

# print '\n\n****DIO FUNCTIONS E2000 TEST****'
# try:
#     mdaq = pml.MLink(IP)
#
#     print mdaq.dio_func.__doc__
#     for i in range(1, 7):
#         mdaq.dio_func(i, False)
#
#     print mdaq.dio_read.__doc__
#     for i in range(1, 9):
#         print 'DI %d: %d' % (i, mdaq.dio_read(i))
#
#     print mdaq.dio_write.__doc__
#     for i in range(9, 17):
#         mdaq.dio_write(i, True)
#
#     mdaq.disconnect()
#
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise

#
# raw_input("Press Enter to continue...")
# print '\n\n****FUNC KEY TEST****'
# try:
#     mdaq = pml.MLink(IP)
#     print mdaq.func_key_read.__doc__
#
#     for i in range(50):
#         time.sleep(0.1)
#         print 'KEY1/KEY2: %d/%d' % (mdaq.func_key_read(1), mdaq.func_key_read(2))
#
#     mdaq.disconnect()
#
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise
#
#
# raw_input("Press Enter to continue...")
# print '\n\n****ENCODER TEST****'
# try:
#     mdaq = pml.MLink(IP)
#     print mdaq.enc_init.__doc__
#     mdaq.enc_init(1, 0)
#
#     print mdaq.enc_read.__doc__
#
#     for i in range(500):
#         time.sleep(0.1)
#         enc = mdaq.enc_read(1);
#         print 'position: %d\ndir: %d\n' % (enc[0], enc[1])
#
#     mdaq.disconnect()
#
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise
#
#
# raw_input("Press Enter to continue...")
# print '\n\n****PWM TEST****'
# try:
#     pwm_module = 1
#     mdaq = pml.MLink(IP)
#     print mdaq.pwm_init.__doc__
#     mdaq.pwm_init(pwm_module, 1000)
#
#     print mdaq.pwm_write.__doc__
#     mdaq.pwm_write(pwm_module, 10, 50)
#
#     mdaq.disconnect()
#
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise
#
#
# raw_input("Press Enter to continue...")
# print '\n\n****AI TEST****'
# try:
#     mdaq = pml.MLink(IP)
#     channels = [ch for ch in range(1, 9)]
#
#     print mdaq.ai_read.__doc__
#     data = mdaq.ai_read(channels, [-10, 10])
#
#     print data
#
#     mdaq.disconnect()
#
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise
#
#
# raw_input("Press Enter to continue...")
# print '\n\n****AI SCAN TEST****'
# try:
#     mdaq = pml.MLink(IP)
#     channels = [x for x in range(1, 9)]
#
#     print mdaq.ai_scan_init.__doc__
#     # channels, range, isDifferential, rate, duration
#     mdaq.ai_scan_init([1, 2, 3], [-10, 10], [False, True, True], 1000, 1)
#     data = mdaq.ai_scan(1000, True)
#
#     # print data
#     print mdaq.ai_read.__doc__
#     #
#     # tic = time.clock()
#     # for i in range(50):
#     #     data = mdaq.ai_scan(1000, True)
#     #     for ch in data:
#     #         print ch
#     # toc = time.clock()
#     # print 'ai_scan exec time: %f sec' % (toc-tic)
#
#     mdaq.disconnect()
# #
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise
#
# print '\n\n****SCILAB COMP TEST****'
# try:
#     mdaq = pml.MLink(IP, connectionless=True)
#     tic = time.clock()
#     mdaq.led_write(1, 1)
#     toc = time.clock()
#     print 'exec_time: %f' % (toc-tic)
#
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise

# raw_input("Press Enter to continue...")
# print '\n\n****AO SCAN TEST - SINGLE****'
# try:
#     mdaq = pml.MLink(IP)
#     channels = [1, 2]
#
#     print mdaq.ao_scan_init.__doc__
#     # mdaqAOScanInit(linkID, channels, initialData, range, isStreamMode, rate, duration
#     mdaq.ao_scan_init([1, 2], [[1, 2, 3], [4, 5, 6]], [-10, 10], False, 100, -1)
#     mdaq.ao_scan()
#     time.sleep(1)
#
#     print mdaq.ao_scan_data.__doc__
#     mdaq.ao_scan_data([1, 2], [[-1, -2, -3], [-4, -5, -6]], True)
#     time.sleep(1)
#
#     mdaq.ao_scan_stop()
# except pml.MLinkError, errval:
#     print "Error:", errval
# except:
#     print "Unexpected error:", sys.exc_info()[0]
#     raise

# raw_input("Press Enter to continue...")
#print '\n\n****AO SCAN TEST - CONTINUOUS****'
#try:
#    mdaq = pml.MLink(IP)
#    channels = [1, 2]
#
#    print mdaq.ao_scan_init.__doc__
#    mdaq.ao_scan_init([1, 2], [[3], [4]], [-10, 10], True, 100, -1)
#    mdaq.ao_scan()
#
#    for i in range(10):
#        mdaq.ao_scan_data([1, 2], [[5], [6]], True)
#
#    mdaq.ao_scan_stop()
#except:
#    print "Unexpected error:", sys.exc_info()[0]
#    raise

#raw_input("Press Enter to continue...")
#print '\n\n****DSP signal 1 ****'
#try:
#    mdaq = pml.MLink(IP)
#
#    print mdaq.dsp_run.__doc__
#    mdaq.dsp_run("model\signal-model.out", 0.1);
#
#    print mdaq.dsp_signal_read.__doc__
#
#    print mdaq.dsp_signal_read(1, 1, 5)
#    print mdaq.dsp_signal_read(2, 1, 5)
#    print mdaq.dsp_signal_read(3, 1, 5)
#
#    print mdaq.dsp_stop.__doc__
#    mdaq.dsp_stop()
#except:
#    print "Unexpected error:", sys.exc_info()[0]
#    raise

#print '\n\n****DSP signal 2 with MEM ****'
#try:
#    mdaq = pml.MLink(IP)
#
#    print mdaq.dsp_run.__doc__
#    mdaq.dsp_run("model\signal-model.out", 0.1)
#    mdaq.dsp_mem_write(1, [1, 2, 3, 4])
#
#    print mdaq.dsp_signal_read.__doc__
#
#    for i in range(0, 10):
#        print mdaq.dsp_signal_read(4, 4, 2)
#
#    print mdaq.dsp_stop.__doc__
#    mdaq.dsp_stop()
#except:
#    print "Unexpected error:", sys.exc_info()[0]
#    raise
