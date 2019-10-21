.PHONY: build clean container container-smoke dev-tools image install lint test

help:
	@echo "  build        build the package"
	@echo "  clean        remove intermediate build artifacts"
	@echo "  container    create a container from the wellknown image"
	@echo "  container-smoke   smoke test the container"
	@echo "  dev-tools    install the develepment tools necessary to build"
	@echo "  image        build the wellknown docker image"
	@echo "  install      install this program"
	@echo "  lint         run static analysis against the source code"
	@echo "  test         run unit tests"


PYDIR=src/grav
TESTDIR=test
DISTDIR=dist
DEV_REQ=dev-requirements.txt
PYSRC=$(shell find $(PYDIR) -name '*.py') setup.py
# TODO: make this handle versioning properly
# if I planned on changing the version
PYTEST=$(shell find $(TESTDIR) -name '*.py')
WHEEL=$(DISTDIR)/gravitational_audition-1.0.0rc1-py3-none-any.whl
INSTALL_COOKIE=.installed
TOOLS_COOKIE=.tools
PYTHON_SCHMUTZ=$(WHEEL) $(TOOLS_COOKIE) $(INSTALL_COOKIE)


DOCKERDIR=wellknown-container
IMAGE_ID=$(DOCKERDIR)/.image_id
CONTAINER_ID=$(DOCKERDIR)/.container_id
IMAGE_TAR=$(PYDIR)/wellknown.tar
DOCKER_SCHMUTZ=$(IMAGE_TAR) $(IMAGE_ID) $(CONTAINER_ID)


$(IMAGE_ID):  $(DOCKERDIR)/Dockerfile $(DOCKERDIR)/loop.sh
	docker build  --iidfile $(IMAGE_ID) $(DOCKERDIR)

$(IMAGE_TAR): $(IMAGE_ID)
	docker save --output $(IMAGE_TAR) $(shell cat $(IMAGE_ID))

$(CONTAINER_ID): $(IMAGE_ID)
	rm -f $(CONTAINER_ID)
	docker create --cidfile $(CONTAINER_ID) $(shell cat $(IMAGE_ID))

$(INSTALL_COOKIE): $(WHEEL)
	pip install --upgrade $(WHEEL)
	pip freeze --all >> $(INSTALL_COOKIE)

$(TOOLS_COOKIE): $(DEV_REQ)
	pip install -r $(DEV_REQ)
	pip freeze --all >> $(TOOLS_COOKIE)

$(WHEEL): $(TOOLS_COOKIE) $(PYSRC) $(IMAGE_TAR)
	pip wheel --wheel-dir dist/ .

build: $(WHEEL)

dev-tools: $(TOOLS_COOKIE)

image: $(IMAGE_TAR)

install: $(INSTALL_COOKIE)

container: $(CONTAINER_ID)

container-smoke: $(CONTAINER_ID)
	docker start $(shell cat $(CONTAINER_ID))
	sleep 1
	docker stop $(shell cat $(CONTAINER_ID))
	docker logs $(shell cat $(CONTAINER_ID))

lint: $(TOOLS_COOKIE)
	flake8 $(PYSRC) $(PYTEST)

test: $(TOOLS_COOKIE) $(INSTALL_COOKIE)
	pytest $(TEST_DIR)

clean:
	rm -f $(DOCKER_SCHMUTZ) $(PYTHON_SCHMUTZ)
