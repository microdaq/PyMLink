import time

import pytest

from microdaq import App


def generate_not_existing_name(existing_names, initial_name):
    i = 1
    name = initial_name
    while name in existing_names:
        name = f"{initial_name}{i}"
        i += 1

    return name


@pytest.fixture()
def device(mock_mdaq):
    return mock_mdaq


@pytest.fixture(scope="function")
def app(device):
    app = App(device)
    yield app
    app.close()


@pytest.fixture()
def model(request, app):
    model_name = request.node.get_closest_marker("model_name")

    if model_name == None:
        model_name = "numberWatch"
    else:
        model_name = model_name.args[0]

    app.upload(f"models/{model_name}", model_name)
    app.build(model_name)

    return app


@pytest.fixture()
def running_model(model):
    model.start(0.1, 5)
    yield model
    model.stop()


@pytest.mark.parametrize("use_extension", [False, True])
def test_upload(app, use_extension):
    existing_files = app.list()
    existing_names = [name[:-5] for name in existing_files]
    model_name = generate_not_existing_name(existing_names, "uploadTest")
    suffix = ".mdaq" if use_extension else ""

    app.upload("models/numberWatch" + suffix, model_name + suffix)
    current_files = app.list()
    new_file = list(set(current_files).difference(set(existing_files)))[0]

    assert new_file == model_name + ".mdaq"


def test_start_stop(model):
    model.start(0.1, 5)
    running_after_start = not model.is_done()
    model.stop()

    assert running_after_start
    assert model.is_done()


def test_wait_until_done(model):
    model.start(0.1, 5)
    running_after_start = not model.is_done()
    model.wait_until_done()

    assert running_after_start
    assert model.is_done()


def test_read(running_model):
    assert running_model.read("Watch/1") == [1]


@pytest.mark.model_name("counterDownload")
def test_read_stream(running_model):
    with running_model.Stream("Download/1", 10) as stream:
        vs1 = running_model.read(stream)["Download/1"]
        vs2 = running_model.read(stream)["Download/1"]

    assert vs1 == list(range(10))
    assert vs2 == list(range(10, 20))


@pytest.mark.model_name("counterDownload")
def test_read_simple_from_stream(running_model):
    time.sleep(1)
    v1 = running_model.read("Download/1")[0]
    with running_model.Stream("Download/1", 10) as stream:
        vs = running_model.read(stream)["Download/1"]

    assert v1 >= 10
    assert all([v > v1 for v in vs])


def test_read_stream_from_simple(running_model):
    with running_model.Stream("Watch/1", 10) as stream:
        with pytest.raises(Exception):
            running_model.read(stream)["Watch/1"]


@pytest.mark.model_name("counterDownload")
def test_read_stream_timeout(running_model):
    with running_model.Stream("Download/1", 40, 4.5) as stream:
        vs = running_model.read(stream)["Download/1"]

    assert vs == list(range(40))


@pytest.mark.model_name("counterDownload")
def test_read_stream_timeout_exceed(running_model):
    with running_model.Stream("Download/1", 40, 2) as stream:
        with pytest.raises(TimeoutError):
            running_model.read(stream)


@pytest.mark.model_name("multiTypes")
def test_read_sequence(running_model):
    with running_model.Stream(["Plot/2"], 3) as stream:
        vs = running_model.read(stream)["Plot/2"]

    assert vs == [i % 10 + 1 for i in range(30)]


@pytest.mark.model_name("multiTypes")
def test_read_matrix(running_model):
    with running_model.Stream(["Plot 2/1"], 5) as stream:
        vs = running_model.read(stream)["Plot 2/1"]

    assert vs == [1, 10, 100, 2, 20, 200, 3, 30, 300, 4, 40, 400] * 5


@pytest.mark.model_name("multiTypes")
def test_read_multiple_streams(running_model):
    with running_model.Stream(["Download/1", "Plot/1", "Plot/2", "Plot 2/1"], 1) as stream:
        data1 = running_model.read(stream)

    with running_model.Stream(["Download/1", "Plot/1", "Plot/2", "Plot 2/1"], 3) as stream:
        data2 = running_model.read(stream)

    dataVector = [1, 2, 3, 4, 5]
    dataSequence = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    dataMatrix = [1, 10, 100, 2, 20, 200, 3, 30, 300, 4, 40, 400]

    assert data1["Download/1"] == [0]
    assert data1["Plot/1"] == dataVector
    assert data1["Plot/2"] == dataSequence
    assert data1["Plot 2/1"] == dataMatrix

    assert data2["Download/1"] == [1, 2, 3]
    assert data2["Plot/1"] == dataVector * 3
    assert data2["Plot/2"] == dataSequence * 3
    assert data2["Plot 2/1"] == dataMatrix * 3


@pytest.mark.model_name("counterDownload")
def test_read_high_frequency(model):
    model.start(0.001, 3)
    with model.Stream("Download/1", 1000) as stream:
        vs1 = model.read(stream)["Download/1"]
        vs2 = model.read(stream)["Download/1"]
        vs3 = model.read(stream)["Download/1"]

    assert vs1 == list(range(1000))
    assert vs2 == list(range(1000, 2000))
    assert vs3 == list(range(2000, 3000))


@pytest.mark.model_name("counterDownload")
def test_read_exact_samples_count(model):
    model.start(0.01, 1)
    with model.Stream("Download/1", 101) as stream:
        vs1 = model.read(stream)["Download/1"]

    time.sleep(1)
    model.start(0.01, 1)
    with model.Stream("Download/1", 102) as stream:
        with pytest.raises(Exception):
            model.read(stream)["Download/1"]

    assert vs1 == list(range(101))


def test_create_2_streams_without_destroy(app):
    with app.Stream("Watch/1", 10) as stream1:
        with pytest.raises(Exception):
            with app.Stream("Watch/1", 30) as stream2:
                pass


@pytest.mark.parametrize("upper_case", [False, True])
def test_write(running_model, upper_case):
    v1 = running_model.read("Watch/1")
    write_channel = "Number/Value" if upper_case else "Number/value"
    running_model.write(write_channel, 4.5)
    time.sleep(1)
    v2 = running_model.read("Watch/1")

    assert v1 == [1]
    assert v2 == [4.5]


def test_write_before_start(model):
    model.write("Number/value", 7.125)
    model.start()
    v = model.read("Watch/1")
    model.stop()

    assert v == [7.125]


@pytest.mark.model_name("number3Watch")
def test_write_vector(running_model):
    v1 = running_model.read("Watch/1")
    running_model.write("Number/value", [11, 2.5, 101])
    time.sleep(1)
    v2 = running_model.read("Watch/1")

    assert v1 == [0, 0, 0]
    assert v2 == [11, 2.5, 101]


@pytest.mark.model_name("number3Watch")
def test_write_vector_before_start(model):
    model.write("Number/value", [0.05, 0.5, 5])
    model.start(0.1, 5)
    v = model.read("Watch/1")
    model.stop()

    assert v == [0.05, 0.5, 5]


@pytest.mark.model_name("number3Watch")
def test_write_incorrect_size(model):
    with pytest.raises(Exception):
        model.write("Number/value", [1, 2])


@pytest.mark.model_name("buttonWatch")
def test_write_internal_property(running_model):
    v1 = running_model.read("Watch/1")
    running_model.write("Button/value", 3)
    time.sleep(0.1)
    v2 = running_model.read("Watch/1")

    assert v1 == [0]
    assert v2 == [3]


@pytest.mark.model_name("operation")
def test_write_enum_property(running_model):
    running_model.write("Operation/Operation", 1)
    time.sleep(0.1)
    v1 = running_model.read("Watch/1")
    running_model.write("Operation/Operation", 2)
    time.sleep(0.1)
    v2 = running_model.read("Watch/1")
    running_model.write("Operation/Operation", 0)
    time.sleep(0.1)
    v3 = running_model.read("Watch/1")

    assert v1 == [1]
    assert v2 == [6]
    assert v3 == [5]


@pytest.mark.model_name("multiInputs")
@pytest.mark.parametrize("channel", ["Watch/1", "Download/1", "Plot/1"])
def test_multi_inputs_simple(running_model, channel):
    v1 = running_model.read(channel)
    time.sleep(0.1)
    v2 = running_model.read(channel)

    assert v2 > v1


@pytest.mark.model_name("multiInputs")
@pytest.mark.parametrize("channel", ["Download/1", "Plot/1"])
def test_multi_inputs_stream(running_model, channel):
    with running_model.Stream(channel, 10) as stream:
        vs1 = running_model.read(stream)[channel]
        vs2 = running_model.read(stream)[channel]

    assert vs1 == list(range(10))
    assert vs2 == list(range(10, 20))


@pytest.mark.model_name("multiInputs")
def test_multi_inputs_cannot_read_from_2(running_model):
    with running_model.Stream(["Plot/1", "Download/1"], 10) as stream:
        with pytest.raises(Exception):
            running_model.read(stream)


def test_attach(device):
    app1 = App(device)
    app1.upload("models/numberWatch", "numberWatch")
    app1.build("numberWatch")
    app1.start(0.1, 20)
    app1.write("Number/value", 6.75)
    app1.close()
    time.sleep(1)

    app2 = App(device)
    app2.attach()
    v = app2.read("Watch/1")
    app2.stop()
    app2.close()

    assert v == [6.75]


def test_attach_stream(device):
    app1 = App(device)
    app1.upload("models/counterDownload", "counterDownload")
    app1.build("counterDownload.mdaq")
    app1.start(0.1, 20)
    app1.close()
    time.sleep(1)

    app2 = App(device)
    app2.attach()

    with app2.Stream("Download/1", 10) as stream:
        vs = app2.read(stream)["Download/1"]

    app2.stop()
    app2.close()

    assert app2.is_done()
    assert all([v >= 10 for v in vs])


def test_attach_recieve_params(device):
    app1 = App(device)
    app1.upload("models/numberWatch", "numberWatch")
    app1.build("numberWatch")
    app1.start(0.1, 20)
    app1.write("Number/value", 2.5)
    app1.close()
    time.sleep(1)

    app2 = App(device)
    app2.attach()
    v = app2.read("Watch/1")
    app2.stop()
    app2.close()

    assert v == [2.5]
    assert app2.info() == {
        "inputs": {"Watch/1": {"rows": 1, "columns": 1, "stream": False}},
        "properties": {"Number/value": 2.5}
    }


@pytest.mark.model_name("multiTypes")
def test_info(model):
    assert model.info() == {
        "inputs": {
            "Download/1": {"columns": 1, "rows": 1, "stream": True},
            "Plot/1": {"columns": 1, "rows": 5, "stream": True},
            "Plot/2": {"columns": 10, "rows": 1, "stream": True},
            "Plot 2/1": {"columns": 4, "rows": 3, "stream": True},
        },
        "properties": {
            "Counter Limited/limit": 7,
            "Counter Limited/reset": 0,
            "Number/value": [1, 2, 3, 4, 5],
            "Number 2/value": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "From File/interpolation": 0,
        }
    }


def test_info_after_write(model):
    model.write("Number/value", 24.5)

    assert model.info() == {
        "inputs": {"Watch/1": {"rows": 1, "columns": 1, "stream": False}},
        "properties": {"Number/value": 24.5}
    }


def test_info_after_start_and_write(running_model):
    running_model.write("Number/value", -44)

    assert running_model.info() == {
        "inputs": {"Watch/1": {"rows": 1, "columns": 1, "stream": False}},
        "properties": {"Number/value": -44}
    }


# MBs should be powers of 2
@pytest.mark.parametrize("MBs", ["2 MB/s", "4 MB/s", "8 MB/s", "16 MB/s"])
@pytest.mark.model_name("sequence1000")
def test_performance_1_channel(model, MBs):
    megabytesPerSecond = int(MBs.split(" MB/s")[0])
    sequencesPerSecond = megabytesPerSecond * 1000 // 8
    samplesPerSecond = sequencesPerSecond * 1000
    interval = 1 / sequencesPerSecond
    readCount = 10
    streamSize = sequencesPerSecond // readCount

    data_recieved = 0
    model.start(interval, 1)

    with model.Stream(["Download/1"], streamSize) as stream:
        for _ in range(readCount):
            data_recieved += len(model.read(stream)["Download/1"])

    assert data_recieved == samplesPerSecond, f"recieved ({int(100 * data_recieved / samplesPerSecond)} %)"


@pytest.mark.parametrize("channels_count", [2, 4, 8, 16, 32])
def test_performance_multi_channels(app, channels_count):
    model_name = f"channels{channels_count}x1000"
    app.upload(f"models/{model_name}", model_name)
    app.build(model_name)
    app.start(0.1, 1)

    channels = [f"Download{'' if i == 1 else f' {i}'}/1" for i in range(1, channels_count + 1)]
    with app.Stream(channels, 1) as stream:
        for _ in range(10):
            data = app.read(stream)
            for values in data.values():
                assert len(values) == 1000
