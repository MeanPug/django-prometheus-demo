IMAGE = meanpugdigital/django-prometheus-demo
TAG = latest

.PHONY: build push deploy

all: build push deploy

build:
	docker build -t $(IMAGE):$(TAG) .

push:
	docker push $(IMAGE):$(TAG)

deploy:
	helm dep update helm/demo
	helm upgrade --install demo helm/demo
