import os
import ctypes
import cantools

import microdaq

class StructPrinter:
    def __str__(self) -> str:
        values = ", ".join(f"{name}={value}" for name, value in self._asdict().items())

        return f"<{self.__class__.__name__}: {values}>"

    def _asdict(self) -> dict:
        return {field[0]: getattr(self, field[0]) for field in self._fields_}


class FrameStructure(ctypes.LittleEndianStructure, StructPrinter):
    @classmethod
    def from_bytes(cls, byte_data: bytes):
        assert len(byte_data) == ctypes.sizeof(cls), \
            f"Wrong size {ctypes.sizeof(cls)} != {len(byte_data)}"

        data = (ctypes.c_uint8 * len(byte_data))(*byte_data)
        return ctypes.cast(data, ctypes.POINTER(cls)).contents

    def into_bytes(self) -> bytes:
        return bytes(self)


class CanFdTxHeader(FrameStructure):
    _pack_ = 4
    _fields_ = [
        ("ID", ctypes.c_uint32, 29),
        ("RTR", ctypes.c_uint32, 1),
        ("XTD", ctypes.c_uint32, 1),
        ("ESI", ctypes.c_uint32, 1),

        ("DLC", ctypes.c_uint8, 4),
        ("BRS", ctypes.c_uint8, 1),
        ("FDF", ctypes.c_uint8, 1),
        ("reserved", ctypes.c_uint8, 1),
        ("EFC", ctypes.c_uint8, 1),

        ("MM", ctypes.c_uint8, 8),
    ]


class CanFdTxFrame(FrameStructure):
    _pack_ = 4
    _fields_ = [
        ("header", CanFdTxHeader),
        ("data", ctypes.c_uint8*64)
    ]


class CanFdRxHeader(FrameStructure):
    _pack_ = 4
    _fields_ = [
        ("ID", ctypes.c_uint32, 29),
        ("RTR", ctypes.c_uint32, 1),
        ("XTD", ctypes.c_uint32, 1),
        ("ESI", ctypes.c_uint32, 1),

        ("RXTS", ctypes.c_uint16, 16),

        ("DLC", ctypes.c_uint8, 4),
        ("BRS", ctypes.c_uint8, 1),
        ("FDF", ctypes.c_uint8, 1),
        ("reserved", ctypes.c_uint8, 2),

        ("FIDX", ctypes.c_uint8, 7),
        ("ANMF", ctypes.c_uint8, 1),
    ]


class CanFdRxFrame(FrameStructure):
    _pack_ = 4
    _fields_ = [
        ("header", CanFdRxHeader),
        ("data", ctypes.c_uint8*64)
    ]


if __name__ == '__main__':
    # sizeof TX/RX frame is 72 bytes
    tx_frame = CanFdTxFrame() 

    # data can be generated based on DBC frame description  
    db = cantools.database.load_file(os.path.join("resources", "abs.dbc"))
    # take message from dbc 
    frame_MM5_10_TX1 = db.get_message_by_name("MM5_10_TX1")
    # get frame data for signals values: 
    # Yaw_Rate = 1
    # AY1 = 2
    data = frame_MM5_10_TX1.encode({'Yaw_Rate': 1, 'AY1': 2})

    # copy payload 
    tx_frame.data = (ctypes.c_ubyte * 64)(*[x for x in data])
    # set ID 
    tx_frame.header.ID = frame_MM5_10_TX1.frame_id
    # for frames longer then 8 bytes DLC has to be calculated - DLC max is 15
    tx_frame.header.DLC = len(data)
    # CANfd frame 
    tx_frame.header.FDF = 1

    frame1 = tx_frame.into_bytes()


    #  ----------------------------------------------------------------
    # data can be generated based on raw values 
    tx_frame.header.ID = 221 
    tx_frame.header.DLC = 15 
    tx_frame.header.FDF = 1

    tx_frame.data[0] = 1
    tx_frame.data[1] = 2
    tx_frame.data[2] = 3
    tx_frame.data[3] = 4
    tx_frame.data[4] = 5
    tx_frame.data[5] = 0
    tx_frame.data[63] = 15 

    frame2 = tx_frame.into_bytes()
  
    # connect with device 
    mdaq = microdaq.Device("10.10.1.1")

    # write frame data 
    # first arg - offset in bytes 
    mdaq.dsp_write_raw_mem(0, frame1);
    mdaq.dsp_write_raw_mem(72, frame2);

    # initialize DSP 
    mdaq.dsp_init(os.path.join("resources", "mdaq_can_repeater.out"), -1, -1)

    # start 
    mdaq.dsp_start()


