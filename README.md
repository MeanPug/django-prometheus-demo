# django-prometheus-demo
Basic demo application showcasing Django + Prometheus + Kubernetes. For more reading about the why and how of custom metrics with Django, you can check out the post [custom application metrics with Django, Prometheus, and Kubernetes](https://labs.meanpug.com/custom-application-metrics-with-django-prometheus-and-kubernetes/).

## Running
### Dependencies
You'll need [Docker](https://docs.docker.com/install/) installed and a Kubernetes cluster to deploy Prometheus to ([Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/) should work just fine). You'll also need to install the [Tiller](https://helm.sh/docs/install/) server into the cluster and have the client available locally.

### Install the Web App
```
# in real life, we wouldnt VC the .htpasswd, but this is easy
kc create secret generic prometheus-basic-auth --from-file=.htpasswd=prometheus/.htpasswd
make
```

### Install the prometheus helm chart
```
helm upgrade --install prometheus stable/prometheus -f helm/prometheus/values.yaml
```

### Testing
The primary urls for interacting with the app are:

* /walks/start/
* /walks/<walk_id>/complete/
* /walks/<walk_id>/status/

You can perform some actions at these locations, then verify that metrics are set properly by either:

* Visiting the Prometheus server at http://localhost:9090
* Using the `/metrics` endpoint to manually verify

## Development
```bash
docker-compose up -d
```
