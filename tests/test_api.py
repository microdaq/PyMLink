# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package.
# Embedded-solutions 2020, www.microdaq.org

"""
A module tests Python integration with C MLink library. No MicroDAQ device
is required.
"""

import os

import microdaq


def test_connect(mock_mdaq_cls, ip):
    _ = mock_mdaq_cls(ip)


def test_disconnect(mock_mdaq):
    mock_mdaq.disconnect()


def test_reconnect(mock_mdaq):
    mock_mdaq.reconnect()


def test_get_fw_version(mock_mdaq):
    mock_mdaq.get_fw_version()


def test_get_lib_version(mock_mdaq):
    mock_mdaq.get_lib_version()


def test_get_str_hw_info(mock_mdaq):
    mock_mdaq.get_str_hw_info()


def test_get_hw_info(mock_mdaq):
    mock_mdaq.get_hw_info()


def test_dsp_init(mock_mdaq):
    xcos_model = os.path.join("model", "signal-model.out")
    mock_mdaq.dsp_init(dsp_application=xcos_model, rate=10, duration=-1)


def test_dsp_start(mock_mdaq):
    mock_mdaq.dsp_start()


def test_dsp_is_done(mock_mdaq):
    mock_mdaq.dsp_is_done()


def test_dsp_wait_until_done(mock_mdaq):
    mock_mdaq.dsp_wait_until_done(timeout=-1)


def test_dsp_mem_write(mock_mdaq):
    mock_mdaq.dsp_mem_write(index=1, data=[0, 1, 2, 3])


def test_dsp_signal_read(mock_mdaq):
    mock_mdaq.dsp_signal_read(signal_id=1, vector_size=1, vector_count=10)


def test_dsp_stop(mock_mdaq):
    mock_mdaq.dsp_stop()


def test_dio_func(mock_mdaq):
    mock_mdaq.dio_func(func=6, state=False)


def test_dio_dir(mock_mdaq):
    mock_mdaq.dio_dir(bank=1, direction=0)


def test_dio_read(mock_mdaq):
    mock_mdaq.dio_read(dio=1)


def test_dio_write(mock_mdaq):
    mock_mdaq.dio_write(dio=1, state=False)


def test_func_key_read(mock_mdaq):
    mock_mdaq.func_key_read(key=1)


def test_led_write(mock_mdaq):
    mock_mdaq.led_write(led=1, state=1)


def test_enc_init(mock_mdaq):
    mock_mdaq.enc_init(module=1, mode=0)


def test_enc_read(mock_mdaq):
    mock_mdaq.enc_read(module=1)


def test_pwm_init(mock_mdaq):
    mock_mdaq.pwm_init(module=1, period=1000)


def test_pwm_write(mock_mdaq):
    mock_mdaq.pwm_write(module=1, duty_a=10, duty_b=50)


def test_ai_read(mock_mdaq):
    mock_mdaq.ai_read(channels=[1, 2], ai_range=[-10, 10])


def test_ai_scan_init(mock_mdaq):
    mock_mdaq.ai_scan_init(
        channels=[1, 2],
        ai_range=[-10, 10],
        is_differential=False,
        rate=1000,
        duration=1,
    )


def test_ai_scan(mock_mdaq):
    # need to initialize self._ai_scan_channels member
    mock_mdaq.ai_scan_init(
        channels=[1, 2],
        ai_range=[-10, 10],
        is_differential=False,
        rate=1000,
        duration=1,
    )

    # actual test
    mock_mdaq.ai_scan(scan_count=10, timeout=2)


def test_ao_write(mock_mdaq):
    mock_mdaq.ao_write(
        channels=[1, 2], ao_range=microdaq.AORange.AO_5V_UNI, data=[1.0, 2.0]
    )


def test_ao_scan_init(mock_mdaq):
    mock_mdaq.ao_scan_init(
        channels=[1, 2],
        initial_data=[[1, 2, 3], [1.5, 2.5, 3.5]],
        ao_range=[0, 5],
        is_stream_mode=False,
        rate=100,
        duration=-1,
    )


def test_ao_scan_data(mock_mdaq):
    mock_mdaq.ao_scan_data(
        channels=[1, 2], data=[[-1, -2, -3], [-4, -5, -6]], opt=True
    )


def test_ao_scan(mock_mdaq):
    mock_mdaq.ao_scan()


def test_ao_scan_wait_until_done(mock_mdaq):
    mock_mdaq.ao_scan_wait_until_done(timeout=-1)


def test_ao_scan_is_done(mock_mdaq):
    mock_mdaq.ao_scan_is_done()


def test_ao_scan_stop(mock_mdaq):
    mock_mdaq.ao_scan_stop()


def test_ai_scan_trigger_dio(mock_mdaq):
    mock_mdaq.ai_scan_trigger_dio(dio=6, level=1)


def test_ai_scan_trigger_clear(mock_mdaq):
    mock_mdaq.ai_scan_trigger_clear()


def test_ai_scan_trigger_dio_pattern(mock_mdaq):
    mock_mdaq.ai_scan_trigger_dio_pattern(pattern="xxxxx1xx")


def test_ai_scan_trigger_encoder(mock_mdaq):
    mock_mdaq.ai_scan_trigger_encoder(module=1, position=0, condition=0)


def test_ai_scan_trigger_ext_start(mock_mdaq):
    mock_mdaq.ai_scan_trigger_ext_start(source=microdaq.Triggers.DSP_START)


def test_ao_scan_trigger_dio(mock_mdaq):
    mock_mdaq.ao_scan_trigger_dio(dio=1, level=0)


def test_ao_scan_trigger_clear(mock_mdaq):
    mock_mdaq.ao_scan_trigger_clear()


def test_ao_scan_trigger_dio_pattern(mock_mdaq):
    mock_mdaq.ao_scan_trigger_dio_pattern(pattern="xxxxx1xx")


def test_ao_scan_trigger_encoder(mock_mdaq):
    mock_mdaq.ao_scan_trigger_encoder(module=1, position=0, condition=0)


def test_ao_scan_trigger_ext_start(mock_mdaq):
    mock_mdaq.ao_scan_trigger_ext_start(source=microdaq.Triggers.DSP_START)
