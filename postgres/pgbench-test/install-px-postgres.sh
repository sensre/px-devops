#!/bin/bash


echo "Deploying postgres SC & PVC for wordpress..."
kubectl apply -f px-postgres-sc.yaml
kubectl apply -f px-postgres-vol.yaml

echo "Deploying postgres app..."
kubectl apply -f px-postgres-app.yaml

