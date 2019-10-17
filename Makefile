.PHONY: build clean image container container-smoke

help:
	@echo "  image        build the wellknown docker image"
	@echo "  container    create a container from the wellknown image"
	@echo "  container-smoke   smoke test the container"

PYDIR=src/grav
DISTDIR=dist
PYSRC=$(shell find $(PYDIR) -name '*.py')
# TODO: make this handle versioning properly
# if I planned on changing the version
WHEEL=$(DISTDIR)/gravitational_audition-0.1.0-py3-none-any.whl
PYTHON_SCHMUTZ=$(WHEEL)

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

$(WHEEL): $(PYSRC) $(IMAGE_TAR)
	pip wheel --wheel-dir dist/ .

build: $(WHEEL)

image: $(IMAGE_TAR)

container: $(CONTAINER_ID)

container-smoke: $(CONTAINER_ID)
	docker start $(shell cat $(CONTAINER_ID))
	sleep 1
	docker stop $(shell cat $(CONTAINER_ID))
	docker logs $(shell cat $(CONTAINER_ID))

clean:
	rm -f $(DOCKER_SCHMUTZ) $(PYTHON_SCHMUTZ)
