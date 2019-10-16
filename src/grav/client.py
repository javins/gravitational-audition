import json
import socket
from http.client import HTTPConnection, HTTPResponse


"""
The native docker python client found at https://github.com/docker/docker-py/
is probably a fine choice.  However, since we specifically want to:

    1) test the daemon
    2) show my development ability

I've chosen to write a minimal docker client.
"""


class FriendlyHTTPResponse(HTTPResponse):
    # I really like requests .json() method on response objects.
    # this class is solely to enable that -- wdella 2019-10
    def __init__(self, *args, **kwargs):
        super(FriendlyHTTPResponse, self).__init__(*args, **kwargs)

    def json(self):
        """Reads the response body, parses it as json, and returns the result."""
        return json.loads(self.read())


class SocketHTTPConnection(HTTPConnection):
    """
    Wrapper to allow httplib to be used with a file socket.

    HTTPConnection typically expects to be given a http url.
    This is the minimal glue to allow it to be used with a
    file path to a socket instead.
    """
    def __init__(self, base_url, socket_path, timeout=10):
        super(SocketHTTPConnection, self).__init__(
            'localhost', timeout=timeout
        )
        self.socket_path = socket_path
        self.timeout = timeout

    def connect(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self.socket_path)
        self.sock = sock

    def response_class(self, sock, *args, **kwargs):
        return FriendlyHTTPResponse(sock, *args, **kwargs)


class DockerClient:
    """
    A minimal docker client that can GET & POST to a socket.
    """
    def __init__(self, target):
        self._target = target
        # With more time, I'd do  connection pooling instead of
        # a new connection for each request
        self.conn = SocketHTTPConnection("/", self._target)
        self.conn.connect()

    def get(self, path, headers={}):
        return self.request("GET", path, headers=headers)

    def post(self, path, body=None, headers={}):
        return self.request("POST", path, body=body, headers=headers)

    def request(self, verb, path, body=None, headers={}):
        if type(body) == dict:  # automatic json conversion
            body = json.dumps(body)
        self.conn.request(verb, path, body=body, headers=headers)
        resp = self.conn.getresponse()
        return resp

    # make sure not to  leak connections, close when the client falls out of scope
    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    target = "/var/run/docker.sock"
    client = DockerClient(target)
    resp = client.get("/images/json")
    data = resp.read()
    print(data)
