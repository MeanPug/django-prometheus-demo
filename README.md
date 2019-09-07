# django-prometheus-demo
Basic demo application showcasing Django + Prometheus + Kubernetes

## Running
### Dependencies
You'll need [Docker](https://docs.docker.com/install/) installed and a Kubernetes cluster to deploy Prometheus to ([Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/) should work just fine). You'll also need to install the [Tiller](https://helm.sh/docs/install/) server into the cluster and have the client available locally.

### Install the Web App
```
docker build -t django-prometheus-demo:latest .
helm upgrade --install demo helm/demo
```

### Install the prometheus helm chart
```
helm upgrade --install prometheus stable/prometheus -f helm/prometheus/values.yaml
```

## Development
```bash
docker-compose up -d
```
