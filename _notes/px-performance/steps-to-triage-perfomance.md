# How to improve PX Performance - Best Practices 

•  Check applications uses stork as scheduler for the Hyperconvergence

• Check the px volumes uses the access pattern - IO profile for the better performance. 
	• auto
	• db
	• db_remote
	• sequential
	• random

• Check if there is any:
	• VolumePlacementStrategy 
	• Cluster topology - region/zone/racks

• Journal device to absorb Portworx metadata writes

• RUN FIO and measure the performances on the disk and px volumes. 

• Check the node resources and performance:
	• uptime
	• top (or htop)
	• ps
	• vmstat
	• iostat
	• mpstat
	• free

• Deploy the Prometheus and Grafana Dashboard and measure the cluster performance status.
