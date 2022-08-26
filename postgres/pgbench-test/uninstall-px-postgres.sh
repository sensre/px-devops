#!/bin/bash

echo "Deploying postgres app..."
kubectl delete -f px-postgres-app.yaml

echo "Deploying postgres SC & PVC for wordpress..."
kubectl delete -f px-postgres-sc.yaml
kubectl delete -f px-postgres-vol.yaml