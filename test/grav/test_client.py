from grav.client import demux_logs


def test_demux_stdout():
    data = b''.join([
        b'\x01\x00\x00\x00\x00\x00\x00\x15Hello Gravitational!\n',
        b'\x01\x00\x00\x00\x00\x00\x00\x11Terminated. Bye!\n',
    ])
    stdout, stderr = demux_logs(data)
    assert stderr == ""
    assert stdout == "Hello Gravitational!\nTerminated. Bye!\n"


def test_demux_mixed():
    data = b''.join([
        b'\x01\x00\x00\x00\x00\x00\x00\x15Hello Gravitational!\n',
        b'\x02\x00\x00\x00\x00\x00\x00\x11Terminated. Bye!\n',
        b'\x01\x00\x00\x00\x00\x00\x00\x11Terminated. Bye!\n',
    ])
    stdout, stderr = demux_logs(data)
    assert stderr == "Terminated. Bye!\n"
    assert stdout == "Hello Gravitational!\nTerminated. Bye!\n"
