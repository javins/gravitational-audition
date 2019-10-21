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

My choice of unittest as a harness is not because I like the framework.
I find its OO heavy syntax and camelcasing rather heavyweight and
java-esque.  I much prefer light weight imperative pytest style syntax.
However I didn't want to introduce 3rd party dependencies and writing
a minimal pytest clone was not likely to be worth the effort -- maybe
an extra 100-150 LoC, and rather dynamic/introspecitve code at that.

Unittest is what's available and does the trick.
"""
import os
import re
from pkg_resources import resource_filename

from grav.client import demux_logs, DockerClient
from grav.harness import DockerApiTest, assert_status


class ContainerStartStopLogTest(DockerApiTest):
    """Execercise start, stop and logs on a single docker container."""

    def setUp(self):
        # If this were real, I'd pass these magic strings stattered through
        # file as params and have them loaded from a config.
        image_tar = resource_filename(__name__, "wellknown.tar")

        # It'd be better to nest client, image, container setup/teardown
        # so that in the case client & image succeed but container fails
        # we only run the teardown for image & client, and skip container
        # teardown since it was never set up.
        #
        # Similarly, if the code knows which part of the setup/teadown fails,
        # it could chain errors to poinpoint which resources are dangling,
        # and probably need to be cleaned up by hand.
        #
        # That is more effort than this sample merits imo, so setup/teardown
        # are all in one, with no effort to pinpoint which resources may
        # leak in the case of failure during setup/teardown.
        # -- wdella 2019-10
        client = DockerClient("/var/run/docker.sock")

        # load image from tar, get image id
        with open(image_tar, 'rb') as fh:
            size = os.stat(image_tar).st_size
            headers = {'Content-Type': 'application/tar', 'Content-Length': size}
            resp = client.post("/images/load?fromSrc=-", body=fh, headers=headers)

        assert_status(resp, 200)
        json = resp.json()
        # N.B. I haven't found a way to avoid this regex parsing.  I'd love it
        # if this api returned a proper json map I could parse the ID out of
        # -- wdella 2019-10
        match = re.match(r"Loaded image ID: (sha256:[\da-f]{64})", json['stream'])
        image_id = match.group(1)

        # create container, get container id
        data = {"Image": image_id}
        headers = {"Content-Type": "application/json"}
        resp = client.post("/containers/create", body=data, headers=headers)
        assert_status(resp, 201)
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
        self.assertStatus(resp, 204)

        # stop
        stop_path = "/containers/%s/stop" % container_id
        resp = client.post(stop_path)
        resp.read()  # TODO: have this handled by the client
        self.assertStatus(resp, 204)

        # logs
        logs_path = "/containers/%s/logs" % container_id
        logs_path += "?stdout=true&stderr=true"
        resp = client.get(logs_path)
        self.assertStatus(resp, 200)
        # logs doesn't return json, but a multiplexed stream
        stdout, stderr = demux_logs(resp.read())

        # validate
        # future work: check return code?

        # stderr first, as in this case we'd expect stdout to be corrupt, and
        # the stderr content will likely be useful for triage.
        self.assertEqual(stderr, "")
        stdout_lines = stdout.splitlines()
        self.assertEqual(stdout_lines[0], "Hello Gravitational!")
        self.assertEqual(stdout_lines[-1], "Terminated. Bye!")

    def tearDown(self):
        client = self.client
        container_id = self.container_id
        image_id = self.image_id

        # if the test dies partway through, the container may
        # still be running, and should be stopped
        inspect_path = "/containers/%s/json" % container_id
        resp = client.get(inspect_path)
        assert_status(resp, 200)
        json = resp.json()
        state = json["State"]
        running = state["Running"]
        if running:
            # stop
            stop_path = "/containers/%s/stop" % container_id
            resp = client.post(stop_path)
            resp.read()  # TODO: have this handled by the client
            assert_status(resp, 204)

        # delete container
        delete_path = "/containers/" + container_id
        resp = client.request("DELETE", delete_path)
        resp.read()  # TODO: have this handled by the client
        assert_status(resp, 204)

        # delete image
        delete_path = "/images/" + image_id
        resp = client.request("DELETE", delete_path)
        resp.read()  # TODO: have this handled by the client
        # why isn't this 204 like the other api endpoints without a body?
        assert_status(resp, 200)
