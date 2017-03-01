# MLink Python2.7 binding.
# visit site www.microdaq.org
# author Witczenko
# email witczenko@gmail.com

import ctypes_mlink as cml
from ctypes import *
from functools import wraps


class MLinkError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class AIRange(object):
    AI_10V = 0
    AI_5V = 1
    AI_2V5 = 2
    AI_1V25 = 3
    AI_0V64 = 4
    AI_0V32 = 5


class AIPolarity(object):
    AI_BIPOLAR = 24
    AI_UNIPOLAR = 25


class AIMode(object):
    AI_SINGLE = 28
    AI_DIFF = 29


class MLink:
    '''
    Description:
        Main class of MLink Python2.7 binding.
    Usage:
        MLink(ip, connectionless=True)
        ip - ip address of MicroDAQ device
        connectionless - True or False
            True  - more convenient, no needs to keep connection (each function call connect()
                    method), slightly less performance
            False - better performance, user has to worry about connection timeout (10 sec)
                    To keep connection call method reconnect() or any other method.
    '''
    # ------------ SPECIAL FUNCTIONS ------------
    def __init__(self, ip='10.10.1.1', connectionless=True):
        self._linkfd = -1
        self._ip = ip
        self._connectionless = connectionless

        if not connectionless:
            self.connect(ip)

    def _get_error(self, errcode):
        return cml.mlink_error(errcode)

    def _raise_exception(self, res):
        if res == -1:
            raise MLinkError('Session timeout, restore connection with reconnect() or connect(ip) method.')
        elif res < -1:
            print 'Error code:', res
            raise MLinkError(self._get_error(res))

    def _connect_decorate(func):
        @wraps(func)
        def func_wrapper(self, *original_args, **original_kwargs):
            if self._connectionless:
                self.reconnect()
                ans = func(self, *original_args, **original_kwargs)
                self.disconnect()
            else:
                ans = func(self, *original_args, **original_kwargs)
            return ans
        return func_wrapper

    # ------------ UTILITY FUNCTIONS ------------
    def disconnect(self):
        '''
        Description:
            Disconnects from MicroDAQ device
        Usage:
            disconnect()
        '''
        # print 'Disconnect'
        cml.mlink_disconnect(self._linkfd)

    def connect(self, ip):
        '''
        Description:
            Connects to MicroDAQ device
        Usage:
            connect(ip)
            ip - ip address
        '''
        # print 'Connect'
        self._linkfd = c_int32()
        self._ip = ip

        res = cml.mlink_connect(ip, 4343, pointer(self._linkfd))
        self._raise_exception(res)

    def reconnect(self):
        '''
        Description:
            Connects to MicroDAQ device with latest ip
            obtained from class constructor or connect method
        Usage:
            reconnect()
        '''
        if self._ip is not None:
            self.connect(self._ip)

    @_connect_decorate
    def get_version(self):
        '''
        Description:
            Returns version of MLink library
        Usage:
            get_version()
         '''
        return cml.mlink_version(pointer(self._linkfd))

    # ------------ DSP FUNCTIONS ------------
    @_connect_decorate
    def dsp_load(self, dsp_firmware, param=''):
        '''
        Description:
            Loads DSP program
        Usage:
            dsp_load(dsp_firmware, param='')
            dsp_firmware - XCos generated DSP application path
            param - optional parameters
        '''
        res = cml.mlink_dsp_load(pointer(self._linkfd), dsp_firmware, param)
        self._raise_exception(res)

    @_connect_decorate
    def dsp_start(self):
        '''
        Description:
            Starts DSP program
        Usage:
            dsp_start()
        '''
        res = cml.mlink_dsp_start(pointer(self._linkfd))
        self._raise_exception(res)

    @_connect_decorate
    def dsp_stop(self):
        '''
        Description:
            Stops DSP program
        Usage:
            dsp_stop()
        '''
        res = cml.mlink_dsp_stop(pointer(self._linkfd))
        self._raise_exception(res)

    # TODO: doc - validate
    @_connect_decorate
    def dsp_upload(self):
        '''
            Description:
                Uploads DSP program to MicroDAQ memory.
                DSP program will be loaded automatically after device reboot.
            Usage:
                dsp_upload()
        '''
        res = cml.mlink_dsp_upload(pointer(self._linkfd))
        self._raise_exception(res)

    # ------------ DIGITAL IO FUNCTIONS ------------
    @_connect_decorate
    def dio_func(self, func, state):
        '''
        Description:
            Sets DIO alternative function
        Usage:
            dio_func(func, state)
            func - DIO alternative function
                1 - ENC1: DIO1 - Channel A, DIO2 - Channel B (enabled by default)
                2 - ENC2: DIO3 - Channel A, DIO4 - Channel B (enabled by default)
                3 - PWM1: DIO10 - Channel A, DIO11 - Channel B (enabled by default)
                4 - PWM2: DIO12 - Channel A, DIO13 - Channel B (enabled by default)
                5 - PWM3: DIO14 - Channel A, DIO14 - Channel B (enabled by default)
                6 - UART: DIO8 - Rx, DIO9 - Tx (enabled by default)
            state - function state (True/False to enable/disable function)
        '''
        res = cml.mlink_dio_set_func(pointer(self._linkfd), func, state)
        self._raise_exception(res)

    @_connect_decorate
    def dio_dir(self, bank, direction):
        '''
        Description:
            Sets MicroDAQ DIO bank direction
        Usage:
            dio_dir(bank, direction)
            bank - bank number (1-4)
            direction - bank direction (True - output, False - input)
        '''
        res = cml.mlink_dio_set_dir(pointer(self._linkfd), bank, direction, 0)
        self._raise_exception(res)

    @_connect_decorate
    def dio_read(self, dio):
        '''
        Description:
            Reads DIO state
        Usage:
            dio_dir(dio)
            bank - bank number (1-4)
            dio - DIO number
        '''
        if not isinstance(dio, list):
            dio = [dio]

        value = c_uint8()
        data = []
        for d in dio:
            res = cml.mlink_dio_get(pointer(self._linkfd), d, pointer(value))
            self._raise_exception(res)
            data += [value.value]

        if len(data) == 1:
            return data[0]
        else:
            return data

    @_connect_decorate
    def dio_write(self, dio, state):
        '''
        Description:
            Writes DIO state
        Usage:
            mdaq_dio_write(dio, state)
            dio - DIO numbers
            state - DIO output states
        '''

        if not isinstance(dio, list):
            dio = [dio]
        if not isinstance(state, list):
            state = [state]

        if len(dio) != len(state):
            raise MLinkError('dio_write: Number of channels and data is not equal!')

        i = 0
        for d in dio:
            res = cml.mlink_dio_set(pointer(self._linkfd), d, state[i])
            i += 1
            self._raise_exception(res)

    @_connect_decorate
    def func_key_read(self, key):
        '''
        Description:
            Reads MicroDAQ function key state
        Usage:
            func_key_read(key)
            key - key number (1 or 2)
        '''
        value = c_uint8()
        res = cml.mlink_func_key_get(pointer(self._linkfd), key, pointer(value))
        self._raise_exception(res)
        return value.value

    @_connect_decorate
    def led_write(self, ledid, state):
        """
        Description:
            Sets MicroDAQ D1 and D2 LED state
        Usage:
            set_led(led, state)
            led - LED number (1 or 2)
            state - LED state (True - ON, False - OFF)
        """
        res = cml.mlink_led_set(pointer(self._linkfd), ledid, state)
        self._raise_exception(res)

    # ------------ ENCODER READ FUNCTIONS ------------
    @_connect_decorate
    def enc_init(self, encoder, init_value):
        """
        Description:
            Initializes encoder module
        Usage:
            enc_init(encoder, init_value)
            encoder - encoder module (1 or 2)
            init_value - initial encoder value
        """
        res = cml.mlink_enc_reset(pointer(self._linkfd), encoder, init_value)
        self._raise_exception(res)

    @_connect_decorate
    def enc_read(self, encoder):
        """
        Description:
            Reads encoder position and motion direction
        Usage:
            enc_read(encoder)
            encoder - encoder module (1 or 2)
        """
        encdir = c_uint8()
        position = c_uint32()
        res = cml.mlink_enc_get(pointer(self._linkfd), encoder, pointer(encdir), pointer(position))
        self._raise_exception(res)
        return position.value, encdir.value

    # ------------ PWM FUNCTIONS ------------
    @_connect_decorate
    def pwm_init(self, module, period, active_low):
        """
        Description:
            Setup MicroDAQ PWM outputs
        Usage:
            pwm_init(module, period, active_low)
            module - PWM module (1, 2 or 3)
            period - PWM module period in microseconds(1-1000000)
            active_low - PWM waveform polarity (True or False)
        """
        res = cml.mlink_pwm_config(pointer(self._linkfd), module, period, active_low, 0, 0)
        self._raise_exception(res)

    @_connect_decorate
    def pwm_write(self, module, duty_a, duty_b):
        """
        Description:
            Sets MicroDAQ PWM outputs
        Usage:
            pwm_write(module, duty_a, duty_b)
            module - PWM module (1, 2 or 3)
            duty_a - PWM channel A duty (0-100)
            duty_b - PWM channel B duty (0-100)
        """
        res = cml.mlink_pwm_set(pointer(self._linkfd), module, duty_a, duty_b)
        self._raise_exception(res)

    # ------------ ANALOG IO FUNCTIONS ------------
    @_connect_decorate
    def ai_read(self, channels, range=AIRange.AI_10V, polarity=AIPolarity.AI_BIPOLAR, mode=AIMode.AI_SINGLE):
        """
        Description:
            Reads MicroDAQ analog inputs
        Usage:
            ai_read(channels, range=AIRange.AI_10V, polarity=AIPolarity.AI_BIPOLAR, mode=AIMode.AI_SINGLE)
            channels - analog input channels to read
            range - analog input range:
                                        AIRange.AI_10V
                                        AIRange.AI_5V
                                        AIRange.AI_2V5
                                        AIRange.AI_1V25
                                        AIRange.AI_0V64
                                        AIRange.AI_0V32
            polarity - analog input polarity (AIPolarity.AI_BIPOLAR or AIPolarity.AI_UNIPOLAR)
            mode - measurement type (AIMode.AI_SINGLE or AIMode.AI_DIFF)
        """

        if not isinstance(channels, list):
            channels = [channels]

        channels_idx = c_int8 * len(channels)
        channels_idx = channels_idx(*channels)
        channels_val = c_float * len(channels)
        channels_val = channels_val()

        res = cml.mlink_ai_read(pointer(self._linkfd), 1, byref(channels_idx), len(channels), range, polarity, mode,
                                byref(channels_val))
        self._raise_exception(res)

        val_list = [channels_val[i] for i in xrange(len(channels))]
        if len(val_list) == 1:
            return val_list[0]
        else:
            return val_list

    @_connect_decorate
    def ai_scan_init(self, channels, frequency, duration, range=AIRange.AI_10V, polarity=AIPolarity.AI_BIPOLAR,
                     mode=AIMode.AI_SINGLE):
        """
        Description:
            Init AI scan
        Usage:
            ai_scan_init(channels, frequency, time, range=AIRange.AI_10V, polarity=AIPolarity.AI_BIPOLAR,
                        mode=AIMode.AI_SINGLE)
            channels - analog input channels to read
            frequency - analog input scan frequency [Hz]
            duration - analog input scan duration in seconds
            range - analog input range:
                                        AIRange.AI_10V
                                        AIRange.AI_5V
                                        AIRange.AI_2V5
                                        AIRange.AI_1V25
                                        AIRange.AI_0V64
                                        AIRange.AI_0V32
            polarity - analog input polarity (%T - bipolar, %F - unipolar)
            mode - measurement type (AIMode.AI_SINGLE or AIMode.AI_DIFF)
        """
        if not isinstance(channels, list):
            channels = [channels]

        self._ai_scan_channels = channels
        channels_idx = c_int8 * len(channels)
        channels_idx = channels_idx(*channels)
        res = cml.mlink_ai_scan_init(pointer(self._linkfd), byref(channels_idx), len(channels), range, polarity, mode,
                                     frequency, duration)
        self._raise_exception(res)

    @_connect_decorate
    def ai_scan(self, scan_count, blocking):
        """
        Description:
            Starts scanning and reads scan data
        Usage:
            ai_scan(scan_count, blocking)
            scan_count - number of scans to read
            blocking - blocking or non-blocking read (True/False)
        """
        data_len = scan_count*len(self._ai_scan_channels)
        channels_val = c_double * data_len
        channels_val = channels_val()
        res = cml.mlink_ai_scan(byref(channels_val), scan_count, blocking)
        self._raise_exception(res)

        val_list = []
        for channel in xrange(0, len(self._ai_scan_channels)):
            val_list.append([channels_val[i+channel] for i in xrange(0, scan_count, len(self._ai_scan_channels))])

        return val_list

    @_connect_decorate
    def ao_write(self, channels, data):
        '''
        Description:
            Writes data to MicroDAQ analog outputs
        Usage:
            ao_write(channels, data)
            channels - analog output channels
            data - data to be written
        '''

        if not isinstance(channels, list):
            channels = [channels]
        if not isinstance(data, list):
            data = [data]

        if len(channels) != len(data):
            raise MLinkError('ao_write: Number of channels and data is not equal!')

        channels_idx = c_int8 * len(channels)
        channels_idx = channels_idx(*channels)
        channels_val = c_float * len(channels)
        channels_val = channels_val(*data)

        res = cml.mlink_ao_write(pointer(self._linkfd), 1, byref(channels_idx), len(channels), 1, byref(channels_val))
        self._raise_exception(res)

    # TODO: doc & generate new PyMlink (missing ao_scan* functions)
    # def ao_scan_init(self, channels, trigger, frequency, duration, range=AIRange.AI_10V):
    #     '''
    #     Description:
    #         Init AO scan
    #     Usage:
    #         ao_scan_init(channels, trigger, frequency, duration, range=AIRange.AI_10V)
    #         channels - analog output channels to write
    #         range - analog output range
    #             Avaliable output ranges:
    #               0: 0-5V
    #               1: 0-10V
    #               2: 5V
    #               3: 10V
    #               4: 2.5V
    #         trigger - DIO number (DIO1-8), high state triggers scanning
    #         frequency - analog input scan frequency [Hz]
    #         duration - analog output scan duration in seconds
    #     '''
    #
    #     channels_idx = c_int8 * len(channels)
    #     channels_idx = channels_idx(*channels)
    #
    #     res = cml.mlink_ao

