"""
This file contains meat of the Gravitational QA coding challenge.

The test_start_stop_logs() method performs the test as requested
in the challenge.

The setUp() method does all the provisioning necessary to go from:
  "package is installed" -> "start/stop/logs a wellknown container"

The tearDown() function attempts to unwind any dangling resources
from setUp() and test_start_stop_logs(). Ideally leaving a clean
test enviromnent if it runs to completion.  This is important for
idempotency.
"""
import os
import re
from pkg_resources import resource_filename
from unittest import TestCase

from grav.client import demux_logs, DockerClient


class ContainerStartStopLogTest(TestCase):
    """
    Execercise start, stop and logs on a single docker container.
    """

    def setUp(self):
        # If this were real, I'd pass these magic strings stattered through
        # file as params and have them loaded from a config.
        image_tar = resource_filename(__name__, "wellknown.tar")

        # It'd be better to nest client, image, container setup/teardown
        # so that in the case client & image succeed but container fails
        # we only run the teardown for image & client, and skip container
        # teardown since it was never set up.
        #
        # That is more effort than this sample merits imo, so setup/teardown
        # are all in one. -- wdella 2019-10
        client = DockerClient("/var/run/docker.sock")

        # load image from tar, get image id
        with open(image_tar, 'rb') as fh:
            size = os.stat(image_tar).st_size
            headers = {'Content-Type': 'application/tar', 'Content-Length': size}
            resp = client.post("/images/load?fromSrc=-", body=fh, headers=headers)

        assert resp.status == 200
        json = resp.json()
        match = re.match(r"Loaded image ID: (sha256:[\da-f]{64})", json['stream'])
        image_id = match.group(1)

        # create container, get container id
        data = {"Image": image_id}
        headers = {"Content-Type": "application/json"}
        resp = client.post("/containers/create", body=data, headers=headers)
        assert resp.status == 201
        json = resp.json()
        container_id = json['Id']

        self.client = client
        self.image_id = image_id
        self.container_id = container_id

    def test_start_stop_logs(self):
        container_id = self.container_id
        client = self.client
        # start
        start_path = "/containers/%s/start" % container_id
        resp = client.post(start_path)
        resp.read()  # TODO: have this handled by the client
        assert resp.status == 204

        # stop
        stop_path = "/containers/%s/stop" % container_id
        resp = client.post(stop_path)
        resp.read()  # TODO: have this handled by the client
        assert resp.status == 204

        # logs
        logs_path = "/containers/%s/logs" % container_id
        logs_path += "?stdout=true&stderr=true"
        resp = client.get(logs_path)
        assert resp.status == 200
        # logs doesn't return json, but a multiplexed stream
        stdout, stderr = demux_logs(resp.read())

        # validate
        lines = stdout.splitlines()
        assert lines[0] == "Hello Gravitational!"
        assert lines[-1] == "Terminated. Bye!"
        assert stderr == ""

    def tearDown(self):
        client = self.client
        container_id = self.container_id
        image_id = self.image_id

        # if the test dies partway through, the container may
        # still be running, and should be stopped
        inspect_path = "/containers/%s/json" % container_id
        resp = client.get(inspect_path)
        assert resp.status == 200
        json = resp.json()
        state = json["State"]
        running = state["Running"]
        if running:
            # stop
            stop_path = "/containers/%s/stop" % container_id
            resp = client.post(stop_path)
            resp.read()  # TODO: have this handled by the client
            assert resp.status == 204

        # delete container
        delete_path = "/containers/" + container_id
        resp = client.request("DELETE", delete_path)
        resp.read()  # TODO: have this handled by the client
        assert resp.status == 204

        # delete image
        delete_path = "/images/" + image_id
        resp = client.request("DELETE", delete_path)
        resp.read()  # TODO: have this handled by the client
        assert resp.status == 200  # why isn't this 204 like the other api endpoints?
