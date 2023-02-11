#!/bin/bash

CMD=$1

PX_POD=$(kubectl get pods -l name=portworx -n kube-system -o jsonpath='{.items[0].metadata.name}')

#OPT_POD=$(kubectl -n kube-system get pods -l name=portworx-operator -o jsonpath='{.items[0].spec.containers.image}')

kubectl exec $PX_POD -n kube-system -- uname -a

echo "*****************"

kubectl version --short

echo "******************"

kubectl exec $PX_POD -n kube-system -- /opt/pwx/bin/pxctl status

echo "******************"

kubectl exec $PX_POD -n kube-system -- /opt/pwx/bin/pxctl cluster provision-status

echo "******************"

kubectl exec $PX_POD -n kube-system -- /opt/pwx/bin/pxctl service kvdb members

echo "******************"

kubectl exec $PX_POD -n kube-system -- /opt/pwx/bin/pxctl volume list

echo "******************"
