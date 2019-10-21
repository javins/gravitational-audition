# Gravitational Interview Project for Walt Della

## Quickstart

### Prerequisites
To run this test you need an Ubuntu 18.04 machine with Python 3 v3.6.8
pip, Docker 18.09.7+ installed.

```apt install docker python3 python3-pip```


### Installation
Download the version you want to install from:

https://github.com/javins/gravitational-audition/releases

Install it with the following command:

```pip install $WHEEL```

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
To set up a development environment for this test, perform the following steps.

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

```

You can of course open up the Makefile and look at what the various targets
do if prefer to run `pip` or `python setup.py` or `docker` commands directly.

Scoping and initial design can be found in the [design doc](DESIGN.md).
