.PHONY: clean image container container-smoke

help:
	@echo "  image        build the wellknown docker image"
	@echo "  container    create a container from the wellknown image"
	@echo "  container-smoke   smoke test the container"

DOCKERDIR=wellknown-container
IMAGE_ID=$(DOCKERDIR)/.image_id
CONTAINER_ID=$(DOCKERDIR)/.container_id

$(IMAGE_ID):  $(DOCKERDIR)/Dockerfile $(DOCKERDIR)/loop.sh
	docker build  --iidfile $(IMAGE_ID) $(DOCKERDIR)

$(CONTAINER_ID): $(IMAGE_ID)
	rm -f $(CONTAINER_ID)
	docker create --cidfile $(CONTAINER_ID) $(shell cat $(IMAGE_ID))

image: $(IMAGE_ID)

container: $(CONTAINER_ID)

container-smoke: $(CONTAINER_ID)
	docker start $(shell cat $(CONTAINER_ID))
	sleep 1
	docker stop $(shell cat $(CONTAINER_ID))
	docker logs $(shell cat $(CONTAINER_ID))

clean:
	rm -f $(IMAGE_ID) $(CONTAINER_ID)
