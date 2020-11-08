# This file is subject to the terms and conditions defined in
# file 'LICENSE.txt', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org


class MLinkError(Exception):
    pass


class MLink:
    def __init__(self, ip):
        self._serie = 2000
        self._adc = 9
        self._dac = 6
        self._cpu = 1
        self._mem = 2

        if ip == "999.999.999.999":
            raise MLinkError 
        _ = ip

    def ai_read(self, channels, *args):
        return [0.0]*len(channels)

    def disconnect(self):
        return True

    def get_str_hw_info(self):
        return f'MicroDAQ E{self._serie}-ADC0{self._adc}-DAC0{self._dac}-{self._cpu}{self._mem}'

    def get_hw_info(self):
        return (self._serie, self._adc, self._dac, self._cpu, self._mem)