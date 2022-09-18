#!/bin/bash

#kubectl apply -f service-monitor.yaml

#kubectl -n kube-system create configmap grafana-dashboard-config --from-file=grafana-dashboard-config.yaml

#kubectl -n kube-system create configmap grafana-source-config --from-file=grafana-datasource.yaml


curl "https://docs.portworx.com/samples/k8s/pxc/portworx-cluster-dashboard.json" -o portworx-cluster-dashboard.json && \
curl "https://docs.portworx.com/samples/k8s/pxc/portworx-node-dashboard.json" -o portworx-node-dashboard.json && \
curl "https://docs.portworx.com/samples/k8s/pxc/portworx-volume-dashboard.json" -o portworx-volume-dashboard.json && \
#curl "https://docs.portworx.com/samples/k8s/pxc/performance.json" -o portworx-performance-dashboard.json && \
curl "https://docs.portworx.com/samples/k8s/pxc/portworx-etcd-dashboard.json" -o portworx-etcd-dashboard.json && \
kubectl -n kube-system create configmap grafana-dashboards --from-file=portworx-cluster-dashboard.json --from-file=performance.json --from-file=portworx-node-dashboard.json --from-file=portworx-volume-dashboard.json --from-file=portworx-etcd-dashboard.json



#kubectl apply -f grafana.yaml

