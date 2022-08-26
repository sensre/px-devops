#!/bin/bash 

kubectl delete -f service-monitor.yaml

kubectl -n kube-system delete configmap grafana-dashboard-config

kubectl -n kube-system delete configmap grafana-source-config

kubectl -n kube-system delete configmap grafana-dashboards

kubectl delete -f grafana.yaml
