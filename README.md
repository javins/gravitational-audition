# Gravitational Interview Project for Walt Della
In 2019-10 I applied for a position with Gravitational in Seattle. This is
the project they asked me to complete as part of their remote interview
process.

## Quickstart

### Prerequisites
To run this project you need an Ubuntu 18.04 machine with Python 3 v3.6.8
pip, Docker 18.09.7+ installed. You can run the following command to
install these.  You will need sudo or root.

```
sudo apt-get update
sudo apt install docker python3 python3-pip
```

After installing docker, you will need to make sure the user who will run
this program has access to docker.  Follow the instructions here:

https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user

### Installation
Download the version you want to install from:

https://github.com/javins/gravitational-audition/releases

Install it with the following command:

```sudo pip3 install $WHEEL```

Where `$WHEEL` is subsituted for the filename of the file you downloaded.

### Execution
After installation, you may run `grav-api-test`.  This command should be
in your path. You should see output like the following if everything
works correctly:

```
$ grav-api-test
test_start_stop_logs (grav.test.ContainerStartStopLogTest) ... ok

----------------------------------------------------------------------
Ran 1 test in 2.530s

OK
```


## Developing
To set up a development environment for this test, perform the following
steps.

Follow the instructions in the Quickstart Prerequisites.

Install these Debian packages:
```
apt install make python3-venv
```

Create a python virtualenv sandbox to work from and activate the sandbox:
```
python 3 -m venv venv
source venv/bin/activate
```

Install the python development requirements:
```
make dev-tools
```

Run other make targets that interest you:
```
$ make
  build        build the package
  clean        remove intermediate build artifacts
  container    create a container from the wellknown image
  container-smoke   smoke test the container
  dev-tools    install the develepment tools necessary to build
  image        build the wellknown docker image
  install      install this program
  lint         run static analysis against the source code
  test         run unit tests
```

You can of course open up the Makefile and look at what the various targets
do if prefer to run `pip` or `python setup.py` or `docker` commands directly.

Scoping and initial design can be found in the [design doc](DESIGN.md).
