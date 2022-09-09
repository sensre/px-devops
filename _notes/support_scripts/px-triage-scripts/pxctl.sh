#!/bin/bash

CMD=$1
PX_POD=$(kubectl get pods -l name=portworx -n kube-system -o jsonpath='{.items[0].metadata.name}')

#OPT_POD=$(kubectl -n kube-system get pods -l name=portworx-operator -o jsonpath='{.items[0].spec.containers.image}')

uname -a

kubectl version

kubectl exec $PX_POD -n kube-system -- /opt/pwx/bin/pxctl status

kubectl exec $PX_POD -n kube-system -- /opt/pwx/bin/pxctl volume list

