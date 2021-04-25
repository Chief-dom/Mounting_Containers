OWNER := cogentdom
IMAGE_NAME := python #dashboard
VERSION := ubuntu
REPOSITORY := mounting_containers
IMAGE_ID := 0cdb6b5588e5 #d94e96d264e7
REGISTRY := chiefdom

default: release

tag:
	docker tag $(IMAGE_ID) docker.pkg.github.com/$(OWNER)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION)

build: ## Build the container forrmated for githubs api
	docker build -t docker.pkg.github.com/$(OWNER)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION) .

release: tag build publish ## Make a release by building and publishing tagged image to Docker Trusted Registry (DTR)

publish: ## Publish image to DTR
	@echo 'publish $(REGISTRY)/$(IMAGE_NAME):$(VERSION)'
	docker push docker.pkg.github.com/$(OWNER)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION)
