# Storage Cluster Options

You can use "kubectl explain storagecluster" to see a description for all the fields in the storagecluster object.



List of required images (for air-gapped installation):

```
gcr.io/google_containers/kube-controller-manager-amd64:$kube_version
gcr.io/google_containers/kube-scheduler-amd64:$kube_version
k8s.gcr.io/pause:3.1
quay.io/openstorage/csi-attacher:v1.2.1-1
quay.io/k8scsi/csi-node-driver-registrar:v1.1.0
quay.io/openstorage/csi-provisioner:v1.4.0-1
quay.io/k8scsi/csi-snapshotter:v2.0.0
quay.io/k8scsi/csi-resizer:v0.3.0
openstorage/stork:2.3.1
portworx/autopilot:1.1.0
portworx/px-lighthouse:2.0.6
portworx/lh-config-sync:2.0.6
portworx/lh-stork-connector:2.0.6
portworx/px-node-wiper:2.1.4
portworx/oci-monitor:2.4.0
portworx/px-enterprise:2.4.0
openstorage/openstorage-operator:1.3-dev
Air-gapped bootstrap helper

````

See also https://install.portworx.com/air-gapped (docs ref) boostrap script, that helps automate import of the container-images into air-gapped customer's environments.



PX components list:

```
portworx [portworx csi-node-driver-registrar]
portworx-api
portworx-proxy
portworx-operator
stork
stork-scheduler
px-lighthouse [px-lighthouse config-sync stork-connector]
autopilot
px-csi-ext [csi-external-provisioner csi-snapshotter csi-resizer]
portworx-pvc-controller
px-prometheus-operator
prometheus

```