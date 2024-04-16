import requests
import websocket
import json
import threading
import time
import struct
import re
from pathlib import Path
from enum import Enum
from typing import List, Dict

from microdaq import Device


class Opcode(Enum):
    READ = 0
    WRITE = 1


class App:
    """
    Description:
        Class to interact with PyCodeGen application
    Usage:
        App(device, password)
        device - MLink device
        password - optional password
    """

    HTTP_PORT = 5000
    TRANSPORT_PORT = 1236
    MDAQ_EXT = ".mdaq"
    CONNECT_TIMEOUT = 5 # seconds
    INTERVAL = 0.01 # seconds
    COMMANDS_CHANNEL_ID = -1
    SEND_PARAMS_CHANNEL_ID = -2
    COMMAND_ATTACH = 1

    def __init__(self, device: Device, password: str | None = None) -> None:
        self.device = device
        self._transport_ws = None
        self._transport_thread = None
        self._logs_ws = None
        self._is_connected = False
        self._is_running = False
        self._connection_error = False
        self._model_data = None
        self._optimization = "f"
        self._read_channels = {}
        self._read_channel_id_by_name = {}
        self._write_channels = {}
        self._write_channel_id_by_name = {}
        self._data = {}
        self._data_lock = threading.Lock()
        self._changed_params = {}
        self._session = requests.Session()

        if password != None:
            self._login(password)

        self._logs_thread = threading.Thread(target=self._connect_logs)
        self._logs_thread.daemon = True
        self._logs_thread.start()

        t0 = time.time()
        while not self._is_connected:
            time.sleep(App.INTERVAL)
            if time.time() - t0 > App.CONNECT_TIMEOUT:
                raise TimeoutError("Cannot connect to device")

    def __del__(self):
        self.close()

    def list(self, path: str = "") -> List[str]:
        """
        Description:
            Returns list of models saved on device
        Usage:
            list(path)
            path - path to storage folder
        """

        resp = self._session.get(f"{self._http_address()}/storage/list/{path}")

        if not resp.ok:
            raise Exception(resp.text)

        return [file for file in resp.json()["files"] if file.endswith(App.MDAQ_EXT)]

    def upload(self, src: str, dst: str) -> None:
        """
        Description:
            Uploads model from local file (src) to device's storage (dst)
        Usage:
            upload(src, dst)
            src - path to local file (can be with or without .mdaq extension)
            dst - path to storage file (can be with or without .mdaq extension)
        """

        dst_path = Path(dst)
        dst_name = dst_path.name
        if not dst_name.endswith(App.MDAQ_EXT):
            dst_name += App.MDAQ_EXT

        if not src.endswith(App.MDAQ_EXT):
            src += App.MDAQ_EXT

        resp = self._session.post(
            f"{self._http_address()}/storage/upload/{dst_path.parent}",
            files={"file": (dst_name, open(src, "rb"))}
        )

        if not resp.ok:
            raise Exception(resp.text)

    def build(self, model: str) -> None:
        """
        Description:
            Builds model located on device's storage
        Usage:
            build(model)
            model - path to model (can be with or without .mdaq extension)
        """

        if not model.endswith(App.MDAQ_EXT):
            model += App.MDAQ_EXT

        resp = self._session.get(f"{self._http_address()}/storage/download/{model}")

        if not resp.ok:
            raise Exception(resp.text)

        model_data = json.loads(resp.text)

        resp = self._session.post(
            f"{self._http_address()}/codegen/build",
            json=model_data
        )

        if not resp.ok:
            raise Exception(resp.text)

        self._model_data = model_data
        self._retrieve_model_info()
        self._changed_params = {}

    def info(self) -> Dict:
        """
        Description:
            Shows information about current model

        Return:
            Dict with 2 items:
            "inputs" - Dict with names as keys and information about signal as values
                e.g. {"Watch/1": {"rows": 1, "columns": 1, "stream": False}}
            "properties" - Dict with names and current values
                e.g. {"Number/Value": 4.5}
        """

        inputs = {}
        for name, id in self._read_channel_id_by_name.items():
            read_channel = self._read_channels[id]
            inputs[name] = {
                "rows": read_channel["size"],
                "columns": read_channel["width"],
                "stream": read_channel["mode"] == "stream"
            }

        params = {}
        for name, id in self._write_channel_id_by_name.items():
            if id in self._changed_params:
                v = self._changed_params[id]
            else:
                v = self._write_channels[id]["init_value"]

            if type(v) == list and len(v) == 1:
                v = v[0]

            params[name] = v

        return {"inputs": inputs, "properties": params}

    def start(
        self,
        rate: float | None = None,
        duration: float | None = None
    ) -> None:
        """
        Description:
            Starts execution of current model
        Usage:
            start(rate, duration)
            rate - interval in seconds
            duration - time of execution in seconds
                negative value means execution will run indefinitely
        """

        data = {}
        if rate != None:
            data["period"] = rate

        if duration != None:
            data["stop_time"] = duration

        if len(self._changed_params) > 0:
            data["variables"] = json.dumps(self._changed_params)

        resp = self._session.post(f"{self._http_address()}/codegen/run", data=data)

        if not resp.ok:
            raise Exception(resp.text)

        self._begin_simulation()

    def attach(self) -> None:
        """Attaches to currently running model"""

        resp = self._session.post(f"{self._http_address()}/codegen/attach")

        if not resp.ok:
            raise Exception(resp.text)

        self._model_data = json.loads(resp.text)

        self._retrieve_model_info()
        self._begin_simulation()

        self._transport_ws.send(
            self._pack_message(
                Opcode.WRITE,
                App.COMMANDS_CHANNEL_ID,
                data=struct.pack(self._optimization, App.COMMAND_ATTACH)
            )
        )

        if len(self._write_channels) > 0:
            while len(self._data[App.SEND_PARAMS_CHANNEL_ID]) == 0:
                self._request_data(App.SEND_PARAMS_CHANNEL_ID)
                time.sleep(App.INTERVAL)

            self._read_properties(self._data[App.SEND_PARAMS_CHANNEL_ID])

    def stop(self) -> None:
        """Stops execution"""

        resp = self._session.post(f"{self._http_address()}/codegen/terminate")

        if not resp.ok:
            raise Exception(resp.text)

        self.wait_until_done()

    def is_done(self) -> bool:
        """Returns True when execution stopped"""

        return not self._is_running

    def wait_until_done(self) -> None:
        """Waits until execution is done"""

        while self._is_running:
            time.sleep(App.INTERVAL)

    def close(self) -> None:
        """Safely closes application"""

        try:
            if self._transport_ws != None and self._transport_thread.is_alive():
                self._transport_ws.close()
                self._transport_thread.join()
        except:
            pass

        try:
            if self._logs_thread.is_alive():
                self._logs_ws.close()
                self._logs_thread.join()
        except:
            pass

    def write(self, channel: str, values: float | List[float]) -> None:
        """
        Description:
            Writes data to channel
        Usage:
            write(channel, values)
            channel - name of parameter channel
            values - data to write. Must be the same size as channel
        """

        channel = self._write_channel_starndard_name(channel)

        if not channel in self._write_channel_id_by_name:
            raise Exception(f"Channel {channel} does not exist or cannot be written to")

        id = self._write_channel_id_by_name[channel]

        if type(values) != list:
            values = [values]

        if len(values) != self._write_channels[id]["size"]:
            raise Exception(
                f"Cannot write to channel {channel}, "
                f"size of values ({len(values)}) do not match "
                f"size of channel ({self._write_channels[id]['size']})"
            )

        self._changed_params[id] = values
        if self._is_running:
            data = struct.pack(f"{len(values)}{self._optimization}", *values)
            self._transport_ws.send(self._pack_message(Opcode.WRITE, id, data=data))

    def read(self, source) -> List[float] | Dict[str, List[float]]:
        """
        Description:
            Reads data from channel or stream
        Usage:
            read(source)
            source - name of channel or Stream object
        Return:
            When reading from channel - List with data from single signal
            When reading from stream - Dict with channel names as keys and Lists with data as values
        """

        if type(source) == str:
            return self._read_simple(source)
        else:
            return self._read_stream(source)

    def _http_address(self) -> str:
        return f"http://{self.device.get_ip()}:{App.HTTP_PORT}"

    def _logs_address(self) -> str:
        return f"ws://{self.device.get_ip()}:{App.HTTP_PORT}/logs"

    def _transport_address(self) -> str:
        return f"ws://{self.device.get_ip()}:{App.TRANSPORT_PORT}"

    def _login(self, password: str) -> None:
        resp = self._session.post(
            f"{self._http_address()}/login_api",
            data={"password": password}
        )

        if not resp.json()["logged_in"]:
            raise Exception("Incorrect password")

    def _request_data(self, id: int) -> None:
        self._transport_ws.send(self._pack_message(Opcode.READ, id))

    def _read_simple(self, channel: str) -> List[float]:
        if not channel in self._read_channel_id_by_name:
            raise Exception(f"Channel {channel} does not exist or cannot be read")

        id = self._read_channel_id_by_name[channel]
        read_channel = self._read_channels[id]

        self._multi_inputs_read_correctly(read_channel, channel)

        with self._data_lock:
            self._data[id].clear()

        self._request_data(id)

        while(len(self._data[id]) == 0):
            time.sleep(App.INTERVAL)

        with self._data_lock:
            ret = self._data[id][-read_channel["length"]:]
            self._data[id].clear()

        return ret

    def _read_stream(self, stream) -> Dict[str, List[float]]:
        for channel in stream.channels:
            id = self._read_channel_id_by_name.get(channel, None)
            if id == None:
                raise Exception(f"Channel {channel} does not exist or cannot be read")

            if self._read_channels[id]["mode"] != "stream":
                raise Exception("Cannot read stream from non-stream channel")

        ret = {}
        t0 = time.time()
        while True:
            recieved_all = True
            for channel in stream.channels:
                if channel not in ret:
                    id = self._read_channel_id_by_name[channel]
                    read_channel = self._read_channels[id]

                    self._multi_inputs_read_correctly(read_channel, channel)

                    count = read_channel["length"] * stream.count

                    if len(self._data[id]) >= count:
                        with self._data_lock:
                            ret[channel] = self._data[id][:count]
                            self._data[id] = self._data[id][count:]
                    else:
                        recieved_all = False
                        self._request_data(id)

            if recieved_all:
                return ret
            else:
                if stream.timeout != None and time.time() - t0 >= stream.timeout:
                    raise TimeoutError()

                time.sleep(App.INTERVAL)

    def _multi_inputs_read_correctly(self, read_channel: Dict, channel: str) -> None:
        if read_channel.get("multi_inputs", False):
            if read_channel["read_from"] == "":
                read_channel["read_from"] = channel
            else:
                if read_channel["read_from"] != channel:
                    raise Exception(
                        "When output is connected to multiple inputs, "
                        "reading can be only done via one input"
                    )

    def _retrieve_model_info(self) -> None:
        if self._model_data["config"]["general"]["optimization"] == "Speed":
            self._optimization = "f"
        else:
            self._optimization = "d"

        nodes_by_id = {node["id"]: node for node in self._model_data["nodes"]}
        links_by_id = {link[0]: link for link in self._model_data["links"]}

        self._read_channels = {}
        self._read_channel_id_by_name = {}
        self._write_channels = {}
        self._write_channel_id_by_name = {}

        for node in self._model_data["nodes"]:
            if "inputs" in node["codegen"]:
                variable = node["codegen"]["inputs"]["variable"]
                for input_n, cg_input in enumerate(variable.values()):
                    if "mode" not in cg_input or cg_input["mode"] == "on_demand":
                        continue

                    # get id of output connected to this input (shadow_id)
                    input = node["inputs"][input_n] 
                    link = links_by_id[input["link"]]
                    source_node = nodes_by_id[link[1]]
                    id = list(source_node["codegen"]["outputs"]["variable"].values())[link[2]]["id"]

                    full_name = f"{node['title']}/{input_n + 1}"

                    if id in self._read_channels:
                        channel = self._read_channels[id]
                        channel["multi_inputs"] = True

                        if channel["mode"] != "stream" and cg_input["mode"] == "stream":
                            channel["mode"] = "stream"

                    else:
                        channel = {
                            "id": id,
                            "size": cg_input["size"],
                            "width": cg_input.get("width", 1),
                            "mode": cg_input["mode"]
                        }
                        channel["length"] = channel["size"] * channel["width"]

                        self._read_channels[id] = channel

                    self._read_channel_id_by_name[full_name] = id

            if "parameters" in node["codegen"] and "variable" in node["codegen"]["parameters"]:
                variable = node["codegen"]["parameters"]["variable"]
                name_from_cg_name = {self._codegen_name(k): k for k in node["properties"].keys()}
                for param_name, cg_param in variable.items():
                    if "mode" not in cg_param or cg_param["mode"] != "online":
                        continue

                    id = cg_param["id"]

                    full_name = f"{node['title']}/"
                    if param_name in name_from_cg_name:
                        full_name += name_from_cg_name[param_name].lower()
                    else:
                        full_name += param_name

                    self._write_channels[id] = {
                        "id": id,
                        "size": cg_param["size"],
                        "init_value": cg_param["value"]
                    }
                    self._write_channel_id_by_name[full_name] = id

    def _codegen_name(self, name: str) -> str:
        return re.sub("\\s+", "_", name).lower()

    def _write_channel_starndard_name(self, name: str) -> str:
        parts = name.split("/")
        parts[-1] = parts[-1].lower()
        return "/".join(parts)

    def _begin_simulation(self) -> None:
        self._data.clear()
        self._data[App.SEND_PARAMS_CHANNEL_ID] = []
        for id, read_channel in self._read_channels.items():
            self._data[id] = []

            if read_channel.get("multi_inputs", False):
                read_channel["read_from"] = ""

        self._connection_error = False

        self._transport_thread = threading.Thread(target=self._connect_transport)
        self._transport_thread.start()

        while not self._is_running and not self._connection_error:
            time.sleep(App.INTERVAL)

    def _connect_logs(self) -> None:
        cookies = [f"{k}={v}" for k, v in self._session.cookies.items()]
        self._logs_ws = websocket.WebSocketApp(
            self._logs_address(),
            on_message=self._on_logs_message,
            cookie=", ".join(cookies)
        )
        self._logs_ws.run_forever()

    def _on_logs_message(self, ws, message):
        try:
            msg = json.loads(message)
            if "action" in msg:
                if msg["action"] == "connection_start":
                    self._is_connected = True

                elif msg["action"] == "resend_timestamp":
                    ws.send(json.dumps({"timestamp": msg["timestamp"]}))

        except Exception:
            pass

    def _connect_transport(self):
        self._transport_ws = websocket.WebSocketApp(
            self._transport_address(),
            on_open=self._on_transport_open,
            on_close=self._on_transport_close,
            on_error=self._on_transport_error,
            on_message=self._on_transport_message
        )
        self._transport_ws.run_forever()

    def _on_transport_open(self, ws):
        self._is_running = True

    def _on_transport_error(self, ws, error):
        self._connection_error = True

    def _on_transport_close(self, ws, a, b):
        self._is_running = False
        self._transport_ws = None

    def _on_transport_message(self, ws, message):
        if len(message) > 24:
            id = struct.unpack_from("i", message, 4)[0]

            with self._data_lock:
                if id < 0:
                    self._data[id] = message[24:]

                else:
                    n = int((len(message) - 24) / struct.calcsize(self._optimization))
                    v = list(struct.unpack_from(f"{n}{self._optimization}", message, 24))
                    self._data[id].extend(v)

    def _pack_message(
        self,
        opcode: Opcode,
        signal_id: int,
        overrun: int = 0,
        frame_count: int = 0,
        channels: int = 0,
        data: bytes = b""
    ) -> bytes:
        def int_to_bytes(v):
            return v.to_bytes(4, "little", signed=True)

        msg = int_to_bytes(opcode.value)
        msg += int_to_bytes(signal_id)
        msg += int_to_bytes(len(data))
        msg += int_to_bytes(overrun)
        msg += int_to_bytes(frame_count)
        msg += int_to_bytes(channels)
        msg += data
        return msg

    def _read_properties(self, data: bytes) -> None:
        pos = 0
        while pos < len(data):
            id = struct.unpack_from("i", data, pos)[0]
            n = self._write_channels[id]["size"]
            v = list(struct.unpack_from(f"{n}{self._optimization}", data, pos + 4))
            self._changed_params[id] = v
            pos += 4 + n * struct.calcsize(self._optimization)

    class Stream:
        """
        Description:
            Object needed to read from stream channels
            New Stream cannot be created when another Stream already exists
            Use Stream in with statement, e.g. with app.Stream("Watch/1", 10) as stream:
            or when stream is no loger needed call destroy() method
        Usage:
            app.Stream(channels, count, timeout_s=None)
            channels - name of stream channel or list of names
            count - number of signals to read
            timeout_s - timeout in seconds
        """

        _instance = None

        def __new__(cls, channels, count, timeout_s = None):
            if cls._instance != None:
                raise Exception("Only 1 Stream object can exist at the same time")

            cls._instance = super().__new__(cls)
            return cls._instance

        def __init__(self, channels: str | List[str], count: int, timeout_s: float | None = None) -> None:
            if type(channels) != list:
                channels = [channels]

            self._channels = channels
            self._count = count
            self._timeout = timeout_s

        def __enter__(self):
            return self

        def __exit__(self, err_type, err_val, err_trace):
            self.destroy()

        @property
        def channels(self) -> List[str]:
            return self._channels

        @property
        def count(self) -> int:
            return self._count

        @property
        def timeout(self) -> float | None:
            return self._timeout

        def destroy(self) -> None:
            if App.Stream._instance == self:
                App.Stream._instance = None
