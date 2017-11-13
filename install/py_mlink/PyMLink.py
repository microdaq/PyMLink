# MLink Python2.7 binding
# visit site www.microdaq.org
# Embedded-solutions, November 2017

import ctypes_mlink as cml
from ctypes import *
from functools import wraps


class MLinkError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class AIRange(object):
    AI_10V = [-10, 10]
    AI_10V_UNI = [0, 10]

    AI_5V = [-5, 5]
    AI_5_12V = [-5.12, 5.12]

    AI_2V = [-2, 2]
    AI_2_56V = [-2.56, 2.56]

    AI_1V = [-1, 1]
    AI_1_24V = [-1.24, 1.24]

    AI_0_64V = [-0.64, 0.64]


class AORange(object):
    AO_10V = [-10, 10]
    AO_10V_UNI = [0, 10]

    AO_5V = [-5, 5]
    AO_5V_UNI = [0, 5]

    AO_2_5V = [-2.5, 2.5]


class MLink:
    '''
    Description:
        Main class of MLink Python2.7 binding.
    Usage:
        MLink(ip, maintain_connection=False)
        ip - ip address of MicroDAQ device
        maintain_connection - True or False
            True  - more convenient, no needs to keep connection (each function call connect()
                    method), slightly less performance
            False - better performance, user has to worry about connection timeout (depends on OS)
                    To keep connection call method reconnect() or any other method.
    '''

    # ------------ SPECIAL FUNCTIONS ------------
    def __init__(self, ip='10.10.1.1', maintain_connection=False):
        self._linkfd = -1
        self._ip = ip
        self._connectionless = maintain_connection
        self._ao_scan_ch = 0
        self._mdaq_hwid = 0
        self.disconnect()

        self.connect(ip)
        self._hwid()
        self.disconnect()

        if not self._connectionless:
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
    @_connect_decorate
    def _hwid(self):
        hwid_raw = c_int * 5
        hwid_raw = hwid_raw(0)

        res = cml.mlink_hwid(pointer(self._linkfd), byref(hwid_raw))

        self._mdaq_hwid = hwid_raw
        self._raise_exception(res)

    def disconnect(self):
        '''
        Description:
            Disconnects from MicroDAQ device
        Usage:
            disconnect()
        '''

        cml.mlink_disconnect_all()

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
            self.disconnect()
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

    def hw_info(self):
        '''
        Description:
            Prints model of connected MicroDAQ device  
        Usage:
            hw_info()
         '''

        print 'MicroDAQ E%d-ADC%d-DAC%d-%d%d' % tuple(self._mdaq_hwid)

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
                5 - PWM3: DIO14 - Channel A, DIO15 - Channel B (enabled by default)
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
            res = cml.mlink_dio_read(pointer(self._linkfd), d, pointer(value))
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
            res = cml.mlink_dio_write(pointer(self._linkfd), d, state[i])
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
        res = cml.mlink_func_read(pointer(self._linkfd), key, pointer(value))
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
        res = cml.mlink_led_write(pointer(self._linkfd), ledid, state)
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
        res = cml.mlink_enc_init(pointer(self._linkfd), encoder, init_value)
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
        position = c_int32()
        res = cml.mlink_enc_read(pointer(self._linkfd), encoder, pointer(encdir), pointer(position))
        self._raise_exception(res)
        return position.value, encdir.value

    # ------------ PWM FUNCTIONS ------------
    @_connect_decorate
    def pwm_init(self, pwm_module, period, active_low=False, duty_a=0, duty_b=0):
        """
        Description:
            Setup MicroDAQ PWM outputs
        Usage:
            pwm_init(module, period, active_low=False, duty_a=0, duty_b=0)
            pwm_module - PWM module (1, 2 or 3)
            period - PWM module period in microseconds(1-1000000)
            active_low - PWM waveform polarity (True or False)
            duty_a - PWM channel A duty (0-100)
            duty_b - PWM channel B duty (0-100)
        """
        res = cml.mlink_pwm_init(pointer(self._linkfd), pwm_module, period, active_low, duty_a, duty_b)
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
        res = cml.mlink_pwm_write(pointer(self._linkfd), module, duty_a, duty_b)
        self._raise_exception(res)

    # ------------ ANALOG IO FUNCTIONS ------------
    @_connect_decorate
    def ai_read(self, channels, ai_range=AIRange.AI_10V, is_differential=False):
        """
        Description:
            Reads MicroDAQ analog inputs
        Usage:
            ai_read(channels, range=AIRange.AI_10V, is_differential=False)
            channels - analog input channels to read
            ai_range - analog input range:
                AI_10V     - [-10, 10]
                AI_10V_UNI - [0, 10]
                AI_5V      - [-5, 5]
                AI_5_12V   - [-5.12, 5.12]
                AI_2V      - [-2, 2]
                AI_2_56V   - [-2.56, 2.56]  
                AI_1V      - [-1, 1]
                AI_1_24V   - [-1.24, 1.24]
                AI_0_64V   - [-0.64, 0.64]
                AIRange.AI_10V  -    single-range argument applied for all used channels
                AIRange.AI_10V  + AIRange.AI_5V  - multi-range argument for two channels

            is_differential - scalar or array with measurement mode settings: 
                              True  - differential 
                              False - single-ended mode
        """

        if not isinstance(channels, list):
            channels = [channels]

        if not isinstance(is_differential, list):
            is_differential = [is_differential]

        if len(is_differential) == 1 and len(channels) != 1:
            is_differential_cpy = is_differential
            for i in range(len(channels) - 1):
                is_differential = is_differential + is_differential_cpy
        elif len(channels) != len(is_differential):
            raise MLinkError('ai_scan_init: Mode (is_differential parameter) vector should match selected AI channels')

        if len(ai_range) == 2 and len(channels) != 1:
            range_cpy = ai_range
            for i in range(len(channels)-1):
                ai_range = ai_range + range_cpy
        elif len(channels) != len(ai_range) / 2:
            raise MLinkError('ai_scan_init: Range vector should match selected AI channels!')

        channels_idx = c_int8 * len(channels)
        channels_idx = channels_idx(*channels)
        channels_val = c_double * (len(channels))
        channels_val = channels_val()
        channels_range = c_double * (len(ai_range))
        channels_range = channels_range(*ai_range)

        diff = c_int8 * len(is_differential)
        diff = diff(*is_differential)

        res = cml.mlink_ai_read(pointer(self._linkfd), byref(channels_idx), len(channels), byref(channels_range),
                                byref(diff), byref(channels_val))
        self._raise_exception(res)

        val_list = [channels_val[i] for i in xrange(len(channels))]
        if len(val_list) == 1:
            return val_list[0]
        else:
            return val_list


    @_connect_decorate
    def ai_scan_init(self, channels, ai_range, is_differential, rate, duration):
        """
        Description:
            Init AI scan
        Usage:
            ai_scan_init(channels, ai_range, is_differential, rate, duration)
            channels - analog input channels to read
            ai_range - analog input range:
                AI_10V     - [-10, 10]
                AI_10V_UNI - [0, 10]
                AI_5V      - [-5, 5]
                AI_5_12V   - [-5.12, 5.12]
                AI_2V      - [-2, 2]
                AI_2_56V   - [-2.56, 2.56]
                AI_1V      - [-1, 1]
                AI_1_24V   - [-1.24, 1.24]
                AI_0_64V   - [-0.64, 0.64]
                AIRange.AI_10V  -    single-range argument applied for all used channels
                AIRange.AI_10V  + AIRange.AI_5V  - multi-range argument for two channels

            is_differential - scalar or array with measurement mode settings:
                              True  - differential
                              False - single-ended mode
            rate - analog input scan frequency [Hz]
            duration - analog input scan duration in seconds
        """
        if not isinstance(channels, list):
            channels = [channels]
        if not isinstance(is_differential, list):
            is_differential = [is_differential]

        if len(is_differential) == 1 and len(channels) != 1:
            is_differential_cpy = is_differential
            for i in range(len(channels) - 1):
                is_differential = is_differential + is_differential_cpy
        elif len(channels) != len(is_differential):
            raise MLinkError('ai_scan_init: Mode (is_differential parameter) vector should match selected AI channels')

        if len(ai_range) == 2 and len(channels) != 1:
            range_cpy = ai_range
            for i in range(len(channels)-1):
                ai_range = ai_range + range_cpy
        elif len(channels) != len(ai_range) / 2:
            raise MLinkError('ai_scan_init: Range vector should match selected AI channels!')

        if duration < 0:
            duration = -1

        self._ai_scan_channels = channels
        channels_idx = c_int8 * len(channels)
        channels_idx = channels_idx(*channels)
        channels_range = c_double * (len(ai_range))
        channels_range = channels_range(*ai_range)
        diff = c_int8 * len(is_differential)
        diff = diff(*is_differential)
        rate = c_float(rate)

        res = cml.mlink_ai_scan_init(pointer(self._linkfd), byref(channels_idx), len(channels), channels_range,
                                     byref(diff), pointer(rate), duration)
        print res
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
    def ao_write(self, channels, ao_range, data):
        '''
        Description:
            Writes data to MicroDAQ analog outputs
        Usage:
            ao_write(channels, range, data)
            channels - analog output channels
            ao_range - analog output range matrix e.g.
                AO_10V      - [-10, 10]
                AO_10V_UNI  - [0, 10]
                AO_5V       - [-5, 5]
                AO_5V_UNI   - [0, 5]
                AO_2_5V     - [-2.5, 2.5]                
                AORange.AO_5V_UNI - single-range argument applied for all used channels
                AORange.AO_5V + AORange.AO_10V  - multi-range argument for two channels
                
            data - data to be written
        '''

        if not isinstance(channels, list):
            channels = [channels]
        if not isinstance(data, list):
            data = [data]
        if not isinstance(ao_range, list):
            ao_range = [ao_range]

        if len(channels) != len(data):
            raise MLinkError('ao_read: Data vector should match selected AI channels!')

        if len(ao_range) == 2 and len(channels) != 1:
            range_cpy = ao_range
            for i in range(len(channels)-1):
                ao_range = ao_range + range_cpy
        elif len(channels) != len(ao_range)/2:
            raise MLinkError('ao_read: Range vector should match selected AI channels!')

        channels_idx = c_int8 * len(channels)
        channels_idx = channels_idx(*channels)
        channels_val = c_double * len(channels)
        channels_val = channels_val(*data)
        channels_range = c_double * (len(ao_range))
        channels_range = channels_range(*ao_range)

        res = cml.mlink_ao_write(pointer(self._linkfd), byref(channels_idx), len(channels), byref(channels_range), 1,
                                 byref(channels_val))
        self._raise_exception(res)


    @_connect_decorate
    def ao_scan_init(self, channels, initial_data, ao_range, is_stream_mode, rate, duration):
        '''
        Description:
            Initiates AO scan
        Usage:
            ao_scan_init(channels, initial_data, ao_range, is_stream_mode, rate, duration)
            channels - analog output channels to write
            initial_data - output data
            ao_range - analog output range matrix e.g.
                AO_10V      - [-10, 10]
                AO_10V_UNI  - [0, 10]
                AO_5V       - [-5, 5]
                AO_5V_UNI   - [0, 5]
                AO_2_5V     - [-2.5, 2.5]    
                AORange.AO_5V_UNI - single-range argument applied for all used channels
                AORange.AO_5V + AORange.AO_10V  - multi-range argument for two channels
                
            is_stream_mode - mode of operation (True - stream, False - periodic)
            rate - scans per second rate (scan frequency) [Hz]
            duration - analog output scan duration in seconds
        '''

        if not isinstance(channels, list):
            channels = [channels]

        if not isinstance(initial_data, list):
            initial_data = [initial_data]

        ch_len = len(channels)
        self._ao_scan_ch = ch_len

        if len(ao_range) == 2 and len(channels) != 1:
            range_cpy = ao_range
            for i in range(len(channels)-1):
                ao_range = ao_range + range_cpy
        elif len(channels) != len(ao_range)/2:
            raise MLinkError('ao_read: Range vector should match selected AI channels!')

        data_size = 0
        if isinstance(initial_data[0], list):
            data_size_ch = len(initial_data[0])
            if all(len(x) == data_size_ch for x in initial_data):
                pass
            else:
                raise MLinkError('Wrong AO scan data size.')

            for ch_data in initial_data:
                data_size = data_size + len(ch_data)
            # make a flat list
            initial_data = sum(initial_data, [])
        else:
            if len(channels) > 1:
                raise MLinkError('Wrong AO scan data size.')
            data_size = len(initial_data)

        ao_data = c_float * data_size
        ao_data = ao_data(*initial_data)
        channels_idx = c_uint8 * ch_len
        channels_idx = channels_idx(*channels)
        channels_range = c_double * (len(ao_range))
        channels_range = channels_range(*ao_range)

        res = cml.mlink_ao_scan_init(pointer(self._linkfd), byref(channels_idx), len(channels), byref(ao_data),
                                     c_int(data_size), byref(channels_range), c_uint8(is_stream_mode), c_float(rate),
                                     c_float(duration))
        self._raise_exception(res)

    @_connect_decorate
    def ao_scan_data(self, channels, data, opt=True):
        '''
        Description:
           Queues data to be output
        Usage:
            ao_data_queue(channels, data, opt=True)
            channels - analog output channels to write
            data - data to be output
            opt - reset buffer index to 0 (True/False) - periodic mode
                  blocking/non-blocking   (True/False) - stream mode 
        '''

        if not isinstance(data, list):
            data = [data]

        if not isinstance(channels, list):
            channels = [channels]

        data_size = 0
        if isinstance(data[0], list):
            data_size_ch = len(data[0])
            if all(len(x) == data_size_ch for x in data):
                pass
            else:
                raise MLinkError('Wrong AO scan data size.')

            for ch_data in data:
                data_size = data_size + len(ch_data)
            # make a flat list
            data = sum(data, [])
        else:
            if len(channels) > 1:
                raise MLinkError('Wrong AO scan data size.')
            data_size = len(data)

        ch_len = len(channels)

        ao_data = c_float * data_size
        ao_data = ao_data(*data)
        channels_idx = c_uint8 * ch_len
        channels_idx = channels_idx(*channels)

        res = cml.mlink_ao_scan_data(pointer(self._linkfd), byref(channels_idx), c_int(ch_len), byref(ao_data),
                                     c_int(data_size), c_uint8(opt))
        self._raise_exception(res)


    @_connect_decorate
    def ao_scan(self):
        '''
        Description:
            Starts AO scanning.
        Usage:
            ao_scan()
        '''

        res = cml.mlink_ao_scan(pointer(self._linkfd))
        self._raise_exception(res)

    @_connect_decorate
    def ao_scan_stop(self):
        '''
        Description:
            Stops AO scanning.
        Usage:
            ao_scan_stop()
        '''

        res = cml.mlink_ao_scan_stop(pointer(self._linkfd))
        self._raise_exception(res)

    @_connect_decorate
    def ai_scan_stop(self):
        '''
        Description:
            Stops AI scanning.
        Usage:
            ai_scan_stop()
        '''

        res = cml.mlink_ai_scan_stop(pointer(self._linkfd))
        self._raise_exception(res)
